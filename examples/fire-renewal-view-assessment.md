# Public Safety Opportunity Assessment

**Fire · See staff renewals due soon**

Assessment ID D603702AF840 · 2026-11-21T09:20:18-07:00 · Rules 1.8.0
17 answers · 2 local AI follow-up selections

## Governance hold at submission

**First action · IT triage**

Do not pilot with real data. IT triage first confirms the data owner and approved environment, then brings in the applicable reviewers.

## Triage recommendation

- **Solution fit:** Self-service
- **Expected benefit (staff estimate):** Moderate
- **Risk:** High
- **IT involvement:** Tier 3 — Mandatory governance review
- **Readiness at submission:** Governance review required
- **Proposed route:** IT triage

Staff could make this small change in a tool their team already uses. Check the review requirements before trying it.

**Technical recommendation:** Check which approved tool the team can use. Try a small change the team can undo if it doesn’t work.

## Current workflow

- **Opportunity:** Each Monday I check our staff training workbook for renewals due in the next 30 days. I read each row and mark what’s coming up for the training coordinator. I’d like a saved view that shows the rows I need to check.
- **Current steps:** From the opening answer (start) — “Each Monday” From the opening answer (current steps) — “I check our staff training workbook for renewals due in the next 30 days” Follow-up answer — I open the workbook, compare each renewal date to the calendar, and tell the training coordinator which items are due soon.
- **Volume and effort:** I do this each Monday. It takes about 15 minutes.
- **Tools and handoffs:** The view would stay in our current workbook in the same restricted folder.
- **Inputs:** Every row has the same columns, including the renewal date.
- **Expected result:** A view in the same workbook that shows only renewals due in the next 30 days.
- **Exceptions:** If a renewal date is blank, the coordinator checks the original record by hand.
- **Ownership:** The training coordinator and HR own the workbook. They’ve allowed our training office to use it for renewal reminders. IT should check who would be able to see the new view.
- **People affected:** Only the training office staff who already use the workbook.

## Proposed requirements

- Confirm a documented acceptance example and record who can approve the result.
- Validate the proposed result with the process owner. A view in the same workbook that shows only renewals due in the next 30 days.
- Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.

## Risk and governance

- **Data classification · Hold:** Confirm who may see the private information, where it can be kept, and whether staff may use it this way.
  - Q4 “What information would this change use?” · Other private information, such as personnel records — The workbook contains staff names and individual training renewal dates. This is private staff information.
- **System access and transfers · Clear:** Existing access or manual transfer reported. Confirm the actual boundary during triage.
  - Q5 “Would information stay in one place or move between tools?” · It stays in one app or shared workspace — The view would stay in our current workbook in the same restricted folder.
  - Q6 “What would the tool need to do with the information?” · Only read information, run a report, or prepare a draft — It would only show matching rows. It would never change dates or send anything.
- **Operational consequence · Clear:** Agree on how staff will check the result and fix it if it’s wrong.
  - Q7 “What could happen if the result were wrong?” · Someone could catch and fix it before it causes a problem — I’d compare the view with the workbook before doing anything with the list.
  - Q9 “Could the result affect an emergency, safety, care, or legal decision?” · No, it only helps with routine work like tracking supplies — This is for office reminders. We aren’t using it to assign shifts or decide whether someone can work.
- **Ownership and authorization · Clear:** Ownership and authorization are staff-reported. Obtain confirmation before any pilot.
  - Q8 “Who’s responsible for this work, and is this use allowed?” · We know who’s responsible for the work and the information, and this use is approved — The training coordinator and HR own the workbook. They’ve allowed our training office to use it for renewal…

**Reviewers and checks**

- **Information Security** · Data classification
- **data steward** · Data classification

## Screening scores

Scores of 6 or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.

- **Automation screening score · 10/10**
  - +3 Most steps follow clear rules · Q11 “Do staff follow the same rules each time?”
  - +2 On a schedule, such as every Friday · Q10 “When does this work come up?”
  - +2 Lists or forms with the same layout each time · Q12 “What do you work from?”
  - +2 A list, check, reminder, or update that follows clear rules · Q13 “What should be ready when the work is done?”
  - +1 We know what can go wrong and who handles it · Q15 “What happens when the usual steps don't work?”
- **AI screening score · 0/10**

## Assumptions and open questions

- The answers and estimates are staff-reported and require validation before implementation.
- Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.
- Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.
- What synthetic inputs and expected results should IT use for acceptance testing?

## Next steps

1. **Department process owner** — Walk through the task with staff. Confirm how long it takes today, what result they need, and how they’ll tell if a change works.

## Interview record

- **Q1 · What task could work better for your team?** Each Monday I check our staff training workbook for renewals due in the next 30 days. I read each row and mark what’s coming up for the training coordinator. I’d like a saved view that shows the rows I need to check.
- **Q2 · How do you know the task is done?** I open the workbook, compare each renewal date to the calendar, and tell the training coordinator which items are due soon.
- **Q3 · Can a tool you already use do this?** We've checked and haven't found one — We have the workbook, but there isn’t a saved view for renewals coming up.
- **Q4 · What information would this change use?** Other private information, such as personnel records — The workbook contains staff names and individual training renewal dates. This is private staff information.
- **Q5 · Would information stay in one place or move between tools?** It stays in one app or shared workspace — The view would stay in our current workbook in the same restricted folder.
- **Q6 · What would the tool need to do with the information?** Only read information, run a report, or prepare a draft — It would only show matching rows. It would never change dates or send anything.
- **Q7 · What could happen if the result were wrong?** Someone could catch and fix it before it causes a problem — I’d compare the view with the workbook before doing anything with the list.
- **Q8 · Who’s responsible for this work, and is this use allowed?** We know who’s responsible for the work and the information, and this use is approved — The training coordinator and HR own the workbook. They’ve allowed our training office to use it for renewal reminders. IT should check who would be able to see the new view.
- **Q9 · Could the result affect an emergency, safety, care, or legal decision?** No, it only helps with routine work like tracking supplies — This is for office reminders. We aren’t using it to assign shifts or decide whether someone can work.
- **Q10 · When does this work come up?** On a schedule, such as every Friday — I do this each Monday. It takes about 15 minutes.
- **Q11 · Do staff follow the same rules each time?** Most steps follow clear rules — Show any renewals coming due in the next 30 days.
- **Q12 · What do you work from?** Lists or forms with the same layout each time — Every row has the same columns, including the renewal date.
- **Q13 · What should be ready when the work is done?** A list, check, reminder, or update that follows clear rules — A view in the same workbook that shows only renewals due in the next 30 days.
- **Q14 · Who would use the result?** One team — Only the training office staff who already use the workbook.
- **Q15 · What happens when the usual steps don't work?** We know what can go wrong and who handles it — If a renewal date is blank, the coordinator checks the original record by hand.
- **Q16 · Does your team have a tool it’s allowed to use for this?** Yes, our team can use an approved tool for this — We already use the approved workbook in a restricted folder. We’d use that same file.
- **Q17 · Will someone check the result before staff use it?** Yes, someone checks and approves it first — The training coordinator would compare the view against the original dates before using it.
