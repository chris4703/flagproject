import unittest

from navigator.assessment import assess, classify, suitability
from navigator.interview import next_options
from navigator.questions import BANK, MANDATORY


def answers(**kwargs):
    return {key: {"value": value, "note": ""} for key, value in kwargs.items()}


CORE = answers(goal="", process="", existing="no", data="none", systems="same", changes="read",
               impact="minor", owner="confirmed", boundary="admin")
RULES = answers(frequency="scheduled", rules="stable", input="structured", output="fixed",
                exceptions="manageable", people="team", tools="approved")
AI = answers(frequency="event", rules="judgment", input="unstructured", output="draft", judgment="bounded",
             review="prior", exceptions="variable", people="team", tools="none")
HYBRID = {**AI, **answers(rules="mixed", output="both", input="mixed", exceptions="manageable")}


class InterviewTests(unittest.TestCase):
    def test_twenty_question_bank_and_early_exit(self):
        self.assertEqual(len(BANK), 20)
        result = {**CORE, **answers(existing="yes", barrier="training")}
        for key in MANDATORY:
            self.assertEqual(next_options({k: v for k, v in result.items() if k != key}), [key])
        self.assertEqual(next_options(result), [])
        self.assertEqual(next_options({**result, **answers(changes="privileged")}), ["review"])
        self.assertEqual(next_options({**CORE, **answers(boundary="live")}), ["review"])

    def test_branch_candidates(self):
        self.assertEqual(next_options({**CORE, **answers(frequency="scheduled", rules="stable", input="structured",
                                                         systems="connected")})[:2],
                         ["exceptions", "output"])
        self.assertEqual(next_options({**CORE, **answers(frequency="scheduled", rules="mixed", input="mixed")})[0],
                         "judgment")

    def test_routine_work_stops_after_fifteen_answers(self):
        fixture = {**CORE, **RULES}
        collected = {}
        while candidates := next_options(collected):
            key = candidates[0]
            self.assertNotIn(key, collected)
            collected[key] = fixture[key]

        self.assertEqual(len(collected), 15)
        self.assertTrue(set(MANDATORY) <= collected.keys())
        self.assertFalse({"exceptions", "example", "judgment"} & collected.keys())
        report = assess(collected, [], "TEST", "time", "Fire", "Fictional")
        self.assertEqual(report["decision"]["code"], "self_service")
        self.assertIn("Which exceptions should staff continue to handle manually?", report["unknowns"])

    def test_missing_evidence_stops_only_after_required_checks(self):
        fixture = {**CORE, **answers(frequency="event", rules="unclear")}
        self.assertEqual(next_options(fixture), [])
        self.assertEqual(classify(fixture, suitability(fixture))[0], "discovery")
        for key in MANDATORY:
            self.assertEqual(next_options({k: v for k, v in fixture.items() if k != key}), [key])

        fixture.update(answers(data="cjis", impact="operational"))
        self.assertEqual(next_options(fixture), ["review"])
        fixture.update(answers(review="prior"))
        self.assertEqual(next_options(fixture), [])
        report = assess(fixture, [], "TEST", "time", "Police", "Fictional")
        self.assertEqual(report["decision"]["code"], "discovery")
        self.assertTrue(report["decision"]["hold"])

    def test_new_answers_can_expand_routine_path(self):
        fixture = {**CORE, **{k: v for k, v in RULES.items() if k not in ("exceptions", "tools")}}
        self.assertEqual(next_options(fixture), ["tools"])
        self.assertIn("exceptions", next_options({**fixture, **answers(tools="external")}))
        self.assertIn("judgment", next_options({**fixture, **answers(output="draft")}))
        self.assertEqual(next_options({**fixture, **answers(output="unknown")}), [])

    def test_all_six_dispositions(self):
        cases = [
            ({**CORE, **answers(existing="yes", barrier="training")}, "existing"),
            ({**CORE, **RULES}, "self_service"),
            ({**CORE, **RULES, **answers(tools="unknown")}, "automation"),
            ({**CORE, **AI}, "ai"),
            ({**CORE, **HYBRID}, "hybrid"),
            ({**CORE, **HYBRID, **answers(review="after")}, "discovery"),
        ]
        for fixture, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(classify(fixture, suitability(fixture))[0], expected)

    def test_risk_forces_hold_independent_of_solution_fit(self):
        fixture = {**CORE, **RULES, **answers(existing="yes", barrier="training", data="both", owner="partial")}
        report = assess(fixture, [], "TEST", "time", "Fire", "Fictional")
        self.assertEqual(report["decision"]["code"], "existing")
        self.assertEqual(report["decision"]["risk"], "High")
        self.assertEqual(report["decision"]["tier"], 3)
        self.assertTrue(report["decision"]["hold"])
        self.assertEqual({"Potential CJIS applicability", "Potential HIPAA applicability"},
                         {c["name"] for c in report["checks"] if "applicability" in c["name"]})

    def test_private_staff_information_requires_review_even_for_self_service(self):
        fixture = {**CORE, **RULES, **answers(data="restricted", review="prior")}
        report = assess(fixture, [], "TEST", "time", "Fire", "Fictional")
        decision = report["decision"]
        self.assertEqual((decision["code"], decision["risk"], decision["tier"]), ("self_service", "High", 3))
        self.assertTrue(decision["hold"])
        self.assertEqual(decision["route"], "IT triage")
        for data in ("cjis", "phi", "both", "unknown"):
            with self.subTest(data=data):
                self.assertNotEqual(classify({**fixture, **answers(data=data)}, suitability(fixture))[0],
                                    "self_service")

    def test_consequential_work_cannot_advance(self):
        fixture = {**CORE, **HYBRID, **answers(boundary="live", impact="serious")}
        report = assess(fixture, [], "TEST", "time", "Fire", "Fictional")
        self.assertEqual(report["decision"]["code"], "discovery")
        self.assertTrue(report["decision"]["hold"])

    def test_unknown_mandatory_values_keep_assessment_on_hold(self):
        for key in MANDATORY:
            with self.subTest(key=key):
                fixture = {**CORE, **RULES, **answers(**{key: "unknown"})}
                report = assess(fixture, [], "TEST", "time", "Fire", "Fictional")
                self.assertTrue(report["decision"]["hold"])


if __name__ == "__main__":
    unittest.main()
