# Public Safety Opportunity Assessment

**Emergency Communications · Sort practice kit notes and update the log**

Assessment ID 66EEE9ABC077 · 2026-11-21T09:20:28-07:00 · Rules 1.8.0
19 answers · 2 local AI follow-up selections

## Triage recommendation

- **Solution fit:** Hybrid
- **Expected benefit (staff estimate):** High
- **Risk:** Elevated
- **IT involvement:** Tier 2 — IT delivery review
- **Readiness at submission:** Ready for triage
- **Proposed route:** IT technical triage → Business Systems / automation and AI enablement

AI could help interpret the information, and rules could handle the repeatable steps. Staff would check the result before it’s used.

**Technical recommendation:** Try AI for the part that requires reading and interpreting information. Use clear rules for repeatable steps. Have staff approve the result and handle anything out of the ordinary.

## Current workflow

- **Opportunity:** After a training session, I read the notes people leave about the practice kits. I decide whether each note is about sound, the screen, or a missing part, then find that kit in our log and type the category. I’d like help with those two steps.
- **Current steps:** From the opening answer (start) — “After a training session” From the opening answer (current steps) — “I read the notes people leave about the practice kits” Follow-up answer — I start with a note and a kit number. I read what happened, pick a category, and write that category on the row for the same kit number.
- **Volume and effort:** It happens after training sessions. I see about ten notes a week.
- **Tools and handoffs:** After I approve the draft, I’d like the note form to pass the category to the practice kit log. IT would need to check whether those two tools can talk to each other.
- **Inputs:** A form with a kit number and a box where people describe the problem in their own words.
- **Expected result:** Give me a suggested category and the note to check. Once I approve it, put the category on the row for that kit.
- **Exceptions:** If there’s no kit number or more than one row matches, leave the log alone and let me handle it.
- **Ownership:** The training lead owns both lists and has agreed to look at this with IT.
- **People affected:** The training room team uses the log.

## Proposed requirements

- Confirm a documented acceptance example and record who can approve the result.
- Validate the proposed result with the process owner. Give me a suggested category and the note to check. Once I approve it, put the category on the row for that kit.
- Run the staff-provided example as an acceptance test. If kit P-04 has a note that says ‘voices were hard to hear,’ suggest Sound. After I approve it, put Sound on the P-04 row.
- Document repeatable rules and keep a manual path for missing, conflicting or invalid inputs.
- Compare AI drafts with examples staff have checked. Make sure staff can correct or reject each draft.
- Specify least-privilege access, integration boundaries, failure handling and rollback before testing.

## Risk and governance

- **Data classification · Clear:** Routine administrative data reported.
  - Q4 “What information would this change use?” · Only routine or public information, such as supply counts — It’s just practice kit numbers and notes about the parts. No staff details or call records.
- **System access and transfers · Review:** Work out which tools need access, what information would move between them, and how to undo a change if something goes wrong.
  - Q5 “Would information stay in one place or move between tools?” · Tools would need to share it automatically — After I approve the draft, I’d like the note form to pass the category to the practice kit log. IT would need to…
  - Q6 “What would the tool need to do with the information?” · Add, change, delete, or send information in a City tool — After I approve a category, the log would fill in the category on the matching kit row.
- **Operational consequence · Review:** Agree on how staff will check the result and fix it if it’s wrong.
  - Q7 “What could happen if the result were wrong?” · Work could be delayed or redone, or internal information could be shared — A wrong entry could send us looking for the wrong part. We can correct it in the training log.
  - Q9 “Could the result affect an emergency, safety, care, or legal decision?” · No, it only helps with routine work like tracking supplies — This is only for practice kits kept in the training room. None of them are used to take calls.
- **Ownership and authorization · Clear:** Ownership and authorization are staff-reported. Obtain confirmation before any pilot.
  - Q8 “Who’s responsible for this work, and is this use allowed?” · We know who’s responsible for the work and the information, and this use is approved — The training lead owns both lists and has agreed to look at this with IT.
- **Human oversight · Review:** Make sure the reviewer can see the original information, reject a wrong result, and do the work by hand if needed.
  - Q19 “Will someone check the result before staff use it?” · Yes, someone checks and approves it first — The training room coordinator reads the original note, checks the kit number, and approves or corrects the…
  - Q7 “What could happen if the result were wrong?” · Work could be delayed or redone, or internal information could be shared — A wrong entry could send us looking for the wrong part. We can correct it in the training log.
  - Q9 “Could the result affect an emergency, safety, care, or legal decision?” · No, it only helps with routine work like tracking supplies — This is only for practice kits kept in the training room. None of them are used to take calls.

**Reviewers and checks**

- **Application owner** · System access and transfers
- **IT architecture** · System access and transfers
- **Department process owner** · Operational consequence, Human oversight
- **governance lead** · Operational consequence

## Screening scores

Scores of 6 or above indicate potential fit. The governance checks evaluate approval, scope, ownership and human oversight separately.

