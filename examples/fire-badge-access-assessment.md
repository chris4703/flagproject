# Public Safety Opportunity Assessment

**Fire · Check badge requests for the records room**

Assessment ID 141FCEC95C66 · 2026-11-21T10:16:20-07:00 · Rules 1.8.0
17 answers · 2 local AI follow-up selections

## Governance hold at submission

**First action · IT triage**

Do not pilot with real data. IT triage first confirms the data owner and approved environment, then brings in the applicable reviewers.

## Triage recommendation

- **Solution fit:** Automation
- **Expected benefit (staff estimate):** Moderate
- **Risk:** High
- **IT involvement:** Tier 3 — Mandatory governance review
- **Readiness at submission:** Governance review required
- **Proposed route:** IT triage

Staff reported repeatable rules and a predictable result. A team-managed path was not established.

**Technical recommendation:** Use made-up examples to test the steps that follow the same rules every time. Agree on what starts the task, what to check, and when staff should take over.

## Current workflow

- **Opportunity:** I help process badge requests for the Fire personnel records room. When a supervisor sends a request, I check whether the employee is active, whether their job is on the approved access list, and whether temporary access has an end date. Then the records manager approves the request and Building Security updates the badge. I spend time chasing missing dates. I’d like the form to flag missing or mismatched details before approval. The records manager would still approve each request, and Building Security would make the badge change. A wrong change could let someone see confidential staff files.
- **Current steps:** From the opening answer (start) — “When a supervisor sends a request” From the opening answer (current steps) — “I check whether the employee is active, whether their job is on the approved access list, and whether temporary access has an end date” Follow-up answer — I start with a supervisor’s request. I compare it with the staff roster and approved job list, then mark any missing details. I give the checked request to the records manager. If they approve it, Building Security changes the badge.
- **Volume and effort:** I do this whenever a supervisor sends a request. Most weeks there are a few. A request with missing details can take a second round of emails.
- **Tools and handoffs:** I’d like the request form to check an approved copy of the staff roster and job list. Ask IT whether those sources can share just the fields the form needs. The form leaves the badge system alone.
- **Inputs:** A request form with the same fields each time, an approved job list, and a staff roster with employment status.
- **Expected result:** A short checklist showing which fields matched and which ones staff need to check before the request goes for approval.
- **Exceptions:** If a request has a missing date or the job doesn’t match, I ask the supervisor to check it. If the roster is unavailable, I pause the request and check with HR. For example, if a temporary access form is missing its end date, flag the missing date and leave the badge unchanged.
- **Ownership:** The records manager owns the room access list, HR owns the staff roster, and Building Security manages badges. They’ve agreed to use made-up requests for a review. IT still needs to confirm which roster fields can be used and where.
- **People affected:** Fire office staff check requests, the records manager approves them, and Building Security makes badge changes.

## Proposed requirements

- Confirm a documented acceptance example and record who can approve the result.
- Validate the proposed result with the process owner. A short checklist showing which fields matched and which ones staff need to check before the request goes for approval.
- Run the staff-provided example from question 13 as an acceptance test. For example, if a temporary access form is missing its end date, flag the missing date and leave the badge unchanged.
- Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.
- Specify least-privilege access, integration boundaries, failure handling and rollback before testing.

## Risk and governance

- **Data classification · Hold:** Confirm who may see the private information, where it can be kept, and whether staff may use it this way.
  - Q4 “What information would this change use?” · Other private information, such as personnel records — The checks use private staff information, including employment status, job role, and who has asked for access. We…
- **System access and transfers · Review:** Work out which tools need access, what information would move between them, and how to undo a change if something goes wrong.
  - Q5 “Would information stay in one place or move between tools?” · Tools would need to share it automatically — I’d like the request form to check an approved copy of the staff roster and job list. Ask IT whether those sources…
  - Q6 “What would the tool need to do with the information?” · Only read information, run a report, or prepare a draft — The form only reads the fields it needs and shows what is missing or doesn’t match. The records manager approves…
- **Operational consequence · Hold:** Keep live and consequential decision-making outside this exercise. Confirm impact and decision boundaries before proceeding.
  - Q7 “What could happen if the result were wrong?” · It could affect someone’s safety, rights, medical care, or a legal decision — If a wrongly cleared request led to a bad badge change, someone could enter the locked room and see confidential…
  - Q9 “Could the result affect an emergency, safety, care, or legal decision?” · No, it only helps with routine work like tracking supplies — The form supports an office approval process. It flags details for staff to check. The records manager decides who…
- **Ownership and authorization · Clear:** Ownership and authorization are staff-reported. Obtain confirmation before any pilot.
  - Q8 “Who’s responsible for this work, and is this use allowed?” · We know who’s responsible for the work and the information, and this use is approved — The records manager owns the room access list, HR owns the staff roster, and Building Security manages badges.…
