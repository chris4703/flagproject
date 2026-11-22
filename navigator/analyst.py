"""Analyst login, portfolio reporting and IT review."""

from collections import Counter, deque
import csv
from datetime import timedelta
import hashlib
import hmac
from http.cookies import CookieError, SimpleCookie
import io
import json
import secrets
from threading import BoundedSemaphore, Lock
from textwrap import shorten
import time

from .assessment import BENEFIT_LABELS, CLASS_LABELS, IT_LABELS
from .interview import note, pick

USERNAME = "analyst"
COOKIE = "navigator_analyst"
SESSION_AGE = 8 * 60 * 60
PASSWORD_ROUNDS = 600_000
PAGE_SIZE = 20
IMPACTS = {"minor": "Low", "operational": "Moderate", "serious": "High", "unknown": "Unknown"}
EFFORTS = {"low": "Low", "medium": "Moderate", "high": "High", "unscoped": "Unscoped"}
SOURCES = {"custom": "Custom interviews", "scenario": "Practice scenarios"}
RISK_LEVELS = ("Low", "Elevated", "High")
REVIEW_STATUS = {
    "awaiting": "Awaiting review",
    "reviewed": "Reviewed",
    "needs_info": "Needs information",
    "approved": "Approved for next step",
    "closed": "Closed",
}
GOVERNANCE_STATUS = {
    "hold": "Governance review required",
    "ready": "No governance hold",
    "cleared": "Clearance recorded",
    "closed": "Closed with flags",
}
TEXT_SORT_COLUMNS = {"title", "department", "solution", "status", "review"}
LEVEL_SORT_COLUMNS = {
    "benefit": ("low", "moderate", "high"),
    "impact": ("minor", "operational", "serious"),
    "effort": ("low", "medium", "high"),
}
REPORT_ID = "$.report.id"
REPORT_DATE = "$.report.generated_at"
COMPLETED = "json_type(state, '$.report') = 'object'"
EXISTING_SUPPORT = {
    "training": "Staff say they need guidance to use a feature they already have.",
    "config": "Staff say a feature they already have needs to be set up.",
    "access": "Staff say they need access to a feature they already have.",
}
RATE_LOCK = Lock()
PASSWORD_SLOTS = BoundedSemaphore(3)
attempts = {}


class ReviewChanged(Exception):
    pass