- **Automation screening score · 9/10**
  - +3 Some steps follow rules and others need someone to decide · Q11 “Do staff follow the same rules each time?”
  - +2 When a request or event comes in · Q10 “When does this work come up?”
  - +1 A mix of lists or forms and notes or emails · Q12 “What do you work from?”
  - +2 A draft someone checks, then a step that follows clear rules · Q13 “What should be ready when the work is done?”
  - +1 We know what can go wrong and who handles it · Q16 “What happens when the usual steps don't work?”
- **AI screening score · 9/10**
  - +3 A mix of lists or forms and notes or emails · Q12 “What do you work from?”
  - +3 Someone can check the result against the original information · Q15 “How do staff check a judgment call?”
  - +2 A draft someone checks, then a step that follows clear rules · Q13 “What should be ready when the work is done?”
  - +1 Some steps follow rules and others need someone to decide · Q11 “Do staff follow the same rules each time?”

## Assumptions and open questions

- The answers and estimates are staff-reported and require validation before implementation.
- Proposed routes are role labels. Confirm Flagstaff's intake channels and accountable roles before a pilot.
- Screening points summarize technical fit. Final disposition and approval belong to authorized reviewers.

## Next steps

1. **IT technical triage → Business Systems / automation and AI enablement** — Try AI for the part that requires reading and interpreting information. Use clear rules for repeatable steps. Have staff approve the result and handle anything out of the ordinary.
2. **Application owner / IT architecture** — Work out which tools need access, what information would move between them, and how to undo a change if something goes wrong.
3. **Department process owner / governance lead** — Agree on how staff will check the result and fix it if it’s wrong.
4. **Department process owner** — Make sure the reviewer can see the original information, reject a wrong result, and do the work by hand if needed.
5. **Department process owner** — Walk through the task with staff. Confirm how long it takes today, what result they need, and how they’ll tell if a change works.

## Interview record

- **Q1 · What task could work better for your team?** After a training session, I read the notes people leave about the practice kits. I decide whether each note is about sound, the screen, or a missing part, then find that kit in our log and type the category. I’d like help with those two steps.
- **Q2 · How do you know the task is done?** I start with a note and a kit number. I read what happened, pick a category, and write that category on the row for the same kit number.
- **Q3 · Can a tool you already use do this?** We've checked and haven't found one — We checked the note form and the kit log. Neither can read the notes and fill in the category.
- **Q4 · What information would this change use?** Only routine or public information, such as supply counts — It’s just practice kit numbers and notes about the parts. No staff details or call records.
- **Q5 · Would information stay in one place or move between tools?** Tools would need to share it automatically — After I approve the draft, I’d like the note form to pass the category to the practice kit log. IT would need to check whether those two tools can talk to each other.
- **Q6 · What would the tool need to do with the information?** Add, change, delete, or send information in a City tool — After I approve a category, the log would fill in the category on the matching kit row.
- **Q7 · What could happen if the result were wrong?** Work could be delayed or redone, or internal information could be shared — A wrong entry could send us looking for the wrong part. We can correct it in the training log.
- **Q8 · Who’s responsible for this work, and is this use allowed?** We know who’s responsible for the work and the information, and this use is approved — The training lead owns both lists and has agreed to look at this with IT.
- **Q9 · Could the result affect an emergency, safety, care, or legal decision?** No, it only helps with routine work like tracking supplies — This is only for practice kits kept in the training room. None of them are used to take calls.
- **Q10 · When does this work come up?** When a request or event comes in — It happens after training sessions. I see about ten notes a week.
- **Q11 · Do staff follow the same rules each time?** Some steps follow rules and others need someone to decide — Someone has to understand the note. Finding the kit’s row is always an exact match on kit number.
- **Q12 · What do you work from?** A mix of lists or forms and notes or emails — A form with a kit number and a box where people describe the problem in their own words.
- **Q13 · What should be ready when the work is done?** A draft someone checks, then a step that follows clear rules — Give me a suggested category and the note to check. Once I approve it, put the category on the row for that kit.
- **Q14 · Can you give an example of what should happen?** If kit P-04 has a note that says ‘voices were hard to hear,’ suggest Sound. After I approve it, put Sound on the P-04 row.
- **Q15 · How do staff check a judgment call?** Someone can check the result against the original information — I can read the original note and see whether the suggested category makes sense.
- **Q16 · What happens when the usual steps don't work?** We know what can go wrong and who handles it — If there’s no kit number or more than one row matches, leave the log alone and let me handle it.
- **Q17 · Who would use the result?** One team — The training room team uses the log.
- **Q18 · Does your team have a tool it’s allowed to use for this?** We checked and didn’t find an approved tool — The form and log are available, but we don’t know what approved tool can help read the notes or pass the category along.
- **Q19 · Will someone check the result before staff use it?** Yes, someone checks and approves it first — The training room coordinator reads the original note, checks the kit number, and approves or corrects the category before the log changes.
