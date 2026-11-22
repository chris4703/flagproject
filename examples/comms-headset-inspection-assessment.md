# Public Safety Opportunity Assessment

**Emergency Communications · Custom fictional workflow**

Assessment ID A25BB694C1B0 · 2026-11-19T20:56:04-07:00 · Rules 1.2.0
19 answers · 2 local AI follow-up selections

## Governance hold at submission

**First action · IT triage**

Do not pilot with real data. IT triage first confirms the data owner and approved environment, then brings in the applicable reviewers.

## Triage recommendation

- **Solution fit:** Hybrid
- **Expected benefit (staff estimate):** High
- **Risk:** High
- **IT involvement:** Tier 3 — Mandatory governance review
- **Readiness at submission:** Governance review required
- **Proposed route:** IT triage

Staff described a checkable interpretation and a fixed follow-on step, with human review before use.

**Technical recommendation:** Evaluate AI for the interpretation step and explicit rules for the predictable checks or routing. Keep exceptions and approval with staff.

## Current workflow

- **Opportunity:** After the monthly headset inspection I want a draft follow-up queue. Training supervisors currently read varied technician notes, match each to the equipment inventory, and transfer a proposed entry for manual approval.
- **Current steps:** A coordinator receives a fixed inventory export and technician comments in different formats. Notes can describe the same problem in several ways. Late or contradictory notes must stay in manual review. Once a supervisor confirms the equipment label and issue, team staff may update a separate maintenance register. No live decision is made here.
- **Volume and effort:** Monthly. Roughly 60 inspections and two hours to reconcile.
- **Tools and handoffs:** A proposed integration would carry supervisor-approved draft fields to the fictional Juniper maintenance register.
- **Inputs:** A standard inventory file plus variable technician comments. Some comments arrive late, omit the equipment label, or conflict with the inventory export.
- **Expected result:** Draft an issue category with a reference to the comment, then apply fixed equipment matching rules to make an exception or approval queue.
- **Exceptions:** Send missing labels, duplicate comments, and conflicting descriptions to the coordinator for manual review.
- **Ownership:** The training quality supervisor and inventory steward are identified and can authorize this synthetic test.
- **People affected:** The communications training team and facilities equipment team.

## Proposed requirements

- Confirm a documented acceptance example and record who can approve the result.
- Validate the proposed result with the process owner. Draft an issue category with a reference to the comment, then apply fixed equipment matching rules to make an exception or approval queue.
- Run the staff-provided example as an acceptance test. Fictional label HX-17 appears twice with different symptoms. Keep both source notes and send the draft to the supervisor instead of submitting an update.
- Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.
- Compare drafts against a reviewed synthetic reference set. A person must be able to correct or reject each draft.
- Specify least-privilege access, integration boundaries, failure handling and rollback before testing.

## Risk and governance

- **Data classification · Hold:** Confirm classification, approved processing environment and handling before implementation.
  - Q4 “What kind of information would the proposed change touch?” · Other private or restricted information — Technician comments could include internal personnel or performance remarks. The example contains generic…
- **System access and transfers · Review:** IT must map permissions, data flow and rollback.
  - Q5 “Where would the information come from and go?” · A new link between systems is needed — A proposed integration would carry supervisor-approved draft fields to the fictional Juniper maintenance register.
  - Q6 “What would the proposed change be allowed to do?” · Create, update, delete or send information in a shared system — A future approved connection may update a shared maintenance work item only after documented human approval.
- **Operational consequence · Hold:** Keep live and consequential decision-making outside this exercise. Confirm impact and decision boundaries before proceeding.
  - Q7 “What could happen if the result were wrong?” · It could affect safety, rights, clinical care, or a legal decision — Uncorrected omissions could indirectly leave faulty equipment available later. This review takes place after…
  - Q9 “Would this influence a live or consequential decision?” · Administrative support only — Administrative training and maintenance follow-up only. An approved supervisor makes any consequential decision…
- **Ownership and authorization · Clear:** Ownership and authorization are staff-reported. Obtain confirmation before any pilot.
  - Q8 “Who can approve access and own this workflow?” · A process owner and data owner are identified, and use is authorized — The training quality supervisor and inventory steward are identified and can authorize this synthetic test.
- **Human oversight · Review:** Confirm the reviewer can see the source, stop an incorrect result and use the manual path.
  - Q19 “Who checks the result before anyone acts on it?” · A person checks and approves before use — The supervisor reads the original note and inventory entry before approving a work item.
  - Q7 “What could happen if the result were wrong?” · It could affect safety, rights, clinical care, or a legal decision — Uncorrected omissions could indirectly leave faulty equipment available later. This review takes place after…
  - Q9 “Would this influence a live or consequential decision?” · Administrative support only — Administrative training and maintenance follow-up only. An approved supervisor makes any consequential decision…

**Reviewers and checks**

