# Development prompts and inputs

## Prompts used to drive the build

1. **Assignment source.** Use Shawn Armour’s final exercise for the required runnable agent, a completed output from a real session and the written brief. Use invented data and prepare for a 20-minute live walkthrough plus 30 minutes of questions.
2. **Product direction.** Build a fresh, isolated Docker project based on the adaptive “20 Questions” conversation. Screen for existing capability, self-service, automation, AI, hybrid or discovery. Assess risk and IT involvement independently. Complete mandatory data, access, stewardship and consequence checks even when the interview ends early.
3. **Implementation direction.** Keep the demo offline with local inference. Restrict the model to choosing from a finite question bank, enforce policy in server rules and generate the report from reviewed answers. Compare a fictional Fire hybrid candidate, Police reuse opportunity and Emergency Communications governance hold.
4. **Presentation direction.** Explain the choices as a business systems architect would, through outcomes, people, data authority, verified quality, technology and cost, rollout and ownership. Use the regular workflow, an exception and a stalled request to make those choices concrete.

## Inputs used by the application

- [Follow-up prompt](../inputs/interviewer.md) names the valid question choices and priorities. [Request summary prompt](../inputs/summary.md) asks the same local model to restate the requested outcome in plain English.
- [Question bank](../navigator/questions.py) includes question IDs, labels, help and a plain-language example per topic.
- [Fictional scenario inputs](../inputs/scenarios.json) are displayed one question at a time when staff choose to fill an example. They use the same workflow and reporting code as a custom interview.
- [Assessment policy](../navigator/assessment.py) determines the outcome and generates the artifact. The [exercise brief](project-brief.md) and [technical design](architecture.md) document the design choices.

## What I would discuss about using AI

I used AI assistance to develop and test the application. I narrowed the model’s runtime authority to follow-up selection so it could help staff surface evidence while policy stayed testable. During review, the first Fire export repeated punctuation in a requirement and rendered AI as “Ai.” I corrected the formatter and ran all three scenarios again. The structured branch also needed a follow-up when a staff member first revealed the need for interpretation in the desired output. The state machine now asks about judgment even when the earlier input was described as structured.

A browser rehearsal exposed another issue. Most new workflows still ran through nearly every available follow-up even when the answers supported a simple route. I shortened the path for straightforward administrative cases and kept the mandatory governance checks. Earlier exits and the resulting classifications were then verified in the browser.

The first headset summary implied that fewer approval steps were part of the request. I narrowed the prompt to the outcome staff wanted and used confirmed intake choices for the tool connection and approval wording. The analyst can still read the full answers and review the rule-based recommendation below the summary.

The [workflow evidence prompt](../inputs/process.md) looks for excerpts covering the start, steps and finish of a task in the first answer. The server checks the excerpts and asks about missing details. Staff proposals remain in the original answer for IT review.