- **Human oversight · Review:** Make sure the reviewer can see the original information, reject a wrong result, and do the work by hand if needed.
  - Q17 “Will someone check the result before staff use it?” · Yes, someone checks and approves it first — The records manager checks the request against the approved list and signs off before Building Security changes a…
  - Q7 “What could happen if the result were wrong?” · It could affect someone’s safety, rights, medical care, or a legal decision — If a wrongly cleared request led to a bad badge change, someone could enter the locked room and see confidential…
  - Q9 “Could the result affect an emergency, safety, care, or legal decision?” · No, it only helps with routine work like tracking supplies — The form supports an office approval process. It flags details for staff to check. The records manager decides who…

**Reviewers and checks**

- **Information Security** · Data classification
- **data steward** · Data classification
- **Application owner** · System access and transfers
- **IT architecture** · System access and transfers
- **Department process owner** · Operational consequence, Human oversight
- **governance lead** · Operational consequence

## Screening scores

Scores of 6 or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.

- **Automation screening score · 10/10**
  - +3 Most steps follow clear rules · Q11 “Do staff follow the same rules each time?”
  - +2 When a request or event comes in · Q10 “When does this work come up?”
  - +2 Lists or forms with the same layout each time · Q12 “What do you work from?”
  - +2 A list, check, reminder, or update that follows clear rules · Q15 “What should be ready when the work is done?”
  - +1 We know what can go wrong and who handles it · Q13 “What happens when the usual steps don't work?”
- **AI screening score · 0/10**

## Assumptions and open questions

- The answers and estimates are staff-reported and require validation before implementation.
- Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.
- Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.

## Next steps

1. **Department process owner** — Walk through the task with staff. Confirm how long it takes today, what result they need, and how they’ll tell if a change works.

## Interview record

- **Q1 · What task could work better for your team?** I help process badge requests for the Fire personnel records room. When a supervisor sends a request, I check whether the employee is active, whether their job is on the approved access list, and whether temporary access has an end date. Then the records manager approves the request and Building Security updates the badge. I spend time chasing missing dates. I’d like the form to flag missing or mismatched details before approval. The records manager would still approve each request, and Building Security would make the badge change. A wrong change could let someone see confidential staff files.
- **Q2 · How do you know the task is done?** I start with a supervisor’s request. I compare it with the staff roster and approved job list, then mark any missing details. I give the checked request to the records manager. If they approve it, Building Security changes the badge.
- **Q3 · Can a tool you already use do this?** We've checked and haven't found one — Our badge system can apply an approved change. We checked with Building Security and it doesn’t run these three checks on incoming requests.
- **Q4 · What information would this change use?** Other private information, such as personnel records — The checks use private staff information, including employment status, job role, and who has asked for access. We can test with made-up requests and a made-up roster.
- **Q5 · Would information stay in one place or move between tools?** Tools would need to share it automatically — I’d like the request form to check an approved copy of the staff roster and job list. Ask IT whether those sources can share just the fields the form needs. The form leaves the badge system alone.
- **Q6 · What would the tool need to do with the information?** Only read information, run a report, or prepare a draft — The form only reads the fields it needs and shows what is missing or doesn’t match. The records manager approves each request. Building Security makes any changes to badges.
- **Q7 · What could happen if the result were wrong?** It could affect someone’s safety, rights, medical care, or a legal decision — If a wrongly cleared request led to a bad badge change, someone could enter the locked room and see confidential staff files.
- **Q8 · Who’s responsible for this work, and is this use allowed?** We know who’s responsible for the work and the information, and this use is approved — The records manager owns the room access list, HR owns the staff roster, and Building Security manages badges. They’ve agreed to use made-up requests for a review. IT still needs to confirm which roster fields can be used and where.
- **Q9 · Could the result affect an emergency, safety, care, or legal decision?** No, it only helps with routine work like tracking supplies — The form supports an office approval process. It flags details for staff to check. The records manager decides who may enter the room, and Building Security applies that decision.
- **Q10 · When does this work come up?** When a request or event comes in — I do this whenever a supervisor sends a request. Most weeks there are a few. A request with missing details can take a second round of emails.
- **Q11 · Do staff follow the same rules each time?** Most steps follow clear rules — Flag the request if the roster doesn’t show the person as active, the job doesn’t match the approved list, or a temporary request has no end date.
- **Q12 · What do you work from?** Lists or forms with the same layout each time — A request form with the same fields each time, an approved job list, and a staff roster with employment status.
- **Q13 · What happens when the usual steps don't work?** We know what can go wrong and who handles it — If a request has a missing date or the job doesn’t match, I ask the supervisor to check it. If the roster is unavailable, I pause the request and check with HR. For example, if a temporary access form is missing its end date, flag the missing date and leave the badge unchanged.
- **Q14 · Who would use the result?** More than one department or team — Fire office staff check requests, the records manager approves them, and Building Security makes badge changes.
- **Q15 · What should be ready when the work is done?** A list, check, reminder, or update that follows clear rules — A short checklist showing which fields matched and which ones staff need to check before the request goes for approval.
- **Q16 · Does your team have a tool it’s allowed to use for this?** We checked and didn’t find an approved tool — We have an approved badge system for applying changes. We haven’t found an approved tool for doing these request checks.
- **Q17 · Will someone check the result before staff use it?** Yes, someone checks and approves it first — The records manager checks the request against the approved list and signs off before Building Security changes a badge. Staff return an incomplete request and can check the information by hand.
