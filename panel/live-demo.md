# Flagstaff WIP · Panel walkthrough

## Before the panel

Bring the MacBook and verify your HDMI or USB-C connection. Open the [PowerPoint](Flagstaff-Navigator.pptx), [PDF fallback](Flagstaff-Navigator.pdf), and [case guide](demo-cases.md). Start Flagstaff WIP from the project directory with `./scripts/demo-up.sh`. Open [the local interview](http://127.0.0.1:8878/) in one tab and [the local analyst dashboard](http://127.0.0.1:8878/analyst) in another. Sign in privately before sharing your screen. Confirm **Local AI ready** and Fire badge assessment **56D378C69ACA**. The [hosted dashboard](https://flagproject.chrisclark.tech/analyst) has the same case under **141FCEC95C66**.

Keep the room calendar assessment and Fire badge export open for the offline walkthrough. In the badge export, bookmark **Governance hold at submission** and **Interview record**. [Room calendar report](../examples/police-room-calendar-assessment.md) · [Fire badge report](../examples/fire-badge-access-assessment.md)

## Walkthrough and pacing cues

Use the time ranges as rehearsal cues. Give the panel the full explanation where it helps.

| Time | Show | What to say and do |
| --- | --- | --- |
| 0:00–0:20 | Slide 1 · Flagstaff WIP | Introduce the Work Improvement Portal. Say that all demo workflows and contacts are fictional. |
| 0:20–1:15 | Slide 2 · The business need | “The exercise asked for an AI agent. The business needs a clear path from what staff tell us to a decision IT can make. Sometimes that means showing people the report they already have.” A useful pilot would let IT route more requests on the first review. |
| 1:15–2:00 | Slide 3 · What the portal does | Point to the homepage and flow. Staff describe a task they think could improve and review their answers. They can download the assessment or use its ID to follow up. IT gets documented next steps. |
| 2:00–2:55 | Slide 4 · Requirements and scope | The exercise asks relevant follow-ups, checks risks and saves a usable assessment. Large-scale load testing is outside this exercise. Before a pilot, validate accessibility, concurrent use, access, retention, and recovery. A City system connection comes later if the pilot shows value. |
| 2:55–3:50 | Slide 5 · How the interview adapts | Walk through the six plain-language checks on the slide. Explain what “enough” means for an existing report, a new approach, and a request that needs more discovery. Use the [slide 5 talking points](#how-we-know-we-have-enough). |
| 3:50–4:30 | Slide 6 · How the assessment is designed | Show the original answers, the recommendation and risk, and who can act next. The export includes requirements, assumptions and open questions. A governance hold puts the first IT action at the top. |
| 4:30–5:20 | Slide 7 · What IT can do next | Walk through the routing table. An existing fit may call for training or access. Self-service goes to the department. Business Systems can evaluate rules, AI, or both. Further discovery gives someone an open question to resolve. A hold routes to IT triage first. The roles are proposed and the City would confirm them. |
| 5:20–5:55 | Slide 8 · Architecture choices | Describe capabilities before showing cases. Check existing tools, show the answers supporting the recommendation, identify what IT still needs to verify, keep approval with reviewers, and provide an offline path. |
| 5:55–6:35 | Slide 9 · Where Qwen helps | Explain the difference between opening-answer extraction, later follow-up selection and reuse across every answer. Qwen can read selected later answers to choose a follow-up. Written rules surface reusable details from each answer and decide when to finish. |
| 6:35–7:15 | Slide 10 · Technical overview | Name the stack, local Qwen model, and the two verified setups. Explain how one Compose command rebuilds the web app and keeps the SQLite data. Describe what would move to an approved Docker host. Use the [technical talking points](#technical-talking-points). |
| 7:15–8:00 | Slide 11 · Where the data goes | Trace the hosted route, including the encrypted tunnel and the two local HTTP hops. Explain what the app stores and what the model sees. Before real data, the City would need to approve protection, access and retention. Use the [security talking points](#security-talking-points). |
| 8:00–9:00 | Slide 12 · Pilot readiness and ownership | Tie the plan to the panel’s criteria. Verify routing and required checks with Qwen on and off. Load-test concurrent interviews and analyst reviews in staging, track p95 latency, errors and SQLite write contention, and reconcile a backup restore. Start with one department team and assign ownership across Business Systems, Service Desk and Platform Ops. |
| 9:00–9:15 | Slide 13 · DEMO | Pause on the divider and switch to the staff-facing browser tab. |
| 9:15–12:45 | Slide 14 and live Police interview | Start **Police** as **Jordan Example** at **jordan@example.invalid**. Follow the [room calendar answer card](#police-room-calendar-live-answer-card). Confirm that the weekly view exists and staff need help finding it. At the tools question, open **Why are we asking?** and point to the opening-answer quote. Explain how Qwen can help reuse details and how the rules decide when to finish. Confirm all six checks, pick **Low** benefit, submit, and copy the new ID. |
| 12:45–14:15 | Slide 15 and the assessment receipt | Open **View assessment details**. Show **Existing solution**, **Low risk**, and **Tier 0**. Find the answer about the weekly view and read the recommendation to show staff how to use it. The ID lets IT find the same record later. Use the [saved room calendar report](../examples/police-room-calendar-assessment.md) if needed. |
| 14:15–15:00 | Slide 16 and the six recommendations | Point to **Existing solution** for the room calendar and **Automation** for the Fire badge request. Give the panel a moment to scan the other outcomes. Move to the analyst dashboard for the longer interview and the hold. |
| 15:00–19:00 | Slide 17 and the live analyst dashboard | In **Solution by impact if wrong**, select the **High** cell in the **Automation** row. Open the Fire badge submission. For a direct lookup, use **56D378C69ACA** locally or **141FCEC95C66** hosted. Show the **Tier 3 hold** and expand **Governance checks from the assessment**. Open the badge export at **Interview record** for the additional questions. Use the [badge walkthrough](#from-the-short-interview-to-the-badge-hold). |
| 19:00–19:45 | Slide 18 · Decision for the panel | “Which workflow should we pilot and who owns it? What result would justify expanding?” |
| 19:45–20:00 | Buffer | Protect the assessment and dashboard segments. If a live step slows down, use the relevant saved report. Slides 19–20 are for the separate panel discussion. |

## How we know we have enough

“Enough means IT has a useful next step and can explain why. After each answer, written rules check whether another question is needed. Staff answer all six checks on the slide, plus a question about who checks the result when the case calls for it. The portal moves to **Review** once the questions for that path have answers. Staff can check or correct those answers before submitting.”

- **A tool already covers the need.** In the Police case, the weekly calendar view gives staff what they need. The portal asks what keeps them from using it. The six checks establish how the work uses information and whether IT needs to verify anything before it advances.
- **The task needs a new approach.** The portal asks what starts or repeats the work, what staff work from, whether the steps follow rules, what the result should be, and who would check it when needed. It can follow up about exceptions or parts that need a judgment call.
- **An open question needs an owner.** Police staff want the latest training forms but are unsure who owns them, where they live, and whether the request includes completed forms. **I’m not sure** is a valid answer to a governance check. It gives IT a specific fact to confirm, and the assessment holds the request while those checks are open.

For the live room calendar, say “Qwen can find the start, steps, and handoff in an opening answer so we can focus on what’s missing. Once we’ve confirmed the weekly view, learned why people miss it, and answered all six checks, the rules take us to Review.” The tools quote on screen is an example of the portal reusing an earlier detail. The saved calendar run took ten questions.

## Police room calendar live answer card

| Question | Short response |
| --- | --- |
| What task could work better for your team? | “When someone asks for a meeting room, I open the booking calendar and check rooms one at a time. Then I send the requester a room and time that’s available. It’s all in the booking calendar we already use. It takes too many clicks.” |
| How do you do this today? Or a question about the missing details | “When a request comes in, I look at each room one at a time. Once I see a free slot, I send the requester the room and time.” Use just the last sentence if the portal asks how the task ends. |
| Can a tool you already use do this? | **Yes.** “A coworker showed me the weekly view. It already shows which rooms are free side by side.” |
| What keeps staff from using it today? | **People need guidance or training.** “Most of us don’t know where to find the weekly view.” |
| What information would this change use? | **Only routine or public information, such as supply counts.** “Room names and whether each time is free or busy.” |
| Would information stay in one place or move between tools? | Open **Why are we asking?** and point to **From your answer to question 1**. Use **Include this detail**. Choose **It stays in one app or shared workspace.** |
| What would the tool need to do with the information? | **Only read information, run a report, or prepare a draft.** Staff only look at the calendar. |
| What could happen if the result were wrong? | **Someone could catch and fix it before it causes a problem.** Staff can check the room’s calendar again. |
| Who’s responsible for this work, and is this use allowed? | **We know who’s responsible for the work and the information, and this use is approved.** “The front desk lead runs room bookings. Our team is already allowed to see the weekly view.” |
| Could the result affect an emergency, safety, care, or legal decision? | **No, it only helps with routine work like tracking supplies.** These are ordinary office meeting rooms. |

## From the short interview to the badge hold

“The room calendar reached a useful next step in ten questions. The badge request took seventeen. IT needs to know exactly what the form would check, what staff do when a check fails, and who decides whether someone can enter the room.”

1. In the badge assessment, point to **Automation** and the **Tier 3 hold**. The form can flag missing or mismatched details. The records manager approves entry, and Building Security changes the badge.
2. Expand **Governance checks from the assessment**. Show **Data classification** and **Operational consequence**. The form uses private staff information, and a bad badge change could let the wrong person see confidential files. Read the first step for IT to confirm the data owner and approved environment.
3. At **Interview record** in the badge export, point to **Do staff follow the same rules each time?**, **What happens when the usual steps don't work?**, and **Will someone check the result before staff use it?** Those answers show the routine checks, the missing-date example, and who approves each request. [Badge assessment](../examples/fire-badge-access-assessment.md)

## The AI-only display guide

“An Emergency Communications training coordinator already spends about 45 minutes turning rough trainer notes into a one-page guide. They supplied what a useful draft would look like, who checks it, and how they would test it. Every suggested step needs a source note. If two notes disagree on the display input, the draft flags both and leaves the input number out until someone tries it in the room.”

- Show the [saved AI assessment](../examples/comms-display-guide-assessment.md), hosted **B760D6BFD09D** or MacBook **CD6265F34926**. It scored **9/10 for AI** and **3/10 for automation**. These are screening scores. Qwen helped with two follow-up selections, and the decision rules used the confirmed answers.
- Propose a test using ten sets of made-up notes with known expected results. Check source references, missing steps and conflicting notes. Time the full job with staff review and look for at least 15 minutes saved. Keep the current manual process available.
- In the guide case, staff check and share the draft themselves. The practice-kit case also has a fixed rule that updates the matching row after approval. Validate the kit ID, owner and recovery steps before connecting tools.

## Architecture talking points

- **Start with the workflow.** The weekly room view already answers the question. The remaining work is showing staff where to find it.
- **Reuse what staff tell us.** The tools question shows a quote from the opening answer. Staff still confirm the choice. A concrete example with an input and expected result can carry forward to the assessment.
- **Make recommendations traceable.** The badge form uses repeatable checks. The original answers show why Automation fits and why private staff information and physical access still need review.
- **Build in governance.** Staff can choose **I’m not sure** on any required check. The training-forms report gives IT questions about who owns the forms, where the current files live, and which records people expect to see.
- **Design for support and failure.** Use one app, SQLite, and an optional local model. Show that the local interview and download work without internet and that the rules can run with the model disabled.

## Technical talking points

- **Application.** “I built and tested the app in short iterations with AI assistance. The backend uses Python’s standard library. The browser uses HTML, CSS, and plain JavaScript. SQLite stores the interviews and reports. The Docker image pins Python 3.13.” [Dockerfile](../Dockerfile) · [Development record](../docs/development.md)
- **Local model.** “The model is Qwen2.5-1.5B-Instruct in a 4-bit GGUF file, served by llama.cpp on Apple Silicon. The Mac mini runs inference alongside Docker in a separate host process. The app can also run on its built-in rules.” [Model installer](../scripts/install-model.sh)
- **Does Qwen read later answers?** “Yes. For follow-up selection, Qwen can read selected later answers and choose up to two questions from the options the rules allow. It extracts the current workflow from the opening answer. Written rules look for reusable details in every answer. The analyst summary can use the opening request and the later answer about what staff want at the end.” [Model calls](../navigator/local_model.py) · [Answer reuse rules](../navigator/prior_answers.py)
- **Deploy and update.** “The Mac mini is an M1 with 16 GB of RAM. Docker Compose runs the app and keeps its database in a persistent volume. The MacBook can run the app and model directly for the offline demo. After setup, `docker compose up -d --build --wait` rebuilds the app and checks readiness.” [Operations guide](../docs/operations.md)
- **Move it to another host.** “An approved Docker host could use the same build and a persistent SQLite volume. The app can point to a compatible private model endpoint or run with built-in rules. I’d validate capacity, network access and database recovery on that host before a City pilot.” [Architecture](../docs/architecture.md)

## Security talking points

- **Follow the data.** “The browser uses HTTPS to Cloudflare, which can see the request contents. The tunnel to the Mac mini is encrypted. Once traffic arrives, the connector talks to the app over local HTTP and the app talks to Qwen over local HTTP.”
- **Explain what the AI sees.** “Qwen reads the opening response to spot the start, steps and finish. For later follow-ups, it sees eligible topics and brief answer excerpts. For the analyst summary, it sees short excerpts of the goal and desired result. The app’s rules own classification and governance.”
- **Say what is stored.** “The app saves drafts and assessments in SQLite. Those records and exports have no application-level encryption. FileVault was on for the MacBook and off for the Mac mini when checked. Analyst sign-in uses salted hashes and expiring sessions. The name and email are stored separately and stay out of AI prompts and assessment exports.”
- **Name the next design decision.** “The exercise is limited to fictional data. For a City pilot, I’d get approval for the data boundary and encryption, then agree on identity, access, logging and retention before accepting records.”

## Thirty-minute panel discussion

Use slide 19 for the AI display guide trial and slide 20 for pilot test priorities. The [panel criteria review](../docs/panel-coverage.md) maps the eight exercise criteria to the app, slides and verification evidence.

- **When to hold off on a solution.** Ask the Police training lead to name who maintains the forms and what a current copy means before choosing a tool.
- **Value and scope.** Compare first-pass routing and rework with existing intake. Validate the staff benefit estimate and the early effort estimate before committing resources.
- **AI use and a human correction.** AI helped draft and test the logic. A rehearsal showed that routine workflows asked too many follow-ups. I shortened that route, kept the required checks, and gave analysts the question and staff answer behind each review reason.
- **Source authority and exceptions.** Verify the guide against the original notes and in the room. For Hybrid, confirm that the practice-kit log owns kit IDs and decide who can correct a failed or mismatched update.
- **CJIS and HIPAA.** The exercise uses fictional data. The Fire badge hold illustrates private staff data and physical access review. Before a pilot, confirm legal applicability with City Security, Privacy, Records and Legal, then agree on access, retention, logging and escalation.
- **Rollout and ownership.** Business Systems maintains prompts and decision rules. The department owns the workflow. Service Desk handles first response and platform operations owns uptime and recovery. Agree on who can pause a pilot and how to return to manual intake.

## Recovery during the walkthrough

If the local model is unavailable, answer the standard current-work question and finish the room calendar interview with the rules. The earlier tools quote and the six checks still work. If the app is unavailable, use slides 3 and 14 for the staff screens, slide 15 for the room calendar assessment, and slide 17 for the question counts and hold screenshot. Open the Fire badge report at **Governance hold at submission**, then show the longer transcript at **Interview record**. Use the local PDF if PowerPoint is unavailable. [Room calendar report](../examples/police-room-calendar-assessment.md) · [Fire badge report](../examples/fire-badge-access-assessment.md) · [Offline PDF deck](Flagstaff-Navigator.pdf)
