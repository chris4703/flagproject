"""Deterministic decision rules and assessment rendering."""

from textwrap import shorten

from .interview import PROCESS_LABELS, VERSION, missing_process_evidence, note, pick, process_evidence
from .prior_answers import reused_example
from .questions import BANK

THRESHOLD = 6
CLASS_LABELS = {
    "existing": "Existing solution", "self_service": "Self-service", "automation": "Automation",
    "ai": "AI", "hybrid": "Hybrid", "discovery": "Further discovery",
}
BENEFIT_LABELS = {"low": "Low", "moderate": "Moderate", "high": "High", "unknown": "Not estimated"}
IT_LABELS = {0: "Department-led", 1: "IT advisory", 2: "IT delivery review", 3: "Mandatory governance review"}
RECOMMENDATIONS = {
    "existing": "Ask the person who manages the tool to check whether it already does what staff need. Find out what’s keeping staff from using it.",
    "self_service": "Check which approved tool the team can use. Try a small change the team can undo if it doesn’t work.",
    "automation": "Use made-up examples to test the steps that follow the same rules every time. Agree on what starts the task, what to check, and when staff should take over.",
    "ai": "Try using AI to create a draft or suggestion for one task. Test it with made-up examples and compare the results with what staff expect. Have staff approve each result before use.",
    "hybrid": "Try AI for the part that requires reading and interpreting information. Use clear rules for repeatable steps. Have staff approve the result and handle anything out of the ordinary.",
    "discovery": "Have the person responsible for the work meet with an IT analyst to answer the open questions before choosing a tool.",
}
EXISTING_RECOMMENDATIONS = {
    "training": "Ask the person who manages the tool to show staff how the feature works and share a short guide.",
    "access": "Ask the person who manages the tool to check that it meets the need and help staff request access through the usual process.",
    "config": "Ask the person who manages the tool to check its settings and test the feature with made-up records.",
}
ROUTES = {
    "existing": "Application owner / Service Desk", "self_service": "Department process owner",
    "automation": "Business Systems / automation team", "ai": "Business Systems / AI enablement",
    "hybrid": "Business Systems / automation and AI enablement",
    "discovery": "Business analyst and department process owner",
}
HOLD_FIRST_ACTION = (
    "Do not pilot with real data. IT triage first confirms the data owner and approved environment, "
    "then brings in the applicable reviewers."
)
PROCESS_OWNER_FOLLOWUP = {
    "owner": "Department process owner",
    "action": "Walk through the task with staff. Confirm how long it takes today, what result they need, and how they’ll tell if a change works.",
}
REVIEW_RESULT = (
    "Make sure the reviewer can see the original information, reject a wrong result, "
    "and do the work by hand if needed."
)
ASSIGN_REVIEWER = "Name who will check the result and when they must approve it before anyone can use it."
REVIEW_SYSTEM_ACCESS = (
    "Work out which tools need access, what information would move between them, and how to undo a change if something goes wrong."
)
REVIEW_IMPACT = "Agree on how staff will check the result and fix it if it’s wrong."
AI_RATIONALE = "AI could prepare a draft from the information staff described. A person would check it before anyone uses it."
HYBRID_RATIONALE = "AI could help interpret the information, and rules could handle the repeatable steps. Staff would check the result before it’s used."
TEST_AI_DRAFTS = (
    "Compare AI drafts with examples staff have checked. Make sure staff can correct or reject each draft."
)

