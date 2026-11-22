"""Adaptive navigation. Policy and report generation live in assessment.py."""

from .prior_answers import earlier_detail, reused_example
from .questions import BANK, MANDATORY

VERSION = "1.8.0"
MAX_MODEL_PICKS = 2
PROCESS_QUESTIONS = {
    "start": ("What starts the task?", "Tell us when this work starts or what prompts someone to begin it."),
    "steps": ("What steps do you take?", "Walk us through the main steps staff take today."),
    "finish": ("How do you know the task is done?", "Tell us what happens to the result today, such as who gets it or where it goes."),
}
PROCESS_LABELS = {"start": "Start", "steps": "Current steps", "finish": "Finish"}


def pick(answers, key):
    return answers.get(key, {}).get("value", "")


def note(answers, key):
    return answers.get(key, {}).get("note", "")


def process_evidence(answers):
    return answers.get("goal", {}).get("process_evidence", {})


def missing_process_evidence(answers):
    return (
        pick(answers, "rules") == "unclear"
        or pick(answers, "input") == "unknown"
        or pick(answers, "output") == "unknown"
    )


def routine_path(answers):
    """The remaining exception and example questions cannot change a routine route."""
    return (
        pick(answers, "rules") == "stable"
        and pick(answers, "input") == "structured"
        and pick(answers, "output") in ("", "fixed")
        and pick(answers, "data") == "none"
        and pick(answers, "systems") in ("same", "manual")
        and pick(answers, "changes") == "read"
        and pick(answers, "impact") == "minor"
        and pick(answers, "owner") == "confirmed"
        and pick(answers, "boundary") == "admin"
        and pick(answers, "people") in ("", "team")
        and pick(answers, "tools") in ("", "approved", "none")
    )


def completion_reason(answers):
    if pick(answers, "boundary") == "live":
        return "IT has enough information to review which decisions this change could affect."
    if pick(answers, "existing") == "yes":
        return "Your answers point to an existing feature, and the required checks are complete."
    if missing_process_evidence(answers):
        return "You’ve answered the required questions. The assessment lists what IT still needs to check."
    if routine_path(answers):
        return "IT has enough to assess this routine workflow, and the required checks are complete."
    return "IT has enough information to review your request."


def needs_review(answers):
    return (
        pick(answers, "data") not in ("", "none")
        or pick(answers, "changes") in ("write", "privileged", "unknown")
        or pick(answers, "impact") not in ("", "minor")
        or pick(answers, "boundary") not in ("", "admin")
        or pick(answers, "input") in ("mixed", "unstructured")
        or pick(answers, "output") in ("draft", "both")
        or pick(answers, "tools") == "external"
    )


def branch_followups(answers):
    pending = []
    interpret = pick(answers, "input") in ("mixed", "unstructured")
    rules = pick(answers, "rules")
    if interpret or rules in ("mixed", "judgment") or pick(answers, "output") in ("draft", "both"):
        pending.extend(("judgment", "output", "example", "exceptions"))
    elif rules == "stable":
        pending.extend(("exceptions", "output"))
    else:
        pending.extend(("example", "output", "exceptions"))
    if pick(answers, "exceptions") in ("variable", "unknown"):
        pending.append("example")
    pending.append("people")
    covered = answers.keys() | ({"example"} if reused_example(answers) else set())
    return [key for key in dict.fromkeys(pending) if key not in covered]


def next_options(answers):
    for key in ("goal", "process", "existing"):
        if key == "process" and PROCESS_QUESTIONS.keys() <= process_evidence(answers).keys():
            continue
        if key not in answers:
            return [key]
    if pick(answers, "existing") == "yes" and "barrier" not in answers:
        return ["barrier"]
    for key in MANDATORY:
        if key not in answers:
            return [key]
    if pick(answers, "existing") == "yes" or pick(answers, "boundary") == "live" or missing_process_evidence(answers):
        return ["review"] if needs_review(answers) and "review" not in answers else []

    for key in ("frequency", "rules", "input"):
        if key not in answers:
            return [key]

    if routine_path(answers):
        for key in ("output", "people", "tools"):
            if key not in answers:
                return [key]
        return []

    pending = branch_followups(answers)
    if pending:
        return pending

    if "tools" not in answers:
        return ["tools"]
    return ["review"] if needs_review(answers) and "review" not in answers else []


def next_question(state):
    answers = state["answers"]
    candidates = next_options(answers)
    if not candidates:
        return None
    previous = state["history"][-1] if state["history"] else {}
    selected = previous.get("model_choice")
    question_id = selected if selected in candidates else candidates[0]
    question = {
        **BANK[question_id],
        "selection": "local AI" if selected == question_id else "interview rules",
        "alternatives": len(candidates),
    }
    if question_id in MANDATORY or question_id == "review":
        question["hint"] += " If you’re unsure, choose “I’m not sure.” IT can follow up."
    if known := process_evidence(answers):
        if question_id == "process":
            missing = [key for key in PROCESS_QUESTIONS if key not in known]
            if len(missing) == 1:
                question["title"], question["hint"] = PROCESS_QUESTIONS[missing[0]]
            else:
                question.update(
                    title="What else happens in this task?",
                    hint=" ".join(PROCESS_QUESTIONS[key][0] for key in missing),
                )
            question["process_context"] = [known[key] for key in PROCESS_QUESTIONS if key in known]
            question["placeholder"] = ""
        elif question_id == "existing" and "process" not in answers:
            question["process_reused"] = True
    if question["options"] and (detail := earlier_detail(answers, question_id)):
        question["earlier_detail"] = detail
    return question


def validate_answer(question, payload):
    value = payload.get("value", "")
    raw = payload.get("note", "")
    if not isinstance(value, str) or not isinstance(raw, str):
        raise ValueError("Use a choice or a short written answer.")
    if question["options"] and value not in {item["value"] for item in question["options"]}:
        raise ValueError("Choose the answer that fits best.")
    if not question["options"] and value:
        raise ValueError("Use the written answer field.")
    if question["note"] == "required" and len(raw.strip()) < 8:
        raise ValueError("Add a short sentence about the task.")
    if len(raw) > 900:
        raise ValueError("Keep each note to 900 characters or fewer.")
    return {"value": value, "note": raw.strip()}
