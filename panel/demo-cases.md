# Flagstaff WIP · Current panel cases

Both analyst dashboards contain all seven cases. The panel walkthrough pairs the Police room calendar with Fire badge access. Open **Find assessment** and enter the ID for the copy you are using. To repeat a case, open **Try a practice scenario** on the staff homepage.

| Staff request | Assessment and what to show | Hosted ID | MacBook ID |
| --- | --- | --- | --- |
| **Police · Find the meeting room calendar.** “I click through each room to see what’s free. Can we make that easier?” | **Existing solution · Low risk · Tier 0.** The weekly view already shows all the rooms. Show staff where to find it. The interview can finish in 10 questions with the required checks complete. [Report](../examples/police-room-calendar-assessment.md) | `01C1AC79C80F` | `86F1AC41C75E` |
| **Fire · See staff renewals due soon.** “Can I see just the renewals due in the next 30 days in the workbook we already use?” | **Self-service · High risk · Tier 3 hold.** The team could add a filter. The workbook contains private staff information. Open the hold and show what IT must confirm about access and permitted use before the team tests with real data. [Report](../examples/fire-renewal-view-assessment.md) | `D603702AF840` | `31253D3935C6` |
| **Emergency Communications · Sort practice kit notes and update the log.** “Can I check a suggested category, then have it go on the right kit’s row?” | **Hybrid · Elevated risk · Tier 2.** AI reads the notes and suggests a category. Staff check it, then a rule matches the kit number and updates its row. Show the IT follow-up on how the approved update would move between tools and what staff should do if the update fails. [Report](../examples/comms-practice-kit-notes-assessment.md) | `66EEE9ABC077` | `6683930910CC` |
| **Fire · Make the Friday office supply list.** “Can I get a list of anything at or below its reorder number?” | **Automation · Low risk · Tier 1.** A fixed comparison makes the list from the counts file. Staff check it and hand it to the office lead. [Report](../examples/fire-office-supply-list-assessment.md) | `14FF365AA3E8` | `95624A79E73A` |
| **Police · Find the right training forms.** “Could we have one place to find the latest forms? I keep getting different copies.” | **Further discovery · Elevated risk · Tier 3 hold.** IT should find out who owns the forms, where the current copies live, and whether the request includes completed forms or only blank ones. [Report](../examples/police-training-forms-assessment.md) | `C3CD0E92C5CC` | `ACFD5344338B` |
| **Emergency Communications · Draft a training room display guide.** “Give me a one-page draft from the notes we supply. Show where each step came from and flag anything that disagrees.” | **AI · Elevated risk · Tier 1.** The coordinator supplied a time baseline, source-note checks, ten made-up test sets, a manual fallback, and a staff approval step. The training lead tests the steps in the room before sharing. [Report](../examples/comms-display-guide-assessment.md) | `B760D6BFD09D` | `CD6265F34926` |

## Live walkthrough

1. Run the Police room calendar live. Show how the portal reuses an earlier answer. Point out that the rules finish after staff confirm the existing view, why they miss it, and all six required checks. The rehearsal took ten questions.
2. Open Fire badge access in the analyst dashboard. Compare its seventeen questions and show the data and consequence flags behind the Tier 3 hold. Use the saved export to show the follow-ups on failed checks and approval.
3. Keep the other cases ready for panel questions. The display guide shows where AI helps, the Friday supply list shows low-impact Automation, and the training-forms case shows when IT needs more information.

## Fire badge access

**Fire · Check badge requests for the records room.** Staff want the form to flag inactive staff, jobs outside the approved list, and temporary requests missing an end date. The records manager approves each request, and Building Security changes the badge. An incorrect badge change could expose confidential staff files.

The saved assessment shows **Automation · High impact if wrong · Tier 3 governance hold**. In **Solution by impact if wrong**, select **High** in the **Automation** row. Find assessment **`141FCEC95C66`** on the hosted dashboard or **`56D378C69ACA`** on the MacBook. [Generated Fire badge access assessment](../examples/fire-badge-access-assessment.md)