# Match generated wording in older saved reports without changing their evidence or decisions.
LEGACY_WORDING = {
    "Ask the application owner to verify the reported feature in the current configuration and address the adoption barrier.": RECOMMENDATIONS["existing"],
    "Validate the approved team tool and test a small, reversible change in the team workspace.": RECOMMENDATIONS["self_service"],
    "Evaluate a rules-based workflow using synthetic examples. Confirm the trigger, checks and manual exception path.": RECOMMENDATIONS["automation"],
    "Evaluate a bounded AI-assisted draft or interpretation. Validate it against a reviewed reference set and keep approval with staff.": RECOMMENDATIONS["ai"],
    "Evaluate AI for the interpretation step and explicit rules for the predictable checks or routing. Keep exceptions and approval with staff.": RECOMMENDATIONS["hybrid"],
    "Ask the process owner and an IT analyst to resolve the open questions before selecting or building a solution.": RECOMMENDATIONS["discovery"],
    "Ask the application owner to demonstrate the reported feature and publish a short guide or training example.": EXISTING_RECOMMENDATIONS["training"],
    "Ask the application owner to verify the feature and route access through the approved access request process.": EXISTING_RECOMMENDATIONS["access"],
    "Ask the application owner to check configuration and test the existing feature using synthetic records.": EXISTING_RECOMMENDATIONS["config"],
    "Confirm the current steps, baseline effort, expected result and acceptance criteria with staff.": PROCESS_OWNER_FOLLOWUP["action"],
    "Confirm the reviewer can see the source, stop an incorrect result and use the manual path.": REVIEW_RESULT,
    "Define a named reviewer and a stop point before any generated or consequential output can be used.": ASSIGN_REVIEWER,
    "IT must map permissions, data flow and rollback.": REVIEW_SYSTEM_ACCESS,
    "Set an acceptance check and a way to correct a bad result.": REVIEW_IMPACT,
    "Staff described a checkable interpretation or draft with human review before use.": AI_RATIONALE,
    "Staff described a checkable interpretation and a fixed follow-on step, with human review before use.": HYBRID_RATIONALE,
    "Compare drafts against a reviewed synthetic reference set. A person must be able to correct or reject each draft.": TEST_AI_DRAFTS,
}


def report_view(report):
    """Present stored decisions with the current handoff format and wording."""
    def restate(item, *fields):
        return {**item, **{field: LEGACY_WORDING.get(item[field], item[field]) for field in fields}}

    view = {
        **report,
        "decision": restate(report["decision"], "rationale", "recommendation"),
        "checks": [restate(item, "reason") for item in report["checks"]],
        "next_actions": [restate(item, "action") for item in report["next_actions"]],
        "requirements": [LEGACY_WORDING.get(value, value) for value in report["requirements"]],
    }
    if "first_action" in report:
        return report if view == report else view
    decision = report["decision"]
    if not decision["hold"]:
        return {**view, "first_action": None}
    return {
        **view, "decision": {**view["decision"], "route": "IT triage"},
        "first_action": {"owner": "IT triage", "action": HOLD_FIRST_ACTION},
        "next_actions": [PROCESS_OWNER_FOLLOWUP],
    }


def label(answers, key):
    value = pick(answers, key)
    if key not in answers:
        return "Not collected on this branch"
    return next((item["label"] for item in BANK[key]["options"] if item["value"] == value), "Written response")


def suitability(answers):
    def contributions(spec):
        return [
            {"field": key, "points": weights[pick(answers, key)], "evidence": label(answers, key)}
            for key, weights in spec.items() if pick(answers, key) in weights
        ]

    automation = contributions({
        "rules": {"stable": 3, "mixed": 3}, "frequency": {"scheduled": 2, "event": 2},
        "input": {"structured": 2, "mixed": 1}, "output": {"fixed": 2, "both": 2},
        "exceptions": {"manageable": 1, "none": 1},
    })
    ai = contributions({
        "input": {"unstructured": 3, "mixed": 3}, "judgment": {"bounded": 3, "context": 2},
        "output": {"draft": 2, "both": 2}, "rules": {"mixed": 1, "judgment": 1},
        "exceptions": {"variable": 1},
    })
    return {key: {"total": sum(item["points"] for item in items), "items": items}
            for key, items in (("automation", automation), ("ai", ai))}


