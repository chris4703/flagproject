# Public Safety Opportunity Assessment

**Emergency Communications · Retrospective quality queue**

Assessment ID B37DE05ED967 · 2026-11-20T12:20:48-07:00 · Rules 1.4.0
17 answers · 2 local AI follow-up selections

## Governance hold at submission

**First action · IT triage**

Do not pilot with real data. IT triage first confirms the data owner and approved environment, then brings in the applicable reviewers.

## Triage recommendation

- **Solution fit:** Automation
- **Expected benefit (staff estimate):** Not estimated
- **Risk:** High
- **IT involvement:** Tier 3 — Mandatory governance review
- **Readiness at submission:** Governance review required
- **Proposed route:** IT triage

Staff reported repeatable rules and a predictable result. A team-managed path was not established.

**Technical recommendation:** Evaluate a rules-based workflow using synthetic examples. Confirm the trigger, checks and manual exception path.

## Current workflow

- **Opportunity:** Prepare a retrospective check queue so a quality supervisor can see which training records still need a check.
- **Current steps:** After the training week ends, the coordinator receives synthetic export rows, applies a missing-review rule, and gives a draft queue to the quality supervisor.
- **Volume and effort:** Weekly, about 45 rows and 35 minutes.
- **Tools and handoffs:** A read-only export from the Juniper Console would be compared with a separate checklist.
- **Inputs:** Fixed spreadsheet columns with identifiers.
- **Expected result:** Produce a draft list of rows with an empty review stamp.
- **Exceptions:** Route invalid stamps to the quality supervisor for manual checking.
- **Ownership:** The quality supervisor owns the work. Data owner authorization is unresolved.
- **People affected:** One administrative review team.

## Proposed requirements

- Confirm a documented acceptance example and record who can approve the result.
- Validate the proposed result with the process owner. Produce a draft list of rows with an empty review stamp.
- Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.

## Risk and governance

- **Data classification · Hold:** Confirm classification, approved processing environment and handling before implementation.
  - Q4 “What kind of information would the proposed change touch?” · Could include criminal justice and patient information — Hypothetical field categories include protected health details and criminal justice information. The review uses…
- **Potential CJIS applicability · Hold:** Validate CJI scope and agency requirements with the designated CJIS contact.
  - Q4 “What kind of information would the proposed change touch?” · Could include criminal justice and patient information — Hypothetical field categories include protected health details and criminal justice information. The review uses…
- **Potential HIPAA applicability · Hold:** Confirm covered function, PHI/ePHI exposure, safeguards and any business associate obligations.
  - Q4 “What kind of information would the proposed change touch?” · Could include criminal justice and patient information — Hypothetical field categories include protected health details and criminal justice information. The review uses…
- **System access and transfers · Clear:** Existing access or manual transfer reported. Confirm the actual boundary during triage.
  - Q5 “Where would the information come from and go?” · Between tools using a manual handoff — A read-only export from the Juniper Console would be compared with a separate checklist.
  - Q6 “What would the proposed change be allowed to do?” · Read or draft only, or stay within existing approved access — Only draft a queue. All record handling occurs in the approved manual process.
- **Operational consequence · Review:** Set an acceptance check and a way to correct a bad result.
  - Q7 “What could happen if the result were wrong?” · It could delay work, cause rework, or disclose internal information — A missing row delays retrospective quality review.
  - Q9 “Would this influence a live or consequential decision?” · Administrative support only — Retrospective administrative review after the training week.
- **Ownership and authorization · Hold:** Identify the process and data owners and confirm their authorization.
  - Q8 “Who can approve access and own this workflow?” · An owner or permission still needs confirmation — The quality supervisor owns the work. Data owner authorization is unresolved.