- **Information Security** · Data classification
- **data steward** · Data classification
- **Application owner** · System access and transfers
- **IT architecture** · System access and transfers
- **Department process owner** · Operational consequence, Human oversight
- **governance lead** · Operational consequence

## Screening scores

Scores of 6 or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.

- **Automation screening score · 9/10**
  - +3 Some steps have clear rules and some need interpretation · Q11 “Which parts follow the same rules every time?”
  - +2 On a regular schedule · Q10 “How often does this happen, and how much work is it?”
  - +1 A mix of lists or forms and free-form material · Q12 “What do you work from?”
  - +2 A draft or suggested interpretation followed by a fixed step · Q15 “What should be ready when the work is done?”
  - +1 Exceptions are known and someone can handle them · Q16 “What happens when the usual steps don't work?”
- **AI screening score · 9/10**
  - +3 A mix of lists or forms and free-form material · Q12 “What do you work from?”
  - +3 Someone can check the interpretation against a source · Q14 “Where does someone have to interpret information?”
  - +2 A draft or suggested interpretation followed by a fixed step · Q15 “What should be ready when the work is done?”
  - +1 Some steps have clear rules and some need interpretation · Q11 “Which parts follow the same rules every time?”

## Assumptions and open questions

- The scenario and examples are fictional. All workflow claims are staff-reported and require validation.
- Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.
- Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.

## Next steps

1. **Department process owner** — Confirm the current steps, baseline effort, expected result and acceptance criteria with staff.

## Interview record

- **Q1 · What would you like to make easier?** After the monthly headset inspection I want a draft follow-up queue. Training supervisors currently read varied technician notes, match each to the equipment inventory, and transfer a proposed entry for manual approval.
- **Q2 · How do you do this today?** A coordinator receives a fixed inventory export and technician comments in different formats. Notes can describe the same problem in several ways. Late or contradictory notes must stay in manual review. Once a supervisor confirms the equipment label and issue, team staff may update a separate maintenance register. No live decision is made here.
- **Q3 · Can a tool you already use do this?** We've checked and haven't found one — The fictional inventory and training review tools can export rows, and neither can interpret technician comments and match them to inventory.
- **Q4 · What kind of information would the proposed change touch?** Other private or restricted information — Technician comments could include internal personnel or performance remarks. The example contains generic fictional categories only.
- **Q5 · Where would the information come from and go?** A new link between systems is needed — A proposed integration would carry supervisor-approved draft fields to the fictional Juniper maintenance register.
- **Q6 · What would the proposed change be allowed to do?** Create, update, delete or send information in a shared system — A future approved connection may update a shared maintenance work item only after documented human approval.
- **Q7 · What could happen if the result were wrong?** It could affect safety, rights, clinical care, or a legal decision — Uncorrected omissions could indirectly leave faulty equipment available later. This review takes place after training inspection and makes no live dispatch or safety decisions.
- **Q8 · Who can approve access and own this workflow?** A process owner and data owner are identified, and use is authorized — The training quality supervisor and inventory steward are identified and can authorize this synthetic test.
- **Q9 · Would this influence a live or consequential decision?** Administrative support only — Administrative training and maintenance follow-up only. An approved supervisor makes any consequential decision separately.
- **Q10 · How often does this happen, and how much work is it?** On a regular schedule — Monthly. Roughly 60 inspections and two hours to reconcile.
- **Q11 · Which parts follow the same rules every time?** Some steps have clear rules and some need interpretation — Inventory matching is fixed. Translating free-text symptom descriptions into draft issue categories needs interpretation.
- **Q12 · What do you work from?** A mix of lists or forms and free-form material — A standard inventory file plus variable technician comments. Some comments arrive late, omit the equipment label, or conflict with the inventory export.
- **Q13 · Can you give one made-up input and the expected result?** Fictional label HX-17 appears twice with different symptoms. Keep both source notes and send the draft to the supervisor instead of submitting an update.
- **Q14 · Where does someone have to interpret information?** Someone can check the interpretation against a source — The supervisor can check the draft issue and asset label against the original note and the inventory before acting.
- **Q15 · What should be ready when the work is done?** A draft or suggested interpretation followed by a fixed step — Draft an issue category with a reference to the comment, then apply fixed equipment matching rules to make an exception or approval queue.
- **Q16 · What happens when the usual steps don't work?** Exceptions are known and someone can handle them — Send missing labels, duplicate comments, and conflicting descriptions to the coordinator for manual review.
- **Q17 · Who would use the result?** More than one department or team — The communications training team and facilities equipment team.
- **Q18 · Is there an approved tool staff can use within their current access?** No suitable tool is known to be approved — The draft classification and shared update require a new approved capability.
- **Q19 · Who checks the result before anyone acts on it?** A person checks and approves before use — The supervisor reads the original note and inventory entry before approving a work item.