def governance(answers, proposed_ai):
    data = pick(answers, "data")
    systems = pick(answers, "systems")
    actions = pick(answers, "changes")
    impact = pick(answers, "impact")
    boundary = pick(answers, "boundary")
    owner = pick(answers, "owner")
    review = pick(answers, "review")
    tools = pick(answers, "tools")
    results = []

    def check(name, level, reason, reviewer, fields):
        results.append({"name": name, "level": level, "reason": reason, "reviewer": reviewer, "fields": fields})

    data_reason = {
        "none": "Routine administrative data reported.",
        "restricted": "Confirm who may see the private information, where it can be kept, and whether staff may use it this way.",
    }
    check("Data classification", "clear" if data == "none" else "hold",
          data_reason.get(data, "Confirm what information is involved, where staff may use it, and how it must be protected."),
          "Information Security / data steward", ["data"])
    if data in ("cjis", "both"):
        check("Potential CJIS applicability", "hold", "Validate CJI scope and agency requirements with the designated CJIS contact.",
              "City CJIS contact / Information Security", ["data"])
    if data in ("phi", "both"):
        check("Potential HIPAA applicability", "hold", "Confirm covered function, PHI/ePHI exposure, safeguards and any business associate obligations.",
              "City Privacy / Legal", ["data"])
    check("System access and transfers",
          "hold" if actions in ("privileged", "unknown", "") or systems in ("unknown", "") else
          "review" if actions == "write" or systems == "connected" else "clear",
          REVIEW_SYSTEM_ACCESS if actions in ("write", "privileged", "unknown", "") or systems in ("connected", "unknown", "") else
          "Existing access or manual transfer reported. Confirm the actual boundary during triage.",
          "Application owner / IT architecture", ["systems", "changes"])
    check("Operational consequence",
          "hold" if impact in ("serious", "unknown", "") or boundary != "admin" else "review" if impact == "operational" else "clear",
          "Keep live and consequential decision-making outside this exercise. Confirm impact and decision boundaries before proceeding."
          if impact in ("serious", "unknown", "") or boundary != "admin" else
          REVIEW_IMPACT,
          "Department process owner / governance lead", ["impact", "boundary"])
    check("Ownership and authorization", "clear" if owner == "confirmed" else "hold",
          "Ownership and authorization are staff-reported. Obtain confirmation before any pilot."
          if owner == "confirmed" else "Identify the process and data owners and confirm their authorization.",
          "Department lead / data owner", ["owner"])
    if proposed_ai or actions in ("write", "privileged") or impact in ("operational", "serious") or boundary != "admin":
        check("Human oversight", "review" if review == "prior" else "hold",
              REVIEW_RESULT if review == "prior" else ASSIGN_REVIEWER,
              "Department process owner", ["review", "impact", "boundary"])
    if tools == "external":
        check("External service or vendor", "hold", "Review allowed uses, data flow, contracts and retention before sharing any data.",
              "Procurement / Information Security / Privacy", ["tools"])
    return results


def classify(answers, scores):
    existing = pick(answers, "existing")
    rules = pick(answers, "rules")
    output = pick(answers, "output")
    review = pick(answers, "review")
    if pick(answers, "boundary") == "live":
        return "discovery", "The workflow was reported to affect a live or consequential decision. Limit follow-up to administrative support."
    if existing == "yes":
        return "existing", f"Staff reported that a current feature covers the need. Adoption barrier: {label(answers, 'barrier')}."
    if missing_process_evidence(answers):
        return "discovery", "The rules, inputs or desired result need clarification before a technology fit can be established."
    auto = scores["automation"]["total"] >= THRESHOLD and rules in ("stable", "mixed") and output in ("fixed", "both")
    ai = (
        scores["ai"]["total"] >= THRESHOLD and output in ("draft", "both")
        and pick(answers, "judgment") == "bounded" and review == "prior"
    )
    if ai and auto:
        return "hybrid", HYBRID_RATIONALE
    if ai:
        return "ai", AI_RATIONALE
    if auto and output == "both":
        return "discovery", "The fixed step may be feasible. The proposed interpretation still needs a checkable reference and prior human review."
    if auto:
        same_team = (
            pick(answers, "tools") == "approved" and pick(answers, "systems") == "same"
            and pick(answers, "changes") == "read" and pick(answers, "people") == "team"
            and pick(answers, "data") in ("none", "restricted") and pick(answers, "impact") == "minor"
            and pick(answers, "boundary") == "admin" and pick(answers, "owner") == "confirmed"
            and existing == "no"
        )
        if same_team:
            return "self_service", "Staff could make this small change in a tool their team already uses. Check the review requirements before trying it."
        return "automation", "Staff reported repeatable rules and a predictable result. A team-managed path was not established."
    return "discovery", "The evidence does not yet support a repeatable rules-based solution or a checkable, human-reviewed AI draft."