- **Human oversight · Review:** Confirm the reviewer can see the source, stop an incorrect result and use the manual path.
  - Q17 “Who checks the result before anyone acts on it?” · A person checks and approves before use — The quality supervisor checks all rows before accepting the queue.
  - Q7 “What could happen if the result were wrong?” · It could delay work, cause rework, or disclose internal information — A missing row delays retrospective quality review.
  - Q9 “Would this influence a live or consequential decision?” · Administrative support only — Retrospective administrative review after the training week.

**Reviewers and checks**

- **Information Security** · Data classification, Potential CJIS applicability
- **data steward** · Data classification
- **City CJIS contact** · Potential CJIS applicability
- **City Privacy** · Potential HIPAA applicability
- **Legal** · Potential HIPAA applicability
- **Department process owner** · Operational consequence, Human oversight
- **governance lead** · Operational consequence
- **Department lead** · Ownership and authorization
- **data owner** · Ownership and authorization

## Screening scores

Scores of 6 or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.

- **Automation screening score · 10/10**
  - +3 Most steps have clear rules · Q11 “Which parts follow the same rules every time?”
  - +2 On a regular schedule · Q10 “How often does this happen, and how much work is it?”
  - +2 Lists, forms or fields in a consistent format · Q12 “What do you work from?”
  - +2 A predictable list, check, reminder, or update · Q15 “What should be ready when the work is done?”
  - +1 Exceptions are known and someone can handle them · Q13 “What happens when the usual steps don't work?”
- **AI screening score · 0/10**

## Assumptions and open questions

- The answers and estimates are staff-reported and require validation before implementation.
- Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.
- Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.
- Who can approve access and own this workflow?
- Is there an approved tool staff can use within their current access?
- What synthetic inputs and expected results should IT use for acceptance testing?

## Next steps

1. **Department process owner** — Confirm the current steps, baseline effort, expected result and acceptance criteria with staff.

## Interview record

- **Q1 · What would you like to make easier?** Prepare a retrospective check queue so a quality supervisor can see which training records still need a check.
- **Q2 · How do you do this today?** After the training week ends, the coordinator receives synthetic export rows, applies a missing-review rule, and gives a draft queue to the quality supervisor.
- **Q3 · Can a tool you already use do this?** We've checked and haven't found one — The system has a raw export only.
- **Q4 · What kind of information would the proposed change touch?** Could include criminal justice and patient information — Hypothetical field categories include protected health details and criminal justice information. The review uses field categories only.
- **Q5 · Where would the information come from and go?** Between tools using a manual handoff — A read-only export from the Juniper Console would be compared with a separate checklist.
- **Q6 · What would the proposed change be allowed to do?** Read or draft only, or stay within existing approved access — Only draft a queue. All record handling occurs in the approved manual process.
- **Q7 · What could happen if the result were wrong?** It could delay work, cause rework, or disclose internal information — A missing row delays retrospective quality review.
- **Q8 · Who can approve access and own this workflow?** An owner or permission still needs confirmation — The quality supervisor owns the work. Data owner authorization is unresolved.
- **Q9 · Would this influence a live or consequential decision?** Administrative support only — Retrospective administrative review after the training week.
- **Q10 · How often does this happen, and how much work is it?** On a regular schedule — Weekly, about 45 rows and 35 minutes.
- **Q11 · Which parts follow the same rules every time?** Most steps have clear rules — Flag rows without a completed review stamp.
- **Q12 · What do you work from?** Lists, forms or fields in a consistent format — Fixed spreadsheet columns with identifiers.
- **Q13 · What happens when the usual steps don't work?** Exceptions are known and someone can handle them — Route invalid stamps to the quality supervisor for manual checking.
- **Q14 · Who would use the result?** One team — One administrative review team.
- **Q15 · What should be ready when the work is done?** A predictable list, check, reminder, or update — Produce a draft list of rows with an empty review stamp.
- **Q16 · Is there an approved tool staff can use within their current access?** I'm not sure — Data steward and Information Security have not validated a tool.
- **Q17 · Who checks the result before anyone acts on it?** A person checks and approves before use — The quality supervisor checks all rows before accepting the queue.