def initialize(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS analyst_credentials (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            salt BLOB NOT NULL, password_hash BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analyst_sessions (
            token_hash TEXT PRIMARY KEY, expires INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS interview_contacts (
            interview_id TEXT PRIMARY KEY REFERENCES interviews(id) ON DELETE CASCADE,
            display_name TEXT NOT NULL, email TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS analyst_reports_by_date
          ON interviews(json_extract(state, '$.report.generated_at'))
          WHERE json_type(state, '$.report') = 'object';
        CREATE INDEX IF NOT EXISTS analyst_reports_by_id
          ON interviews(json_extract(state, '$.report.id'))
          WHERE json_type(state, '$.report') = 'object';
    """)


def derive_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ROUNDS)


def set_password(conn, password):
    if not 16 <= len(password) <= 128:
        raise ValueError("Use a password with 16 to 128 characters.")
    salt = secrets.token_bytes(24)
    digest = derive_password(password, salt)
    conn.execute("INSERT OR REPLACE INTO analyst_credentials VALUES (1, ?, ?)", (salt, digest))
    conn.execute("DELETE FROM analyst_sessions")


def rate_allows_attempt(address):
    now = time.monotonic()
    with RATE_LOCK:
        expired = [key for key, window in attempts.items() if now - window[-1] > 300]
        for key in expired:
            del attempts[key]
        if address not in attempts and len(attempts) >= 512:
            return False
        window = attempts.setdefault(address, deque())
        while window and now - window[0] > 300:
            window.popleft()
        if len(window) >= 8:
            return False
        window.append(now)
        return True


def authenticate(conn, username, password):
    credentials = conn.execute("SELECT salt, password_hash FROM analyst_credentials WHERE id=1").fetchone()
    if credentials is None:
        return False
    if not isinstance(username, str) or not isinstance(password, str) or not 1 <= len(password) <= 128:
        return False
    salt, expected = credentials
    matched = hmac.compare_digest(derive_password(password, salt), expected)
    return matched and username == USERNAME


def token_digest(token):
    return hashlib.sha256(token.encode("ascii")).hexdigest()


def issue_session(conn):
    token = secrets.token_urlsafe(32)
    now = int(time.time())
    conn.execute("DELETE FROM analyst_sessions WHERE expires <= ?", (now,))
    conn.execute("INSERT INTO analyst_sessions VALUES (?, ?)", (token_digest(token), now + SESSION_AGE))
    return token


def get_token(header):
    cookies = SimpleCookie()
    try:
        cookies.load(header)
    except CookieError:
        return ""
    item = cookies.get(COOKIE)
    if item is None or len(item.value) != 43:
        return ""
    value = item.value
    return value if value.isascii() and value.replace("-", "").replace("_", "").isalnum() else ""


def authorized(conn, token):
    return bool(token and conn.execute(
        "SELECT 1 FROM analyst_sessions WHERE token_hash=? AND expires>?",
        (token_digest(token), int(time.time())),
    ).fetchone())


def end_session(conn, token):
    if token:
        conn.execute("DELETE FROM analyst_sessions WHERE token_hash=?", (token_digest(token),))


def session_cookie(token, https):
    max_age = SESSION_AGE if token else 0
    secure = "; Secure" if https else ""
    return f"{COOKIE}={token}; Max-Age={max_age}; HttpOnly; SameSite=Strict; Path=/api/analyst{secure}"


def effort_for(report, answers):
    solution = report["decision"]["code"]
    if solution == "discovery":
        return "unscoped"
    if solution == "existing":
        return "low"
    systems = pick(answers, "systems")
    access = pick(answers, "changes")
    teams = pick(answers, "people")
    if systems in ("unknown", "") or access in ("unknown", ""):
        return "unscoped"
    if access == "privileged" or (systems == "connected" and (access == "write" or teams in ("multiple", "external"))):
        return "high"
    if solution in ("automation", "ai", "hybrid") or systems == "connected" or access == "write" or teams in ("multiple", "external"):
        return "medium"
    return "low"


def accepted_filters(params, departments):
    allowed = {
        "days": ("7", "30", "90"), "department": departments, "source": SOURCES,
        "solution": CLASS_LABELS, "impact": IMPACTS, "benefit": BENEFIT_LABELS,
        "effort": EFFORTS, "status": GOVERNANCE_STATUS, "review": REVIEW_STATUS,
        "risk": RISK_LEVELS, "tier": tuple(map(str, IT_LABELS)),
    }
    result = {}
    for key, choices in allowed.items():
        value = params.get(key, "")
        if value and value not in choices:
            raise ValueError(f"Choose a valid {key} filter.")
        result[key] = value
    raw_page = params.get("page", "1")
    if not raw_page.isascii() or not raw_page.isdigit() or not 1 <= int(raw_page) <= 100000:
        raise ValueError("Choose a valid page.")
    return result, int(raw_page)


def review_state(saved):
    history = saved.get("it_review_history", [])
    reviewed_at = saved.get("reviewed_at")
    latest = history[-1] if history else {
        "status": "reviewed" if reviewed_at else "awaiting",
        "note": "",
        "updated_at": reviewed_at,
    }
    governance = "ready"
    if saved["report"]["decision"]["hold"]:
        governance = {"approved": "cleared", "closed": "closed"}.get(latest["status"], "hold")
    return {
        **latest, "revision": len(history), "reviewed_at": reviewed_at,
        "governance": governance, "governance_label": GOVERNANCE_STATUS[governance],
    }


def completed(conn, filters, today):
    sql = f"SELECT state FROM interviews WHERE {COMPLETED}"
    args = []
    if filters["days"]:
        start = today - timedelta(days=int(filters["days"]) - 1)
        sql += f" AND json_extract(state, '{REPORT_DATE}') >= ?"
        args.append(start.isoformat())
    sql += f" ORDER BY json_extract(state, '{REPORT_DATE}') DESC, json_extract(state, '{REPORT_ID}') DESC"
    for (raw,) in conn.execute(sql, args):
        state = json.loads(raw)
        report = state["report"]
        decision = report["decision"]
        answers = state.get("answers", {})
        impact = pick(answers, "impact")
        source = "scenario" if state.get("scenario") else "custom"
        review = review_state(state)
        row = {
            "id": report["id"], "date": report["generated_at"],
            "title": report["scenario"] if source == "scenario" else (note(answers, "goal") or "Custom workflow"),
            "source": source, "department": report["department"],
            "solution": decision["code"], "impact": impact if impact in IMPACTS else "unknown",
            "benefit": report.get("expected_benefit", "unknown"), "effort": effort_for(report, answers),
            "risk": decision["risk"], "tier": decision["tier"],
            "status": review["governance"], "questions": report["question_count"],
            "review": review["status"],
            "hold_reasons": [item["name"] for item in report["checks"]
                             if item["level"] == "hold" and review["governance"] == "hold"],
        }
        if all(not value or value == str(row[key]) for key, value in filters.items() if key != "days"):
            yield row


def sort_submissions(rows, sort):
    column = sort.removeprefix("-")
    descending = sort.startswith("-")
    if column in LEVEL_SORT_COLUMNS:
        ranks = {value: i for i, value in enumerate(LEVEL_SORT_COLUMNS[column])}
        direction = -1 if descending else 1

        def level_key(row):
            rank = ranks.get(row[column])
            return rank is None, (rank or 0) * direction

        return sorted(rows, key=level_key)
    if column in TEXT_SORT_COLUMNS:
        labels = {"solution": CLASS_LABELS, "status": GOVERNANCE_STATUS, "review": REVIEW_STATUS}.get(column)

        def text_key(row):
            value = labels[row[column]] if labels else row[column]
            return value.strip().casefold()

        return sorted(rows, key=text_key, reverse=descending)
    raise ValueError("Choose a valid submission sort.")


def overview(rows, page, departments, sort=""):
    dimensions = {
        "solution": CLASS_LABELS, "impact": IMPACTS, "benefit": BENEFIT_LABELS,
        "effort": EFFORTS, "risk": RISK_LEVELS,
        "tier": IT_LABELS, "department": departments, "source": SOURCES,
    }
    counts = {field: dict.fromkeys(options, 0) for field, options in dimensions.items()}
    cross_tab = {solution: dict.fromkeys(IMPACTS, 0) for solution in CLASS_LABELS}
    benefit_effort = {benefit: dict.fromkeys(EFFORTS, 0) for benefit in BENEFIT_LABELS}
    holds = Counter()
    total = hold_count = question_total = 0
    listed = []
    start = (page - 1) * PAGE_SIZE
    for row in rows:
        if sort or start <= total < start + PAGE_SIZE:
            listed.append(row)
        total += 1
        hold_count += row["status"] == "hold"
        question_total += row["questions"]
        for field, tally in counts.items():
            value = row[field]
            if value in tally:
                tally[value] += 1
        cross_tab[row["solution"]][row["impact"]] += 1
        benefit_effort[row["benefit"]][row["effort"]] += 1
        holds.update(row["hold_reasons"])
    if sort:
        listed = sort_submissions(listed, sort)[start:start + PAGE_SIZE]
    return {
        "total": total, "holds": hold_count, "avg_questions": round(question_total / total, 1) if total else None,
        "counts": counts, "cross_tab": cross_tab, "benefit_effort": benefit_effort, "hold_reasons": holds.most_common(),
        "records": [{**row, "title": " ".join(row["title"].split())[:120]} for row in listed],
        "sort": sort, "page": page, "pages": max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE),
        "labels": {"solution": CLASS_LABELS, "impact": IMPACTS, "benefit": BENEFIT_LABELS,
                   "effort": EFFORTS, "source": SOURCES, "tier": IT_LABELS, "review": REVIEW_STATUS,
                   "governance": GOVERNANCE_STATUS,
                   "risk": {label: label for label in RISK_LEVELS},
                   "department": {label: label for label in departments}},
        "departments": departments,
    }


def report_for(conn, report_id):
    row = conn.execute(
        f"""SELECT state, display_name, email FROM interviews
            LEFT JOIN interview_contacts ON interviews.id = interview_contacts.interview_id
            WHERE {COMPLETED} AND json_extract(state, '{REPORT_ID}') = ?""",
        (report_id,),
    ).fetchone()
    if row is None:
        return None
    raw, name, email = row
    state = json.loads(raw)
    state["contact"] = {"name": name, "email": email} if email else None
    return state


def request_summary(saved):
    answers = saved.get("answers", {})
    context = ""
    prior_review = pick(answers, "review") == "prior"
    if pick(answers, "systems") == "connected":
        context = "They also want the tools to share information."
        if prior_review:
            context = "They want to connect the tools and have a person check the result before it is used."
            if pick(answers, "changes") == "write":
                context = "They want the tools to share updates after someone approves them."
    elif pick(answers, "existing") == "yes":
        context = EXISTING_SUPPORT.get(pick(answers, "barrier"), "")
    if prior_review and not context:
        context = "Staff say a person would review the result before it is used."
    cached = saved.get("analyst_request_summary")
    if cached:
        return {"text": cached, "context": context, "source": "local_ai"}
    goal = note(answers, "goal") or saved["report"]["workflow"].get("Opportunity", "")
    return {
        "text": shorten(goal, width=285, placeholder="…") or "No request description was recorded.",
        "context": context, "source": "submitted_answers",
    }


def cache_request_summary(conn, report_id, summary):
    conn.execute(
        f"""UPDATE interviews
            SET state=json_set(state, '$.analyst_request_summary', ?)
            WHERE {COMPLETED} AND json_extract(state, '{REPORT_ID}') = ?
              AND json_extract(state, '$.analyst_request_summary') IS NULL""",
        (summary, report_id),
    )
    row = conn.execute(
        f"""SELECT json_extract(state, '$.analyst_request_summary') FROM interviews
            WHERE {COMPLETED} AND json_extract(state, '{REPORT_ID}') = ?""",
        (report_id,),
    ).fetchone()
    return row[0] if row else None


def update_review(conn, report_id, timestamp, payload):
    """Record a disposition while the caller holds the write transaction."""
    row = conn.execute(
        f"""SELECT id, state FROM interviews WHERE {COMPLETED} AND json_extract(state, '{REPORT_ID}') = ?""",
        (report_id,),
    ).fetchone()
    if row is None:
        return None
    interview_id, raw = row
    saved = json.loads(raw)
    current = review_state(saved)
    target = payload.get("status", "reviewed")
    if "status" not in payload:
        if current["status"] != "awaiting":
            return current
    elif type(payload.get("revision")) is not int or payload["revision"] != current["revision"]:
        raise ReviewChanged("This review changed in another tab. Reopen the assessment and try again.")
    if not isinstance(target, str) or target not in REVIEW_STATUS:
        raise ValueError("Choose a valid IT review status.")
    note = payload.get("note", "")
    if not isinstance(note, str) or len(note) > 500:
        raise ValueError("Keep the review note to 500 characters or fewer.")
    note = note.strip()
    if target == current["status"] and note == current["note"]:
        return current
    if target == "approved" and saved["report"]["decision"]["hold"]:
        if payload.get("clearance_confirmed") is not True or not note:
            raise ValueError("Confirm governance clearance and enter a reference or note before approving the next step.")
    history = saved.setdefault("it_review_history", [])
    history.append({"status": target, "note": note, "updated_at": timestamp})
    if not saved.get("reviewed_at") and target != "awaiting":
        saved["reviewed_at"] = timestamp
    conn.execute("""
        UPDATE interviews
        SET state=json_set(state, '$.it_review_history', json(?), '$.reviewed_at', ?), revision=revision+1
        WHERE id=?
        """, (json.dumps(history), saved.get("reviewed_at"), interview_id))
    return review_state(saved)


def safe_csv_value(value):
    if isinstance(value, str) and value.lstrip(" \t\r\n").startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def export_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(("Report ID", "Completed (Arizona time)", "Workflow", "Department", "Source",
                     "Solution classification", "Expected benefit", "Impact if wrong", "Indicative effort", "Risk",
                     "IT tier", "Governance status", "IT review status", "Questions"))
    for row in rows:
        writer.writerow((row["id"], row["date"], safe_csv_value(row["title"]), row["department"],
                         SOURCES[row["source"]], CLASS_LABELS[row["solution"]], BENEFIT_LABELS[row["benefit"]], IMPACTS[row["impact"]],
                         EFFORTS[row["effort"]], row["risk"], row["tier"], GOVERNANCE_STATUS[row["status"]],
                         REVIEW_STATUS[row["review"]], row["questions"]))
    return output.getvalue().encode("utf-8")