def assess(answers, history, report_id, generated_at, department, scenario, expected_benefit="unknown"):
    scores = suitability(answers)
    classification, rationale = classify(answers, scores)
    proposed_ai = pick(answers, "output") in ("draft", "both")
    checks = governance(answers, proposed_ai)
    holds = [item for item in checks if item["level"] == "hold"]

    risk = "High" if (
        pick(answers, "data") in ("cjis", "phi", "both", "restricted")
        or pick(answers, "impact") == "serious" or pick(answers, "boundary") == "live"
        or pick(answers, "changes") == "privileged"
    ) else "Elevated" if holds or any(item["level"] == "review" for item in checks) or proposed_ai else "Low"

    technical = (
        pick(answers, "systems") == "connected" or pick(answers, "changes") in ("write", "privileged")
        or pick(answers, "people") in ("multiple", "external")
    )
    tier = 3 if holds else 2 if technical else 1 if (
        classification not in ("existing", "self_service") or pick(answers, "barrier") in ("config", "access", "unknown")
        or risk != "Low"
    ) else 0
    advice = RECOMMENDATIONS[classification]
    barrier = pick(answers, "barrier")
    if classification == "existing":
        advice = EXISTING_RECOMMENDATIONS.get(barrier, advice)
    if holds:
        route = "IT triage"
        next_actions = []
    else:
        route = "IT technical triage → " + ROUTES[classification] if tier == 2 else ROUTES[classification]
        next_actions = [{"owner": route, "action": advice}]
        next_actions.extend({"owner": item["reviewer"], "action": item["reason"]}
                            for item in checks if item["level"] == "review")
    next_actions.append(PROCESS_OWNER_FOLLOWUP)

    unknowns = [BANK[key]["title"] for key in answers
                if pick(answers, key) in ("unknown", "unclear", "partial") and key != "existing"]
    if pick(answers, "existing") in ("unknown", "partial"):
        unknowns.append("Can an existing feature or configuration cover the remaining need?")
    if "frequency" not in answers or not note(answers, "frequency"):
        unknowns.append("What are the baseline volume, hands-on time and rework?")
    if classification in ("automation", "self_service") and "exceptions" not in answers:
        unknowns.append("Which exceptions should staff continue to handle manually?")
    example_from_earlier = reused_example(answers)
    example = note(answers, "example") or (example_from_earlier["excerpt"] if example_from_earlier else "")
    if classification in ("automation", "ai", "hybrid", "self_service") and not example:
        unknowns.append("What synthetic inputs and expected results should IT use for acceptance testing?")

    requirements = ["Confirm a documented acceptance example and record who can approve the result."]
    if "output" in answers:
        result = note(answers, "output") or label(answers, "output")
        requirements.append("Validate the proposed result with the process owner. " + result.rstrip(".") + ".")
    if example:
        source = f" from question {example_from_earlier['source_number']}" if example_from_earlier else ""
        requirements.append(f"Run the staff-provided example{source} as an acceptance test. {example.rstrip('.')}.")
    if classification in ("automation", "hybrid", "self_service"):
        requirements.append("Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.")
    if proposed_ai:
        requirements.append(TEST_AI_DRAFTS)
    if technical:
        requirements.append("Specify least-privilege access, integration boundaries, failure handling and rollback before testing.")

    model_count = sum(bool(entry.get("model_choice")) for entry in history)
    evidence = [{"id": entry["id"], "question": entry.get("title", BANK[entry["id"]]["title"]),
                 "answer": label(answers, entry["id"]) if BANK[entry["id"]]["options"] else "",
                 "note": note(answers, entry["id"]),
                 "source_number": answers[entry["id"]].get("source_number")} for entry in history]
    current_steps = note(answers, "process")
    if known := process_evidence(answers):
        lines = [f"From the opening answer ({topic.lower()}) — “{known[key]}”"
                 for key, topic in PROCESS_LABELS.items() if key in known]
        if current_steps:
            lines.append(f"Follow-up answer — {current_steps}")
        current_steps = "\n".join(lines)
    return {
        "id": report_id, "generated_at": generated_at, "version": VERSION,
        "department": department, "scenario": scenario, "question_count": len(history), "model_count": model_count,
        "expected_benefit": expected_benefit,
        "decision": {"code": classification, "label": CLASS_LABELS[classification], "rationale": rationale,
                     "risk": risk, "tier": tier, "it": IT_LABELS[tier], "hold": bool(holds), "route": route,
                     "recommendation": advice},
        "workflow": {
            "Opportunity": note(answers, "goal"), "Current steps": current_steps,
            "Volume and effort": note(answers, "frequency") or label(answers, "frequency"),
            "Tools and handoffs": note(answers, "systems") or label(answers, "systems"),
            "Inputs": note(answers, "input") or label(answers, "input"),
            "Expected result": note(answers, "output") or label(answers, "output"),
            "Exceptions": note(answers, "exceptions") or label(answers, "exceptions"),
            "Ownership": note(answers, "owner") or label(answers, "owner"),
            "People affected": note(answers, "people") or label(answers, "people"),
        },
        "scores": scores, "checks": checks, "requirements": requirements, "unknowns": unknowns,
        "assumptions": [
            "The answers and estimates are staff-reported and require validation before implementation.",
            "Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.",
            "Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.",
        ],
        "first_action": {"owner": "IT triage", "action": HOLD_FIRST_ACTION} if holds else None,
        "next_actions": next_actions, "evidence": evidence,
    }


