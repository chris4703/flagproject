"""Run fictional interviews through the live HTTP API and download a finished report."""

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


EXPECTED = {
    "police-room-calendar": ("existing", "Low", 0, False),
    "fire-renewal-view": ("self_service", "High", 3, True),
    "comms-practice-kit-notes": ("hybrid", "Elevated", 2, False),
    "fire-office-supply-list": ("automation", "Low", 1, False),
    "police-training-forms": ("discovery", "Elevated", 3, True),
    "comms-display-guide": ("ai", "Elevated", 1, False),
    "fire-badge-access": ("automation", "High", 3, True),
}
BENEFITS = {
    "police-room-calendar": "low", "fire-renewal-view": "moderate", "comms-practice-kit-notes": "high",
    "fire-office-supply-list": "moderate", "police-training-forms": "unknown", "comms-display-guide": "low",
    "fire-badge-access": "moderate",
}


def run(base, require_model, destination, scenario_id=None):
    def request(path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        headers = {"User-Agent": "Mozilla/5.0 (Flagstaff WIP rehearsal)"}
        if data:
            headers.update({"Content-Type": "application/json", "Origin": base})
        req = Request(base + path, data, headers)
        with urlopen(req, timeout=20) as reply:
            blob = reply.read()
            return json.loads(blob) if reply.headers.get_content_type() == "application/json" else blob

    def reject(status, path, payload):
        try:
            request(path, payload)
        except HTTPError as error:
            if error.code == status:
                return
            raise
        raise AssertionError(f"Expected HTTP {status}")

    health = request("/api/health")
    if require_model:
        assert health["model_ready"], "Local inference is unavailable"
    if destination:
        destination.mkdir(parents=True, exist_ok=True)
    scenarios = (scenario_id,) if scenario_id else EXPECTED
    for scenario in scenarios:
        session = request("/api/sessions", {"scenario": scenario})
        path = "/api/sessions/" + session["id"]
        reject(400, path, {"action": "finish", "revision": 0})
        reject(409, path + "/download", None)
        while session["question"]:
            q = session["question"]
            result = {"action": "answer", "revision": session["revision"], "id": q["id"], **q["example_answer"]}
            old = session["revision"]
            session = request(path, result)
            if old == 0:
                reject(409, path, result)
                draft = request(path, {"action": "back", "revision": session["revision"]})
                assert draft["draft"] == q["example_answer"] and draft["question"]["id"] == "goal"
                session = request(path, {**result, "revision": draft["revision"]})
            assert len(session["evidence"]) <= 20
        report = request(path, {"action": "finish", "revision": session["revision"],
                                "expected_benefit": BENEFITS[scenario]})["report"]
        decision = report["decision"]
        actual = decision["code"], decision["risk"], decision["tier"], decision["hold"]
        assert actual == EXPECTED[scenario], (scenario, actual)
        fields = {answer["id"] for answer in report["evidence"]}
        assert {"data", "systems", "changes", "impact", "owner", "boundary"} <= fields
        if scenario == "police-room-calendar":
            assert report["question_count"] <= 10 and report["model_count"] == 0
            assert "show staff how the feature works" in decision["recommendation"]
        if not health["model_ready"]:
            assert report["model_count"] == 0
        if scenario == "fire-renewal-view":
            assert {item["name"] for item in report["checks"] if item["level"] == "hold"} == {"Data classification"}
        if scenario == "comms-practice-kit-notes":
            review = {item["name"] for item in report["checks"] if item["level"] == "review"}
            assert {"System access and transfers", "Human oversight"} <= review
            if require_model:
                assert report["model_count"] > 0
        if scenario == "police-training-forms":
            assert len(report["unknowns"]) >= 4
        if scenario == "comms-display-guide":
            assert report["scores"]["ai"]["total"] >= 6 > report["scores"]["automation"]["total"]
            assert any(item["name"] == "Human oversight" and item["level"] == "review" for item in report["checks"])
        if scenario == "fire-badge-access":
            choices = {answer["id"]: answer["value"] for answer in session["evidence"]}
            assert {key: choices[key] for key in ("impact", "changes", "review")} == {
                "impact": "serious", "changes": "read", "review": "prior",
            }
            holds = {item["name"] for item in report["checks"] if item["level"] == "hold"}
            assert {"Data classification", "Operational consequence"} <= holds
        raw = request(path + "/download")
        assert report["id"].encode() in raw and request(path)["report"] == report
        assert b"## Screening scores" in raw and b"Evidence: data" not in raw
        if decision["hold"]:
            assert decision["route"] == "IT triage"
            assert raw.index(b"Do not pilot with real data.") < raw.index(b"## Triage recommendation")
            assert raw.count(b"**Information Security**") == 1
        if destination:
            (destination / f"{scenario}-assessment.md").write_bytes(raw)
        print(f"{scenario}: {report['id']}, {report['question_count']} answers, {report['model_count']} AI follow-ups, {actual}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8878")
    parser.add_argument("--require-model", action="store_true")
    parser.add_argument("--write", type=Path)
    parser.add_argument("--scenario", choices=EXPECTED, help="Run only this practice case.")
    args = parser.parse_args()
    run(args.url, args.require_model, args.write, args.scenario)
