# Public Safety Opportunity Assessment

**Fire · Weekly drill records**

Assessment ID AF07A1A1FBD4 · 2026-11-20T12:20:48-07:00 · Rules 1.4.0
19 answers · 2 local AI follow-up selections

## Triage recommendation

- **Solution fit:** Hybrid
- **Expected benefit (staff estimate):** Not estimated
- **Risk:** Elevated
- **IT involvement:** Tier 1 — IT advisory
- **Readiness at submission:** Ready for triage
- **Proposed route:** Business Systems / automation and AI enablement

Staff described a checkable interpretation and a fixed follow-on step, with human review before use.

**Technical recommendation:** Evaluate AI for the interpretation step and explicit rules for the predictable checks or routing. Keep exceptions and approval with staff.

## Current workflow

- **Opportunity:** Build a reliable Friday follow-up list for drills. Reading short drill notes and matching them to the training tracker takes most of the time.
- **Current steps:** On Friday I export the Mesa Pine training tracker, read each station’s drill notes, match the drill IDs, and mark missing or late entries. The training supervisor checks the draft before staff are reminded.
- **Volume and effort:** Weekly, about 35 drill entries and 70 minutes of hands-on effort. Roughly five need manual reconciliation.
- **Tools and handoffs:** The Mesa Pine tracker produces a CSV. Station notes are in a shared training folder. Staff assemble the review list manually.
- **Inputs:** A CSV of scheduled drills and short notes in inconsistent formats. Some notes are late or disagree with the tracker.
- **Expected result:** Suggest drill ID, date and completion status from each note. Apply matching rules to produce a draft list with matched, missing and conflicting entries.
- **Exceptions:** Missing IDs, mismatched dates and late notes go to a manual queue. The supervisor decides what to follow up on.
- **Ownership:** Training supervisor owns the workflow. Training records steward authorizes use of the synthetic drill inputs.
- **People affected:** Two training administrators and one supervisor in the training section.

## Proposed requirements

- Confirm a documented acceptance example and record who can approve the result.
- Validate the proposed result with the process owner. Suggest drill ID, date and completion status from each note. Apply matching rules to produce a draft list with matched, missing and conflicting entries.
- Run the staff-provided example as an acceptance test. The tracker lists drill MP-17 for Friday. A station note says MP-17 moved to Monday. Route it to review with the note attached as a reference.
- Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.
- Compare drafts against a reviewed synthetic reference set. A person must be able to correct or reject each draft.

## Risk and governance

- **Data classification · Clear:** Routine administrative data reported.
  - Q4 “What kind of information would the proposed change touch?” · Routine or public administrative information — Synthetic drill codes, dates and generic team labels only.
- **System access and transfers · Clear:** Existing access or manual transfer reported. Confirm the actual boundary during triage.
  - Q5 “Where would the information come from and go?” · Between tools using a manual handoff — The Mesa Pine tracker produces a CSV. Station notes are in a shared training folder. Staff assemble the review…
  - Q6 “What would the proposed change be allowed to do?” · Read or draft only, or stay within existing approved access — Read the two inputs and prepare a draft in the training workspace. Staff handle any reminders.
- **Operational consequence · Review:** Set an acceptance check and a way to correct a bad result.
  - Q7 “What could happen if the result were wrong?” · It could delay work, cause rework, or disclose internal information — An incorrect match could create duplicate follow-up or delay a reminder.
  - Q9 “Would this influence a live or consequential decision?” · Administrative support only — Administrative drill recordkeeping only.
- **Ownership and authorization · Clear:** Ownership and authorization are staff-reported. Obtain confirmation before any pilot.
  - Q8 “Who can approve access and own this workflow?” · A process owner and data owner are identified, and use is authorized — Training supervisor owns the workflow. Training records steward authorizes use of the synthetic drill inputs.
- **Human oversight · Review:** Confirm the reviewer can see the source, stop an incorrect result and use the manual path.
  - Q19 “Who checks the result before anyone acts on it?” · A person checks and approves before use — The training supervisor checks each exception against its source and signs off on the list. Staff can revert to…
  - Q7 “What could happen if the result were wrong?” · It could delay work, cause rework, or disclose internal information — An incorrect match could create duplicate follow-up or delay a reminder.
  - Q9 “Would this influence a live or consequential decision?” · Administrative support only — Administrative drill recordkeeping only.

**Reviewers and checks**

- **Department process owner** · Operational consequence, Human oversight
- **governance lead** · Operational consequence

## Screening scores

Scores of 6 or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.

