"""HTTP interface and persistence for the local exercise."""

from contextlib import closing
from datetime import datetime, timedelta, timezone
from getpass import getpass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import json
import logging
import mimetypes
import os
from pathlib import Path
import re
import secrets
import sqlite3
import sys
from urllib.parse import parse_qsl, urlsplit

from navigator import analyst, local_model
from navigator.assessment import BENEFIT_LABELS, assess, label, markdown, report_view
from navigator.interview import VERSION, completion_reason, next_question, validate_answer
from navigator.prior_answers import collect_context, reused_example
from navigator.questions import BANK

ROOT = Path(__file__).resolve().parent
DB = Path(os.getenv("NAV_DB", str(ROOT / ".state" / "navigator.sqlite3"))).resolve()
SCENARIOS = json.loads((ROOT / "inputs" / "scenarios.json").read_text())
DEPARTMENTS = ["Police", "Fire", "Emergency Communications"]
ARIZONA = timezone(timedelta(hours=-7))
ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"}
PUBLIC_HOST = os.getenv("NAV_PUBLIC_HOST", "").strip().lower()
if PUBLIC_HOST:
    ALLOWED_HOSTS.add(PUBLIC_HOST)
SESSION_PATH = re.compile(r"/api/sessions/([0-9a-f]{48})(?:/(download))?")
EMAIL_FORMAT = re.compile(r"[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+")
ANALYST_REVIEW = re.compile(r"/api/analyst/reports/([0-9A-F]{12})/review")
ANALYST_SUMMARY = re.compile(r"/api/analyst/reports/([0-9A-F]{12})/summary")
ANALYST_REPORT = re.compile(r"/api/analyst/reports/([0-9A-F]{12})(?:/(download))?")
STATIC = {
    "/": "index.html", "/app.js": "app.js", "/styles.css": "styles.css", "/staff.css": "staff.css",
    "/analyst": "analyst.html", "/analyst/": "analyst.html",
    "/analyst.js": "analyst.js", "/analyst.css": "analyst.css",
}


