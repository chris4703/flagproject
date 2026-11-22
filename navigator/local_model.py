"""Bounded local model assistance for intake and analyst review."""

import json
import os
from pathlib import Path
import re
from threading import BoundedSemaphore
import urllib.request

from .interview import MAX_MODEL_PICKS, PROCESS_QUESTIONS, next_options, note
from .questions import BANK, FOLLOWUPS

URL = os.getenv("NAV_MODEL_URL", "").rstrip("/")
MODEL = "flagstaff-local"
INPUTS = Path(__file__).resolve().parents[1] / "inputs"
INTERVIEW_PROMPT = (INPUTS / "interviewer.md").read_text()
SUMMARY_PROMPT = (INPUTS / "summary.md").read_text()
PROCESS_PROMPT = (INPUTS / "process.md").read_text()
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
SUMMARY_SLOT = BoundedSemaphore(1)
EMAIL = re.compile(r"[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+")
TECHNIQUES = (
    re.compile(r"\b(?:AI|agents?|artificial intelligence|machine learning)\b", re.I),
    re.compile(r"\bautomat\w*\b", re.I),
)
PROPOSED_WORK = re.compile(
    r"\b(?:want|wish|hope|would|could|should|will|ideally|propos\w*)\b", re.I
)
CURRENT_WORK = re.compile(r"\b(?:today|currently|right now|at present|as it stands)\b", re.I)
PROCESS_SIGNALS = {
    "start": re.compile(
        r"\b(?:every|each|when|whenever|after|once|daily|weekly|monthly|nightly|morning|"
        r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
        r"start\w*|begin\w*|arriv\w*|receiv\w*|email\w*|call\w*|trigger\w*)\b",
        re.I,
    ),
    "finish": re.compile(
        r"\b(?:send\w*|sent|share\w*|email\w*|hand(?:s|ed|ing)? (?:off|over|it|the)|"
        r"give\w*|deliver\w*|submit\w*|notify\w*|notified|post\w*|save\w*|fil(?:e[ds]?|ing)|"
        r"upload\w*|finish\w*|(?:is|are) (?:done|complete)|sign off|signed off|"
        r"pass(?:es|ed)?|goes to|put\w*|place\w*|leave\w*)\b",
        re.I,
    ),
}


def ready():
    if not URL:
        return False
    try:
        with OPENER.open(f"{URL}/health", timeout=1) as response:
            return response.status == 200
    except OSError:
        return False


def complete(prompt, evidence, max_tokens, timeout):
    body = {
        "model": MODEL, "temperature": 0, "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(evidence)},
        ],
    }
    request = urllib.request.Request(
        f"{URL}/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with OPENER.open(request, timeout=timeout) as response:
            reply = json.loads(response.read(32000))
        return json.loads(reply["choices"][0]["message"]["content"])
    except (OSError, ValueError, KeyError, TypeError, IndexError):
        return None


def propose(state):
    candidates = next_options(state["answers"])
    if not URL or len(candidates) < 2 or any(k not in FOLLOWUPS for k in candidates):
        return None
    if sum(bool(event.get("model_choice")) for event in state["history"]) >= MAX_MODEL_PICKS:
        return None
    evidence = {
        key: {"choice": item["value"], "note": item["note"][:220]}
        for key, item in state["answers"].items()
        if key in {"goal", "process", "rules", "input", "output", "exceptions", "judgment", "example"}
    }
    output = complete(INTERVIEW_PROMPT, {
        "candidates": [{"id": key, "topic": BANK[key]["title"]} for key in candidates],
        "staff_excerpts": evidence,
    }, max_tokens=45, timeout=6)
    if isinstance(output, dict) and set(output) == {"question_id"} and output["question_id"] in candidates:
        return output["question_id"]
    return None


def process_clues(text):
    if not URL or len(text.split()) < 8:
        return {}
    source = EMAIL.sub("[email omitted]", text)
    current = []
    after_proposal = False
    for clause in re.split(r"(?<=[.!?;])\s+|[\r\n]+", source):
        if PROPOSED_WORK.search(clause):
            after_proposal = True
            continue
        if after_proposal and not CURRENT_WORK.search(clause):
            continue
        current.append(" ".join(clause.split()))
        after_proposal = False
    if not any(current):
        return {}
    output = complete(PROCESS_PROMPT, {"answer": " ".join(current)}, max_tokens=190, timeout=6)
    if not isinstance(output, dict) or set(output) != PROCESS_QUESTIONS.keys():
        return {}
    evidence = {}
    for field in PROCESS_QUESTIONS:
        excerpt = output[field]
        if not isinstance(excerpt, str) or not 5 <= len(excerpt.strip()) <= 200:
            continue
        excerpt = " ".join(excerpt.split()).rstrip(".;,")
        if "[email omitted]" in excerpt:
            continue
        signal = PROCESS_SIGNALS.get(field)
        if signal and not signal.search(excerpt):
            continue
        for clause in current:
            match = re.search(r"(?<!\w)" + re.escape(excerpt) + r"(?!\w)", clause, re.I)
            if match and match.group() not in evidence.values():
                evidence[field] = match.group()
                break
    return evidence


def summarize_request(answers):
    if not URL or not note(answers, "goal"):
        return None
    fields = {"requested_outcome": "goal", "desired_result": "output"}
    evidence = {
        label: EMAIL.sub("[email omitted]", note(answers, key))[:300]
        for label, key in fields.items() if note(answers, key)
    }
    if not SUMMARY_SLOT.acquire(blocking=False):
        return None
    try:
        output = complete(SUMMARY_PROMPT, evidence, max_tokens=90, timeout=9)
    finally:
        SUMMARY_SLOT.release()
    if not isinstance(output, dict) or set(output) != {"summary"} or not isinstance(output["summary"], str):
        return None
    summary = output["summary"].strip()
    if (not summary.startswith("Staff want ") or not 20 <= len(summary) <= 300 or len(summary.split()) > 42
            or re.search(r"[@<>\r\n]|https?://", summary, re.I)):
        return None
    excerpts = " ".join(evidence.values())
    if any(technique.search(summary) and not technique.search(excerpts) for technique in TECHNIQUES):
        return None
    return re.sub(r"\bfollow-up queue\b", "follow-up list", summary, flags=re.I)
