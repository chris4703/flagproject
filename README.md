# Flagstaff WIP · Work Improvement Portal

City of Flagstaff Business Systems Architect II final interview exercise. Flagstaff WIP interviews Police, Fire and Emergency Communications staff about one fictional workflow and produces an IT triage assessment. It can recommend an existing feature, self-service, automation, AI, a hybrid, or further discovery.

## Panel materials

- [The Brief](presentation/The-Brief.html)
- [Analyst quickstart](presentation/Flagstaff-WIP-Analyst-Quickstart.html)
- [Panel handout](presentation/Flagstaff-WIP-Panel-Handout.pdf)
- [Flagstaff slideshow for Keynote](presentation/Flagstaff-Slideshow.key)

For the HTML handouts, download and extract the repository ZIP, then open the files in `presentation/`. Keep the linked folders beside `The-Brief.html` so its PDFs and Markdown files open. Open the slideshow in Keynote.

## Analyst dashboard

Open [the hosted analyst dashboard](https://flagproject.chrisclark.tech/analyst) or follow **Analyst dashboard** in the interview footer. Sign in as `analyst` using the password provisioned for that copy. The dashboard filters completed reports, compares staff-estimated benefit with indicative effort, and shows consequence, risk, governance and solution fit separately. Counts link to matching submissions. **Find assessment** opens the saved submission by its receipt ID. **Request at a glance** summarizes the result staff want in plain language using the local model. Signed-in analysts can change the IT review status, see the follow-up contact, or draft an email with the assessment ID. Download a full assessment or a filtered CSV. See [analyst operations](docs/operations.md#analyst-access).

## Run the demo

Open [the hosted portal](https://flagproject.chrisclark.tech) from any browser. On the prepared MacBook, run `./scripts/demo-up.sh` from this directory and open [the local portal](http://127.0.0.1:8878). The panel walkthrough pairs a live room calendar interview with the saved Fire badge governance hold. To repeat a case, open **Try a practice scenario**. The Mac mini runs the same app in its own Docker Compose project on port 8878. [Case guide](panel/demo-cases.md) · [Installation and Docker deployment](docs/operations.md)

| Deliverable | Open |
| --- | --- |
| Written exercise brief | [PDF brief](panel/Project-Brief.pdf) and [Markdown source](docs/project-brief.md) |
| Sample produced by the deployed app | [Fire staff renewal view](examples/fire-renewal-view-assessment.md) shows a small self-service change held for a review of private staff information. |
| Current demo cases | [Case guide and seven saved reports](panel/demo-cases.md) |
| Architecture and implementation | [Technical design](docs/architecture.md) and [release verification](docs/verification.md) |
| Interview materials | [Workflow evidence prompt](inputs/process.md), [follow-up prompt](inputs/interviewer.md), [analyst summary prompt](inputs/summary.md), [question bank](navigator/questions.py), [fictional scenarios](inputs/scenarios.json) and [development prompts](docs/development.md) |
| Presenting the exercise | [PowerPoint](panel/Flagstaff-Navigator.pptx), [PDF slides](panel/Flagstaff-Navigator.pdf), [walkthrough](panel/live-demo.md), and [panel criteria review](docs/panel-coverage.md) |


For the interview exercise, use invented workflow and contact details. The assessment identifies who should review a proposal and what evidence they need. The demo has no City accounts, live integrations, ticket creation, or City compliance approval.
