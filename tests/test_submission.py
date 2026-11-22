import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from navigator import analyst
from navigator.assessment import report_view
from navigator.questions import MANDATORY
import server


class SubmissionTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        fixtures = Path(__file__).parent / "fixtures" / "regression-scenarios.json"
        scenarios = patch.object(server, "SCENARIOS", json.loads(fixtures.read_text()))
        scenarios.start()
        self.addCleanup(scenarios.stop)
        db_path = patch.object(server, "DB", Path(directory.name) / "test.sqlite3")
        db_path.start()
        self.addCleanup(db_path.stop)
        server.initialize()

    def test_new_workflow_requires_valid_follow_up_contact(self):
        for contact in (None, {"name": "", "email": "a@example.invalid"},
                        {"name": "Jordan Sample", "email": "bad email"}):
            with self.subTest(contact=contact), self.assertRaises(server.RequestError) as error:
                server.new_session({"department": "Police", "contact": contact})
            self.assertEqual(error.exception.status, 400)
        with server.db() as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM interviews").fetchone()[0], 0)

    def test_process_follow_up_can_be_focused_or_skipped(self):
        opening = "Every Thursday I copy open loans from the log. I send the list to the lead."
        excerpts = {"start": "Every Thursday", "steps": "I copy open loans from the log",
                    "finish": "I send the list to the lead"}
        for complete in (True, False):
            with self.subTest(complete=complete), patch.object(server.local_model, "process_clues") as model:
                model.return_value = excerpts if complete else {key: excerpts[key] for key in ("start", "steps")}
                state = server.new_session({"scenario": "police-inventory"})
                sid = state["id"]
                state = server.mutate(sid, {"action": "answer", "revision": 0, "id": "goal", "note": opening})
                if complete:
                    self.assertEqual(state["question"]["id"], "existing")
                    self.assertTrue(state["question"]["process_reused"])
                else:
                    self.assertEqual(state["question"]["title"], "How do you know the task is done?")
                    self.assertEqual(state["question"]["process_context"], [excerpts["start"], excerpts["steps"]])
                back = server.mutate(sid, {"action": "back", "revision": state["revision"]})
                self.assertEqual(back["draft"], {"value": "", "note": opening})
                state = server.mutate(sid, {"action": "answer", "revision": back["revision"], "id": "goal", "note": opening})
                while state["question"]:
                    question = state["question"]
                    answer = question["example_answer"] if question["id"] != "process" else {
                        "value": "", "note": excerpts["finish"],
                    }
                    state = server.mutate(sid, {"action": "answer", "id": question["id"], "revision": state["revision"], **answer})
                finished = server.mutate(sid, {"action": "finish", "revision": state["revision"]})["report"]
                self.assertEqual(finished["question_count"], 9 if complete else 10)
                self.assertEqual(finished["decision"]["code"], "existing")
                self.assertEqual(finished["model_count"], 0)
                self.assertTrue(all(value in finished["workflow"]["Current steps"] for value in excerpts.values()))
                self.assertTrue({"data", "systems", "changes", "impact", "owner", "boundary"} <= {
                    row["id"] for row in finished["evidence"]
                })
                if not complete:
                    self.assertEqual(finished["evidence"][1]["question"], "How do you know the task is done?")

    def test_unverified_or_proposed_details_cannot_complete_process(self):
        text = ("Every Thursday I copy open loans from the log. "
                "A new dashboard would send the report to the training lead.")
        with patch.object(server.local_model, "URL", "http://localhost"), patch.object(server.local_model, "complete") as model:
            model.return_value = {"start": "Every Thursday", "steps": "I copy open loans from the log",
                                  "finish": "send the report to the training lead"}
            self.assertEqual(server.local_model.process_clues(text),
                             {"start": "Every Thursday", "steps": "I copy open loans from the log"})
            self.assertNotIn("dashboard", model.call_args.args[1]["answer"])
            model.return_value["steps"] = "Checks the returns"
            self.assertEqual(server.local_model.process_clues(text), {"start": "Every Thursday"})
        with patch.object(server.local_model, "URL", ""):
            self.assertEqual(server.local_model.process_clues(text), {})

    def test_later_context_reuses_example_but_requires_explicit_choices(self):
        state = server.new_session({"scenario": "fire-drills"})
        sid = state["id"]
        example = "If a note is missing a drill date, then flag the entry for manual review."
        review_detail = "The supervisor checks the draft before staff use it."
        data_detail = "The task uses routine inventory labels."

        def answer(value, note):
            return server.mutate(sid, {"action": "answer", "revision": state["revision"],
                                       "id": state["question"]["id"], "value": value, "note": note})

        with patch.object(server.local_model, "URL", ""):
            state = answer("", f"Every Friday our team checks drill logs. {data_detail}")
            state = answer("", "I open a CSV and read the notes. " + review_detail)
            state = answer("partial", "The tracker already has a list.")
            self.assertEqual(state["question"]["id"], "data")
            self.assertEqual(state["question"]["earlier_detail"], {"excerpt": data_detail, "source_number": 1})
            with self.assertRaisesRegex(ValueError, "Choose the answer"):
                answer("", data_detail)
            state = answer("none", data_detail)
            self.assertEqual(state["evidence"][-1]["source_number"], 1)
            while question := state["question"]:
                key = question["id"]
                self.assertNotEqual(key, "example")
                if key == "frequency":
                    self.assertEqual(question["earlier_detail"]["source_number"], 1)
                if key == "input":
                    self.assertEqual(question["earlier_detail"]["source_number"], 2)
                if key == "review":
                    self.assertEqual(question["earlier_detail"]["excerpt"], review_detail)
                fixture = question["example_answer"]
                state = answer(fixture["value"], example if key == "rules" else fixture["note"])

        self.assertTrue(set(MANDATORY) <= {row["id"] for row in state["evidence"]})
        self.assertEqual(state["reused_example"]["excerpt"], example)
        source_number = state["reused_example"]["source_number"]
        self.assertEqual(state["evidence"][source_number - 1]["id"], "rules")
        finished = server.mutate(sid, {"revision": state["revision"], "action": "finish"})
        self.assertEqual(finished["report"]["decision"]["code"], "hybrid")
        _, saved = server.lookup(sid)
        self.assertIn(f"example from question {source_number} as an acceptance test. {example}", saved["export"])
        self.assertIn("*(Detail from Q1.)*", saved["export"])

    def test_edit_removes_reusable_context_and_incomplete_example_does_not_skip(self):
        with patch.object(server.local_model, "URL", ""):
            state = server.new_session({"scenario": "fire-drills"})
            sid = state["id"]
            state = server.mutate(sid, {"action": "answer", "id": "goal", "revision": 0,
                                       "note": "The work uses patient information."})
            state = server.mutate(sid, {"action": "revise", "id": "goal", "revision": state["revision"]})
            while question := state["question"]:
                key = question["id"]
                fixture = question["example_answer"]
                if key == "goal":
                    fixture = {"value": "", "note": "If a drill log has an incomplete entry, we aren't sure what to do."}
                if key == "data":
                    self.assertNotIn("earlier_detail", question)
                if key == "example":
                    break
                state = server.mutate(sid, {"action": "answer", "id": key,
                                           "revision": state["revision"], **fixture})
            self.assertEqual(state["question"]["id"], "example")

    def test_staff_can_finish_without_optional_notes_and_unknown_data_stays_on_hold(self):
        with patch.object(server.local_model, "URL", ""):
            state = server.new_session({"scenario": "police-inventory"})
            sid = state["id"]
            while question := state["question"]:
                key = question["id"]
                payload = {"action": "answer", "id": key, "revision": state["revision"]}
                if key in ("data", "review"):
                    self.assertIn("IT can follow up.", question["hint"])
                    payload["value"] = "unknown"
                elif question["options"]:
                    payload["value"] = question["example_answer"]["value"]
                else:
                    payload["note"] = question["example_answer"]["note"]
                state = server.mutate(sid, payload)
            self.assertTrue(set(MANDATORY) <= {row["id"] for row in state["evidence"]})
            report = server.mutate(sid, {"action": "finish", "revision": state["revision"]})["report"]
            self.assertEqual(report["decision"]["code"], "existing")
            self.assertTrue(report["decision"]["hold"])
            self.assertEqual(report["decision"]["route"], "IT triage")
            checks = {check["name"]: check["level"] for check in report["checks"]}
            self.assertEqual(checks["Data classification"], "hold")

    def test_contact_stays_private_and_review_keeps_receipt_and_export(self):
        contact = {"name": "Jordan Sample", "email": "jordan+qa@example.invalid"}
        state = server.new_session({"scenario": "police-inventory", "contact": contact})
        sid = state["id"]
        self.assertTrue(state["has_contact"])
        self.assertNotIn(contact["email"], json.dumps(state))
        with patch.object(server.local_model, "propose", return_value=None) as model:
            while state["question"]:
                question = state["question"]
                state = server.mutate(sid, {"revision": state["revision"], "action": "answer",
                                            "id": question["id"], **question["example_answer"]})
            self.assertTrue(model.called)
            self.assertNotIn(contact["email"], json.dumps(model.call_args[0][0]))
        completed = server.mutate(sid, {"revision": state["revision"], "action": "finish"})
        report_id = completed["report"]["id"]
        self.assertIsNone(completed["reviewed_at"])
        self.assertEqual(completed["review_status"], "awaiting")
        self.assertNotIn(contact["email"], json.dumps(completed))

        timestamp = "2026-11-19T20:00:00-07:00"
        with server.db() as conn:
            before = analyst.report_for(conn, report_id)
            self.assertEqual(before["contact"], contact)
            self.assertNotIn(contact["name"], before["export"])
            self.assertNotIn(contact["email"], before["export"])
            reviewed = analyst.update_review(conn, report_id, timestamp, {})
            self.assertEqual(reviewed["reviewed_at"], timestamp)
            self.assertEqual(analyst.update_review(conn, report_id, "later", {}), reviewed)
            analyst.update_review(conn, report_id, "later", {
                "status": "needs_info", "revision": reviewed["revision"], "note": "Private follow-up",
            })
            self.assertEqual(analyst.report_for(conn, report_id)["export"], before["export"])
        revision, saved = server.lookup(sid)
        participant = server.public_state(sid, revision, saved)
        self.assertEqual(participant["report"]["id"], report_id)
        self.assertEqual(participant["reviewed_at"], timestamp)
        self.assertEqual(participant["review_status"], "needs_info")
        self.assertNotIn("Private follow-up", json.dumps(participant))
        self.assertNotIn(contact["email"], json.dumps(participant))

    def test_saved_assessment_uses_plain_language_without_rewriting_submitted_evidence(self):
        with patch.object(server.local_model, "URL", ""):
            state = server.new_session({"scenario": "fire-classroom-recap"})
            sid = state["id"]
            while question := state["question"]:
                state = server.mutate(sid, {"action": "answer", "revision": state["revision"],
                                            "id": question["id"], **question["example_answer"]})
            finished = server.mutate(sid, {"action": "finish", "revision": state["revision"]})
        current = finished["report"]
        self.assertEqual(current["decision"]["code"], "ai")
        self.assertIn("Test it with made-up examples", current["next_actions"][0]["action"])
        self.assertIn("reject a wrong result", current["next_actions"][1]["action"])
        self.assertIn("how long it takes today", current["next_actions"][2]["action"])

        _, saved = server.lookup(sid)
        self.assertEqual(server.report_export(saved), saved["export"])
        old_review = "Confirm the reviewer can see the source, stop an incorrect result and use the manual path."
        old_advice = ("Evaluate a bounded AI-assisted draft or interpretation. "
                      "Validate it against a reviewed reference set and keep approval with staff.")
        legacy = saved["report"]
        legacy["decision"]["recommendation"] = legacy["next_actions"][0]["action"] = old_advice
        legacy["next_actions"][1]["action"] = old_review
        legacy["workflow"]["Opportunity"] = old_advice
        legacy["evidence"][0]["note"] = old_advice
        saved["export"] = "Original download with " + old_review

        view = report_view(legacy)
        self.assertEqual(view["next_actions"], current["next_actions"])
        self.assertEqual(view["decision"], current["decision"])
        self.assertEqual(view["workflow"], legacy["workflow"])
        self.assertEqual(view["evidence"], legacy["evidence"])
        self.assertEqual(legacy["next_actions"][1]["action"], old_review)
        export = server.report_export(saved)
        self.assertIn(current["next_actions"][1]["action"], export)
        self.assertIn(old_advice, export)
        self.assertEqual(saved["export"], "Original download with " + old_review)