- **Automation screening score · 9/10**
  - +3 Some steps have clear rules and some need interpretation · Q11 “Which parts follow the same rules every time?”
  - +2 On a regular schedule · Q10 “How often does this happen, and how much work is it?”
  - +1 A mix of lists or forms and free-form material · Q12 “What do you work from?”
  - +2 A draft or suggested interpretation followed by a fixed step · Q14 “What should be ready when the work is done?”
  - +1 Exceptions are known and someone can handle them · Q16 “What happens when the usual steps don't work?”
- **AI screening score · 9/10**
  - +3 A mix of lists or forms and free-form material · Q12 “What do you work from?”
  - +3 Someone can check the interpretation against a source · Q13 “Where does someone have to interpret information?”
  - +2 A draft or suggested interpretation followed by a fixed step · Q14 “What should be ready when the work is done?”
  - +1 Some steps have clear rules and some need interpretation · Q11 “Which parts follow the same rules every time?”

## Assumptions and open questions

- The answers and estimates are staff-reported and require validation before implementation.
- Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.
- Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.
- Can an existing feature or configuration cover the remaining need?

## Next steps

1. **Business Systems / automation and AI enablement** — Evaluate AI for the interpretation step and explicit rules for the predictable checks or routing. Keep exceptions and approval with staff.
2. **Department process owner / governance lead** — Set an acceptance check and a way to correct a bad result.
3. **Department process owner** — Confirm the reviewer can see the source, stop an incorrect result and use the manual path.
4. **Department process owner** — Confirm the current steps, baseline effort, expected result and acceptance criteria with staff.

## Interview record

- **Q1 · What would you like to make easier?** Build a reliable Friday follow-up list for drills. Reading short drill notes and matching them to the training tracker takes most of the time.
- **Q2 · How do you do this today?** On Friday I export the Mesa Pine training tracker, read each station’s drill notes, match the drill IDs, and mark missing or late entries. The training supervisor checks the draft before staff are reminded.
- **Q3 · Can a tool you already use do this?** It covers part of the work — The tracker can list scheduled drills. It cannot match free-form station notes or explain a missing entry.
- **Q4 · What kind of information would the proposed change touch?** Routine or public administrative information — Synthetic drill codes, dates and generic team labels only.
- **Q5 · Where would the information come from and go?** Between tools using a manual handoff — The Mesa Pine tracker produces a CSV. Station notes are in a shared training folder. Staff assemble the review list manually.
- **Q6 · What would the proposed change be allowed to do?** Read or draft only, or stay within existing approved access — Read the two inputs and prepare a draft in the training workspace. Staff handle any reminders.
- **Q7 · What could happen if the result were wrong?** It could delay work, cause rework, or disclose internal information — An incorrect match could create duplicate follow-up or delay a reminder.
- **Q8 · Who can approve access and own this workflow?** A process owner and data owner are identified, and use is authorized — Training supervisor owns the workflow. Training records steward authorizes use of the synthetic drill inputs.
- **Q9 · Would this influence a live or consequential decision?** Administrative support only — Administrative drill recordkeeping only.
- **Q10 · How often does this happen, and how much work is it?** On a regular schedule — Weekly, about 35 drill entries and 70 minutes of hands-on effort. Roughly five need manual reconciliation.
- **Q11 · Which parts follow the same rules every time?** Some steps have clear rules and some need interpretation — Matching drill IDs and dates and finding missing entries follow written rules. Reading notes about rescheduled drills needs interpretation.
- **Q12 · What do you work from?** A mix of lists or forms and free-form material — A CSV of scheduled drills and short notes in inconsistent formats. Some notes are late or disagree with the tracker.
- **Q13 · Where does someone have to interpret information?** Someone can check the interpretation against a source — The supervisor checks a suggested drill ID and date against the original note and the tracker.
- **Q14 · What should be ready when the work is done?** A draft or suggested interpretation followed by a fixed step — Suggest drill ID, date and completion status from each note. Apply matching rules to produce a draft list with matched, missing and conflicting entries.
- **Q15 · Can you give a representative input and the expected result?** The tracker lists drill MP-17 for Friday. A station note says MP-17 moved to Monday. Route it to review with the note attached as a reference.
- **Q16 · What happens when the usual steps don't work?** Exceptions are known and someone can handle them — Missing IDs, mismatched dates and late notes go to a manual queue. The supervisor decides what to follow up on.
- **Q17 · Who would use the result?** One team — Two training administrators and one supervisor in the training section.
- **Q18 · Is there an approved tool staff can use within their current access?** No suitable tool is known to be approved — The tracker and shared folder exist. An approved tool for interpreting notes has yet to be identified.
- **Q19 · Who checks the result before anyone acts on it?** A person checks and approves before use — The training supervisor checks each exception against its source and signs off on the list. Staff can revert to the current manual list.