class RequestError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def db():
    conn = sqlite3.connect(DB, timeout=8)
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with db() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""CREATE TABLE IF NOT EXISTS interviews (
            id TEXT PRIMARY KEY, revision INTEGER NOT NULL, state TEXT NOT NULL
        )""")
        analyst.initialize(conn)


def follow_up_contact(payload, scenario):
    incoming = payload.get("contact")
    if incoming is None and scenario:
        return "Practice participant", f"{scenario}@example.invalid"
    if not isinstance(incoming, dict):
        raise RequestError(400, "Enter your name and email for IT follow-up.")
    name = incoming.get("name")
    email = incoming.get("email")
    if not isinstance(name, str) or not isinstance(email, str):
        raise RequestError(400, "Enter your name and email for IT follow-up.")
    if any(ord(char) < 32 or ord(char) == 127 for char in name + email):
        raise RequestError(400, "Enter a name and email on one line.")
    name, email = name.strip(), email.strip()
    if not name or len(name) > 120:
        raise RequestError(400, "Enter a name of up to 120 characters.")
    if len(email) > 254 or not EMAIL_FORMAT.fullmatch(email):
        raise RequestError(400, "Enter a valid email address.")
    return name, email


def new_session(payload):
    scenario = payload.get("scenario", "")
    department = payload.get("department", "")
    if not isinstance(scenario, str) or not isinstance(department, str):
        raise RequestError(400, "Choose a department or practice scenario.")
    if scenario:
        if scenario not in SCENARIOS:
            raise RequestError(400, "Choose one of the listed practice scenarios.")
        department = SCENARIOS[scenario]["department"]
    if department not in DEPARTMENTS:
        raise RequestError(400, "Choose a department to continue.")
    name, email = follow_up_contact(payload, scenario)
    sid = secrets.token_hex(24)
    state = {"department": department, "scenario": scenario, "history": [], "answers": {},
             "report": None, "has_contact": True}
    with db() as conn:
        conn.execute("INSERT INTO interviews VALUES (?, ?, ?)", (sid, 0, json.dumps(state)))
        conn.execute("INSERT INTO interview_contacts VALUES (?, ?, ?)", (sid, name, email))
    return public_state(sid, 0, state)


def lookup(sid):
    with db() as conn:
        row = conn.execute("SELECT revision, state FROM interviews WHERE id = ?", (sid,)).fetchone()
    if row is None:
        raise RequestError(404, "This interview is unavailable. Start a new one.")
    return row[0], json.loads(row[1])


def save(sid, revision, state):
    with db() as conn:
        result = conn.execute("UPDATE interviews SET revision = ?, state = ? WHERE id = ? AND revision = ?",
                              (revision + 1, json.dumps(state), sid, revision))
        if result.rowcount != 1:
            raise RequestError(409, "That interview changed in another request. Reload and try again.")
    return public_state(sid, revision + 1, state)


def public_state(sid, revision, state):
    scenario = SCENARIOS.get(state["scenario"], {})
    question = None if state["report"] else next_question(state)
    review = analyst.review_state(state) if state["report"] else None
    if question and question["id"] in scenario.get("answers", {}):
        value, note = scenario["answers"][question["id"]]
        question.update({"example_answer": {"value": value, "note": note}})
    evidence = [{
        "id": item["id"],
        "title": item.get("title", BANK[item["id"]]["title"]),
        "answer": label(state["answers"], item["id"]) if BANK[item["id"]]["options"] else "",
        "value": state["answers"][item["id"]]["value"],
        "note": state["answers"][item["id"]]["note"],
        "source_number": state["answers"][item["id"]].get("source_number"),
    } for item in state["history"]]
    return {
        "id": sid, "revision": revision, "department": state["department"],
        "scenario": scenario.get("title", ""), "question": question, "evidence": evidence,
        "review_reason": completion_reason(state["answers"]) if question is None and state["report"] is None else "",
        "reused_example": reused_example(state["answers"]) if question is None and state["report"] is None else None,
        "report": report_view(state["report"]) if state["report"] else None,
        "has_contact": state.get("has_contact", False),
        "reviewed_at": state.get("reviewed_at"),
        "review_status": review["status"] if review else None,
        "governance_status": review["governance"] if review else None,
        "model_choices": sum(bool(item.get("model_choice")) for item in state["history"]),
    }


def report_export(state):
    report = state["report"]
    view = report_view(report)
    return state["export"] if view is report else markdown(view)


def mutate(sid, payload):
    revision, state = lookup(sid)
    if type(payload.get("revision")) is not int or payload["revision"] != revision:
        raise RequestError(409, "That interview has changed. Reload and try again.")
    if state["report"]:
        raise RequestError(409, "That assessment is complete. Start a new interview to make changes.")
    action = payload.get("action")
    active = next_question(state)
    if action == "answer":
        if not active or active["id"] != payload.get("id"):
            raise RequestError(409, "That question is no longer active.")
        answer = validate_answer(active, payload)
        if active["id"] == "goal":
            if clues := local_model.process_clues(answer["note"]):
                answer["process_evidence"] = clues
        new_text = answer["note"]
        if detail := active.get("earlier_detail"):
            excerpt = detail["excerpt"]
            if new_text == excerpt or new_text.startswith(excerpt + "\n"):
                answer["source_number"] = detail["source_number"]
                new_text = new_text[len(excerpt):].lstrip()
        answer["prior_context"] = collect_context(new_text, state["answers"].keys() | {active["id"]})
        state["answers"][active["id"]] = answer
        event = {"id": active["id"], "title": active["title"]}
        state["history"].append(event)
        selected = local_model.propose(state)
        if selected:
            event["model_choice"] = selected
    elif action in ("back", "revise"):
        history = state["history"]
        if not history:
            raise RequestError(400, "There are no earlier answers to change.")
        index = len(history) - 1 if action == "back" else next(
            (i for i, item in enumerate(history) if item["id"] == payload.get("id")), None
        )
        if index is None:
            raise RequestError(400, "Choose an answered question to change.")
        revised_id = history[index]["id"]
        draft = {key: state["answers"][revised_id][key] for key in ("value", "note")}
        for entry in history[index:]:
            del state["answers"][entry["id"]]
        del history[index:]
        updated = save(sid, revision, state)
        if updated["question"] and updated["question"]["id"] == revised_id:
            updated["draft"] = draft
        return updated
    elif action == "finish":
        if active:
            raise RequestError(400, "Complete the remaining questions before creating the assessment.")
        expected_benefit = payload.get("expected_benefit", "unknown")
        if not isinstance(expected_benefit, str) or expected_benefit not in BENEFIT_LABELS:
            raise RequestError(400, "Choose a valid estimate of expected benefit.")
        generated_at = datetime.now(ARIZONA).isoformat(timespec="seconds")
        scenario = SCENARIOS.get(state["scenario"], {}).get("title", "Custom workflow")
        state["report"] = assess(state["answers"], state["history"], secrets.token_hex(6).upper(),
                                 generated_at, state["department"], scenario, expected_benefit)
        state["export"] = markdown(state["report"])
    else:
        raise RequestError(400, "Choose a supported interview action.")
    return save(sid, revision, state)


class Handler(BaseHTTPRequestHandler):
    server_version = "Navigator/1.0"
    sys_version = ""

    def setup(self):
        super().setup()
        self.connection.settimeout(12)

    def log_message(self, fmt, *args):
        # Session tokens and workflow details stay out of logs.
        return

    def format_response(self, status, content, content_type, filename=None, cookie=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(content)

    def json_response(self, status, data, cookie=None):
        self.format_response(status, json.dumps(data).encode("utf-8"),
                             "application/json; charset=utf-8", cookie=cookie)

    def json_payload(self):
        if self.headers.get_content_type() != "application/json":
            raise RequestError(415, "Send actions as JSON.")
        length = int(self.headers.get("Content-Length", "0"))
        if not 0 < length <= 8192:
            raise RequestError(413, "That request is too long or empty.")
        payload = json.loads(self.rfile.read(length))
        if not isinstance(payload, dict):
            raise RequestError(400, "Send a single action.")
        return payload

    def check_host(self):
        host = self.headers.get("Host", "")
        hostname = urlsplit(f"//{host}").hostname
        if hostname not in ALLOWED_HOSTS:
            raise RequestError(403, "This address is not enabled for Flagstaff WIP.")
        scheme = "https" if hostname == PUBLIC_HOST else "http"
        origin = self.headers.get("Origin")
        if origin and origin.lower() != f"{scheme}://{host}".lower():
            raise RequestError(403, "Open Flagstaff WIP directly in its own tab.")

    def login_address(self, https):
        address = self.headers.get("CF-Connecting-IP", "") if https else ""
        try:
            return str(ipaddress.ip_address(address))
        except ValueError:
            return self.client_address[0]

    def handle_analyst(self, method, path, query):
        https = urlsplit(f"//{self.headers['Host']}").hostname == PUBLIC_HOST
        token = analyst.get_token(self.headers.get("Cookie", ""))
        with closing(db()) as conn, conn:
            if method == "POST":
                if not self.headers.get("Origin"):
                    raise RequestError(403, "Open the analyst dashboard directly in your browser.")
                payload = self.json_payload()
                if path == "/api/analyst/login":
                    if not analyst.rate_allows_attempt(self.login_address(https)):
                        raise RequestError(429, "Too many sign-in attempts. Try again in a few minutes.")
                    if not analyst.PASSWORD_SLOTS.acquire(blocking=False):
                        raise RequestError(429, "Sign-in is busy. Try again shortly.")
                    try:
                        conn.execute("BEGIN IMMEDIATE")
                        if not conn.execute("SELECT 1 FROM analyst_credentials WHERE id=1").fetchone():
                            raise RequestError(503, "Analyst access has not been configured on this copy.")
                        if not analyst.authenticate(conn, payload.get("username"), payload.get("password")):
                            raise RequestError(401, "The username or password is incorrect.")
                        analyst.end_session(conn, token)
                        token = analyst.issue_session(conn)
                        conn.commit()
                    finally:
                        analyst.PASSWORD_SLOTS.release()
                    self.json_response(200, {"signed_in": True}, analyst.session_cookie(token, https))
                elif path == "/api/analyst/logout":
                    analyst.end_session(conn, token)
                    conn.commit()
                    self.json_response(200, {"signed_in": False}, analyst.session_cookie("", https))
                elif match := ANALYST_REVIEW.fullmatch(path):
                    if not analyst.authorized(conn, token):
                        raise RequestError(401, "Sign in to review submissions.")
                    now = datetime.now(ARIZONA).isoformat(timespec="seconds")
                    conn.execute("BEGIN IMMEDIATE")
                    try:
                        review = analyst.update_review(conn, match.group(1), now, payload)
                    except analyst.ReviewChanged as error:
                        raise RequestError(409, str(error)) from error
                    if review is None:
                        raise RequestError(404, "That submission is unavailable.")
                    conn.commit()
                    self.json_response(200, review)
                elif match := ANALYST_SUMMARY.fullmatch(path):
                    if not analyst.authorized(conn, token):
                        raise RequestError(401, "Sign in to view submissions.")
                    report_id = match.group(1)
                    saved = analyst.report_for(conn, report_id)
                    if saved is None:
                        raise RequestError(404, "That submission is unavailable.")
                    if not saved.get("analyst_request_summary"):
                        summary = local_model.summarize_request(saved.get("answers", {}))
                        if summary:
                            saved["analyst_request_summary"] = analyst.cache_request_summary(conn, report_id, summary)
                            conn.commit()
                    self.json_response(200, analyst.request_summary(saved))
                else:
                    raise RequestError(404, "That analyst action is unavailable.")
                return

            if not analyst.authorized(conn, token):
                raise RequestError(401, "Sign in to view submissions.")
            if path in ("/api/analyst/overview", "/api/analyst/export.csv"):
                params = dict(parse_qsl(query, max_num_fields=16))
                filters, page = analyst.accepted_filters(params, DEPARTMENTS)
                today = datetime.now(ARIZONA).date()
                rows = analyst.completed(conn, filters, today)
                if path.endswith(".csv"):
                    self.format_response(200, analyst.export_csv(rows), "text/csv; charset=utf-8",
                                         "navigator-submissions.csv")
                else:
                    self.json_response(200, analyst.overview(rows, page, DEPARTMENTS, params.get("sort", "")))
                return
            match = ANALYST_REPORT.fullmatch(path)
            if match:
                report_id, download = match.groups()
                saved = analyst.report_for(conn, report_id)
                if saved is None:
                    raise RequestError(404, "That submission is unavailable.")
                if download:
                    self.format_response(200, report_export(saved).encode("utf-8"), "text/markdown; charset=utf-8",
                                         f"opportunity-{report_id}.md")
                else:
                    self.json_response(200, {
                        **report_view(saved["report"]), "contact": saved["contact"], "reviewed_at": saved.get("reviewed_at"),
                        "review": analyst.review_state(saved), "review_options": analyst.REVIEW_STATUS,
                        "request_summary": analyst.request_summary(saved),
                    })
                return
            raise RequestError(404, "That analyst view is unavailable.")

    def handle_app(self, method):
        self.check_host()
        target = urlsplit(self.path)
        path = target.path
        if path.startswith("/api/analyst/"):
            self.handle_analyst(method, path, target.query)
            return
        match = SESSION_PATH.fullmatch(path)
        if method == "GET":
            if path == "/favicon.ico":
                self.format_response(204, b"", "image/x-icon")
            elif path in STATIC:
                file = ROOT / "web" / STATIC[path]
                content_type = mimetypes.guess_type(file)[0] or "application/octet-stream"
                self.format_response(200, file.read_bytes(), content_type)
            elif path == "/api/health":
                self.json_response(200, {"status": "ok", "model_ready": local_model.ready(), "version": VERSION})
            elif path == "/api/options":
                scenarios = [{"id": key, **{k: v for k, v in item.items() if k != "answers"}}
                             for key, item in SCENARIOS.items()]
                self.json_response(200, {"departments": DEPARTMENTS, "scenarios": scenarios, "benefits": BENEFIT_LABELS})
            elif match:
                sid, download = match.groups()
                revision, state = lookup(sid)
                if not download:
                    self.json_response(200, public_state(sid, revision, state))
                elif state["report"]:
                    self.format_response(200, report_export(state).encode("utf-8"), "text/markdown; charset=utf-8",
                                         f"opportunity-{state['report']['id']}.md")
                else:
                    raise RequestError(409, "Create the assessment before downloading it.")
            else:
                raise RequestError(404, "That page is unavailable.")
            return

        if path != "/api/sessions" and (not match or match.group(2)):
            raise RequestError(404, "That action is unavailable.")
        payload = self.json_payload()
        result = new_session(payload) if path == "/api/sessions" else mutate(match.group(1), payload)
        self.json_response(201 if path == "/api/sessions" else 200, result)

    def dispatch(self, method):
        try:
            self.handle_app(method)
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            return
        except RequestError as error:
            self.json_response(error.status, {"error": str(error)})
        except (ValueError, UnicodeError) as error:
            message = str(error) if type(error) is ValueError and not str(error).startswith("invalid literal") else "Check the answer and try again."
            self.json_response(HTTPStatus.BAD_REQUEST, {"error": message})
        except Exception as error:
            logging.error("Request failed: %s", type(error).__name__)
            self.json_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Flagstaff WIP could not save that action. Try again."})

    def do_GET(self):
        self.dispatch("GET")

    def do_POST(self):
        self.dispatch("POST")


if __name__ == "__main__":
    initialize()
    if sys.argv[1:] == ["--set-analyst-password"]:
        if sys.stdin.isatty():
            password = getpass("New analyst password: ")
            if password != getpass("Confirm analyst password: "):
                raise SystemExit("Passwords did not match.")
        else:
            password = sys.stdin.readline().rstrip("\r\n")
        with closing(db()) as conn, conn:
            analyst.set_password(conn, password)
        print("Analyst password configured. Prior analyst sessions signed out.")
        raise SystemExit(0)
    address = os.getenv("NAV_BIND", "127.0.0.1"), int(os.getenv("NAV_PORT", "8878"))
    with ThreadingHTTPServer(address, Handler) as server:
        print(f"Navigator listening on http://{address[0]}:{address[1]}", flush=True)
        server.serve_forever()
