import csv
from datetime import date
import io
import json
import sqlite3
import unittest
from unittest.mock import patch

from navigator import analyst, local_model
from navigator.assessment import assess


class AnalystTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.addCleanup(self.conn.close)
        self.conn.execute("CREATE TABLE interviews (id TEXT PRIMARY KEY, revision INTEGER, state TEXT)")
        analyst.initialize(self.conn)
        self.departments = ["Police", "Fire", "Emergency Communications"]

    def add(self, report_id, department, scenario="", impact="minor", benefit=None, solution="existing", effort_high=False):
        picked = {"goal": "", "impact": impact, "systems": "connected" if effort_high else "same",
                  "changes": "write" if effort_high else "read", "people": "multiple" if effort_high else "team"}
        answers = {key: {"value": value, "note": ""} for key, value in picked.items()}
        answers["goal"]["note"] = " =Example of a workbook title"
        report = assess(answers, [], report_id, "2026-11-19T12:00:00-07:00", department, scenario)
        report["decision"].update(code=solution, hold=effort_high)
        if benefit is None:
            report.pop("expected_benefit")
        else:
            report["expected_benefit"] = benefit
        state = {"report": report, "answers": answers, "scenario": scenario, "export": "# Completed report"}
        self.conn.execute("INSERT INTO interviews VALUES (?, 1, ?)", (report_id, json.dumps(state)))

    def rows(self, **params):
        filters, _ = analyst.accepted_filters(params, self.departments)
        return list(analyst.completed(self.conn, filters, date(2026, 11, 19)))

    def test_dashboard_counts_and_filters_preserve_independent_dimensions(self):
        self.add("AA01", "Police", scenario="Practice", benefit=None)
        self.add("AA02", "Emergency Communications", impact="serious", benefit="high",
                 solution="hybrid", effort_high=True)
        self.conn.execute("INSERT INTO interviews VALUES ('draft', 1, '{\"report\":null}')")
        data = analyst.overview(self.rows(), 1, self.departments)
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["holds"], 1)
        self.assertEqual(data["counts"]["benefit"]["unknown"], 1)
        self.assertEqual(data["cross_tab"]["hybrid"]["serious"], 1)
        self.assertEqual(data["benefit_effort"]["high"]["high"], 1)
        matched = self.rows(source="custom", department="Emergency Communications", benefit="high", status="hold")
        self.assertEqual([row["id"] for row in matched], ["AA02"])
        routed = self.rows(risk=matched[0]["risk"], tier=str(matched[0]["tier"]), solution="hybrid")
        self.assertEqual([row["id"] for row in routed], ["AA02"])
        self.assertEqual(analyst.report_for(self.conn, "AA02")["export"], "# Completed report")
        self.assertIsNone(analyst.report_for(self.conn, "draft"))

    def test_csv_escapes_spreadsheet_formulas(self):
        self.add("AA03", "Fire")
        columns = list(csv.DictReader(io.StringIO(analyst.export_csv(self.rows()).decode())))
        self.assertEqual(len(columns), 1)
        self.assertEqual(columns[0]["Workflow"], "' =Example of a workbook title")

    def test_submission_sort_orders_all_matches_before_pagination(self):
        self.add("AA01", "Police", benefit="high")
        self.add("AA02", "Fire", benefit="low")
        self.add("AA03", "Fire", benefit="moderate")
        self.add("AA04", "Fire")
        rows = self.rows()
        with patch.object(analyst, "PAGE_SIZE", 2):
            original = analyst.overview(rows, 1, self.departments)
            self.assertEqual([row["id"] for row in original["records"]], ["AA04", "AA03"])
            for sort, expected in (
                ("benefit", ["AA02", "AA03", "AA01", "AA04"]),
                ("-benefit", ["AA01", "AA03", "AA02", "AA04"]),
                ("department", ["AA04", "AA03", "AA02", "AA01"]),
            ):
                with self.subTest(sort=sort):
                    first, second = (analyst.overview(iter(rows), page, self.departments, sort) for page in (1, 2))
                    self.assertEqual([row["id"] for row in first["records"] + second["records"]], expected)
                    self.assertEqual(first["counts"], original["counts"])
        with self.assertRaises(ValueError):
            analyst.overview(rows, 1, self.departments, "unsupported")

    def test_request_summary_uses_intake_and_keeps_review_and_export(self):
        self.add("AA04", "Emergency Communications", effort_high=True, solution="hybrid")
        saved = analyst.report_for(self.conn, "AA04")
        saved["answers"]["review"] = {"value": "prior", "note": ""}
        self.conn.execute("UPDATE interviews SET state=? WHERE id='AA04'", (json.dumps(saved),))
        preview = analyst.request_summary(saved)
        self.assertEqual(preview["source"], "submitted_answers")
        self.assertIn("workbook title", preview["text"])
        self.assertIn("after someone approves", preview["context"])

        analyst.update_review(self.conn, "AA04", "2026-11-19T13:00:00-07:00", {})
        generated = "Staff want a work list for their team."
        self.assertEqual(analyst.cache_request_summary(self.conn, "AA04", generated), generated)
        self.assertEqual(analyst.cache_request_summary(self.conn, "AA04", "Later text"), generated)
        updated = analyst.report_for(self.conn, "AA04")
        self.assertEqual(analyst.request_summary(updated), {**preview, "text": generated, "source": "local_ai"})
        self.assertEqual(updated["report"], saved["report"])
        self.assertEqual(updated["export"], saved["export"])
        self.assertEqual(updated["reviewed_at"], "2026-11-19T13:00:00-07:00")

    def test_review_and_clearance_are_independent(self):
        self.add("AA05", "Emergency Communications", impact="serious", effort_high=True, solution="hybrid")
        original = analyst.report_for(self.conn, "AA05")
        timestamp = "2026-11-19T13:00:00-07:00"
        self.assertEqual(analyst.review_state(original)["status"], "awaiting")
        legacy = analyst.review_state({**original, "reviewed_at": timestamp})
        self.assertEqual((legacy["status"], legacy["governance"]), ("reviewed", "hold"))
        reviewed = analyst.update_review(self.conn, "AA05", timestamp, {"status": "reviewed", "revision": 0})
        self.assertEqual((reviewed["status"], reviewed["governance"]), ("reviewed", "hold"))
        self.assertEqual(len(self.rows(review="reviewed", status="hold")), 1)
        approval = {"status": "approved", "revision": 1}
        with self.assertRaises(ValueError):
            analyst.update_review(self.conn, "AA05", timestamp, approval)
        with self.assertRaises(ValueError):
            analyst.update_review(self.conn, "AA05", timestamp, {**approval, "clearance_confirmed": True, "note": "  "})
        approved = analyst.update_review(self.conn, "AA05", timestamp, {
            **approval, "clearance_confirmed": True, "note": "Clearance reference QA-1",
        })
        self.assertEqual((approved["status"], approved["governance"]), ("approved", "cleared"))
        self.assertEqual(self.rows(status="hold"), [])
        with self.assertRaises(analyst.ReviewChanged):
            analyst.update_review(self.conn, "AA05", timestamp, {"status": "closed", "revision": 1})
        closed = analyst.update_review(self.conn, "AA05", timestamp, {"status": "closed", "revision": 2})
        self.assertEqual((closed["status"], closed["governance"]), ("closed", "closed"))
        saved = analyst.report_for(self.conn, "AA05")
        self.assertEqual(saved["report"], original["report"])
        self.assertEqual(saved["export"], original["export"])
        self.assertEqual(saved["it_review_history"][1]["note"], "Clearance reference QA-1")

    def test_model_summary_limits_evidence_and_rejects_unsupported_technology(self):
        answers = {
            "goal": {"note": "List overdue equipment loans and ask sample@example.invalid."},
            "output": {"note": "A list by room."},
            "process": {"note": "A separate detail."},
        }
        with patch.object(local_model, "URL", "http://localhost"), patch.object(local_model, "complete") as model:
            model.return_value = {"summary": "Staff want an AI agent to list overdue equipment loans."}
            self.assertIsNone(local_model.summarize_request(answers))
            evidence = model.call_args.args[1]
            self.assertEqual(set(evidence), {"requested_outcome", "desired_result"})
            self.assertNotIn("sample@example.invalid", evidence["requested_outcome"])
            model.return_value = {"summary": "Staff want a list of overdue equipment loans by room."}
            self.assertEqual(local_model.summarize_request(answers), model.return_value["summary"])
        with patch.object(local_model, "URL", ""):
            self.assertIsNone(local_model.summarize_request(answers))

    def test_sessions_expire_and_password_rotation_revokes_access(self):
        first = "synthetic browser login phrase one"
        second = "synthetic browser login phrase two"
        analyst.set_password(self.conn, first)
        self.assertTrue(analyst.authenticate(self.conn, "analyst", first))
        self.assertFalse(analyst.authenticate(self.conn, "something else", first))
        token = analyst.issue_session(self.conn)
        self.assertTrue(analyst.authorized(self.conn, token))
        self.conn.execute("UPDATE analyst_sessions SET expires=0")
        self.assertFalse(analyst.authorized(self.conn, token))
        another = analyst.issue_session(self.conn)
        analyst.set_password(self.conn, second)
        self.assertFalse(analyst.authorized(self.conn, another))
        self.assertFalse(analyst.authenticate(self.conn, "analyst", first))
        self.assertTrue(analyst.authenticate(self.conn, "analyst", second))