def markdown(report):
    report = report_view(report)

    def plain(value):
        # Keep staff text in a paragraph and escape Markdown/HTML delimiters.
        escaped = " ".join(value.split())
        for token in ("\\", "`", "*", "_", "[", "]", "<", ">", "#", "|", "~"):
            escaped = escaped.replace(token, "\\" + token)
        return escaped

    interview = {item["id"]: (number, item) for number, item in enumerate(report["evidence"], 1)}

    def reference(field, response=False):
        if field not in interview:
            return f"“{plain(BANK[field]['title'])}” · No answer recorded."
        number, item = interview[field]
        question = f"Q{number} “{plain(item['question'])}”"
        if not response:
            return question
        excerpt = shorten(item["note"], width=115, placeholder="…")
        context = " — ".join(plain(value) for value in (item["answer"], excerpt) if value)
        return f"{question} · {context}" if context else question

    d = report["decision"]
    lines = [
        "# Public Safety Opportunity Assessment", "",
        f"**{plain(report['department'])} · {plain(report['scenario'])}**", "",
        f"Assessment ID {report['id']} · {report['generated_at']} · Rules {report['version']}",
        f"{report['question_count']} answers · {report['model_count']} local AI follow-up selections", "",
    ]
    if first := report["first_action"]:
        lines.extend(["## Governance hold at submission", "",
                      f"**First action · {first['owner']}**", "", first["action"], ""])
    lines.extend([
        "## Triage recommendation", "",
        f"- **Solution fit:** {d['label']}",
        f"- **Expected benefit (staff estimate):** {BENEFIT_LABELS[report.get('expected_benefit', 'unknown')]}",
        f"- **Risk:** {d['risk']}",
        f"- **IT involvement:** Tier {d['tier']} — {d['it']}",
        f"- **Readiness at submission:** {'Governance review required' if d['hold'] else 'Ready for triage'}",
        f"- **Proposed route:** {d['route']}", "",
        plain(d["rationale"]), "", f"**Technical recommendation:** {d['recommendation']}",
        "", "## Current workflow", "",
    ])
    lines.extend(f"- **{field}:** {plain(value)}" for field, value in report["workflow"].items())
    lines.extend(["", "## Proposed requirements", ""])
    lines.extend(f"- {plain(value)}" for value in report["requirements"])
    lines.extend(["", "## Risk and governance", ""])
    review_roles = {}
    for check in report["checks"]:
        lines.append(f"- **{check['name']} · {check['level'].title()}:** {check['reason']}")
        lines.extend(f"  - {reference(field, response=True)}" for field in check["fields"])
        if check["level"] != "clear":
            for role in check["reviewer"].split(" / "):
                review_roles.setdefault(role, []).append(check["name"])
    if review_roles:
        lines.extend(["", "**Reviewers and checks**", ""])
        lines.extend(f"- **{role}** · {', '.join(checks)}" for role, checks in review_roles.items())
    lines.extend(["", "## Screening scores", "",
                  f"Scores of {THRESHOLD} or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.", ""])
    for key, score in report["scores"].items():
        score_label = "AI" if key == "ai" else "Automation"
        lines.append(f"- **{score_label} screening score · {score['total']}/10**")
        lines.extend(f"  - +{item['points']} {plain(item['evidence'])} · {reference(item['field'])}" for item in score["items"])
    lines.extend(["", "## Assumptions and open questions", ""])
    lines.extend(f"- {plain(value)}" for value in report["assumptions"] + report["unknowns"])
    lines.extend(["", "## Next steps", ""])
    lines.extend(f"{i}. **{item['owner']}** — {item['action']}" for i, item in enumerate(report["next_actions"], 1))
    lines.extend(["", "## Interview record", ""])
    for number, item in enumerate(report["evidence"], 1):
        response = " — ".join(plain(x) for x in (item["answer"], item["note"]) if x) or "No example provided."
        source = f" *(Detail from Q{item['source_number']}.)*" if item.get("source_number") else ""
        lines.append(f"- **Q{number} · {plain(item['question'])}** {response}{source}")
    return "\n".join(lines) + "\n"
