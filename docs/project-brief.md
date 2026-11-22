# Flagstaff Public Safety Workflow Discovery

**Business Systems Architect II final interview exercise | Project brief**

## Problem and intended outcome

Public Safety staff know their workflows. IT needs a practical way to discover which problems merit attention across Police, Fire and Emergency Communications. The management brief asks for an AI agent and an actionable output. The first business decision is whether an existing capability, a process change, a team-managed tool, or an IT investigation is the right next step.

A good intake gives IT the current steps, the exception that matters, the desired result, and a responsible reviewer. It distinguishes technical fit from permission to proceed. Measure the share of pilot assessments IT can route on first review without asking staff to explain the workflow again. Compare with a small set of comparable current intake cases and record why cases are sent back.

## Stakeholder questions and working assumptions

- **What decision should IT make on first review?** Assume IT can route, request one named piece of evidence, or close with a reason.
- **Where is workflow delay and who owns the outcome?** Assume a department supervisor owns each workflow. Time and volume in the interview are rough estimates to validate with frontline staff and representative cases.
- **What tools and support already exist?** Assume application owners and Service Desk can confirm features, licenses, configurations and approved tools. Fictional software names represent no City system.
- **Which source owns an important record, and who resolves conflicts?** In the drill example, assume the tracker owns the official training status, the station note is supporting evidence, and a supervisor resolves disagreements. Verify all three with the process and data owners.
- **How does IT receive and dispose of an assessment?** Assume a designated analyst uses the existing intake channel manually and returns the outcome to the requestor. Confirm review roles and retention with the City.
- **What can be handled in discovery?** Assume invented descriptions, no uploads, staff accounts, live records or direct integrations. Use invented name and email values to test follow-up. A real pilot requires written authorization, classification and retention decisions.
- **How much interruption can staff absorb?** Assume short, interruptible administrative sessions on existing browsers. Test with staff from all three departments, including people using keyboard navigation or assistive technology.

## Requirements and acceptance

- **Must | Adaptive intake.** Ask one question at a time, show examples, accept unknowns and stop after enough evidence and required checks. An existing-feature case can finish in 10 questions and a straightforward new workflow in 15. A complex case draws from the 20-question bank.
- **Must | Decision consistency.** The same confirmed answers produce the same solution class, risk, IT tier and hold. Verify all six classes and compare model-on against model-off runs. Risk and governance can hold an otherwise feasible idea.
- **Must | IT handoff.** Before generation, staff review and can revise an answer. The persisted report contains trigger and steps, systems, volume, output and exceptions as available, assumptions, open questions, requirements, rationale, checks and role-owned next actions. Confirm submission with a short assessment ID the analyst can look up for follow-up. Confirm that a stale action cannot replace a newer answer.
- **Must | Offline operations.** After setup, finish and download an assessment while disconnected. If local inference is absent, finish the same case using rules. No API key, remote font, CDN or City integration may be required.
- **Must | Data boundary.** Use synthetic descriptions and contact details without attachments. Keep name and email in a separate table available to signed-in analysts. Ensure local access by default and avoid recording the transcript or session keys in request logs.
- **Should | Accessibility and performance.** Verify a keyboard-only interview, labeled controls and 200% zoom without horizontal page scrolling. Pilot targets are 90% of routine turns under one second on the approved host and an automatic fallback when a local inference call exceeds six seconds. Validate under representative concurrent use before selecting infrastructure.
- **Should | Operational recovery.** Test return to manual intake and restoration from a database backup. Before a pilot, agree on retention, recovery point/time and how to reconcile assessments created after a restore.
- **Later | Intake integration and reporting.** If manual routing proves useful, test mapping to the approved service desk tool, idempotent delivery, reconciliation, disposition capture and a correction audit trail.

## Scope and exclusions

The proof of concept covers one administrative workflow per session, fictional scenarios, local conditional questioning, report preview and Markdown download. An application owner can inspect the reported capability without a software project. The analyst dashboard supports a single demo analyst account and reads completed assessments. Out of scope are uploads, real personal or operational records, staff accounts, system connectors, vendor procurement, replacing the City’s intake, automated ticket creation, and production hosting. Live dispatch, enforcement, clinical care and autonomous decisions affecting rights or safety are excluded from any solution delivered by this exercise.

## Decision design and technology trade-offs

Report three outputs separately. **Solution fit** checks for current capability first. For new opportunities, explicit rules, trigger, structured inputs, predictable output and manageable exceptions contribute up to ten automation points. Interpretation, contextual judgment, draft value and variability contribute up to ten AI points. Six points is a screening threshold. Reviewable interpretation and prior human approval are required for AI or hybrid. For eligible routine team work, an approved tool and existing access can qualify as self-service. Missing process evidence can send the case to discovery.

**Risk** reflects data exposure, system permissions, consequence and oversight. **IT involvement** ranges from department-led (0), through advisory (1) and technical delivery review (2), to mandatory governance review (3). A hold explicitly names the reviewer and blocks a pilot recommendation from advancing, even when the technical fit remains visible.

Reuse an existing feature first. Evaluate configuration or an approved low-code tool when it meets access, cost and support requirements. A purchased product would have to demonstrate the required behavior using synthetic inputs, a failed connection, a duplicate event and a recoverable correction before commitment. The exercise uses a small Python app, SQLite and one optional local model to avoid a queue, hosted database, model subscription and external service dependency. The trade-offs are local installation, model patching, single-host capacity and manual handoff. An approved City platform may be a better long-term home after a pilot.

## Risks, governance and source authority

- **CJI.** The designated City CJIS contact and information security team determine CJI scope and applicable agency requirements. Map storage, transfers, audit access, incident response, vendor access and the authorization boundary before introducing real data. [FBI CJIS Security Policy](https://le.fbi.gov/file-repository/cjis_security_policy_v6-0_20241227.pdf)
- **PHI and ePHI.** City Privacy and Legal determine whether a covered function or business associate is involved, which information is protected, and what safeguards and agreements apply. Local inference alone supplies no compliance determination. [HHS covered entities and business associates](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html) · [HHS Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)
- **Wrong outputs and duplicate work.** The Fire sample’s tracker is the assumed official record. A mismatch or late note goes to supervisor review. Pilot acceptance would require no duplicate follow-up for a retried input, a visible source for every proposed match, and a way to return to the manual list.
- **Model errors and unreliable intake.** The model can prioritize a less useful follow-up or summarize a request imprecisely. Staff verify the answers. Analysts can read the confirmed workflow below the summary and correct the disposition in the pilot’s intake record. Proposed production controls include role-based access, authorized output review, auditable overrides and data minimization.
- **Staff trust and service load.** Pilot with a department champion, a Service Desk contact and a simple way to correct the assessment. Confirm who handles stranded work, who can stop the pilot and how staff resume the existing process.

## Phased delivery and ownership

1. **Exercise — demonstrate.** Run the Police reuse interview live. Compare the Fire self-service assessment and the Emergency Communications Hybrid recommendation on hold. Demonstrate the offline path. Business Systems owns rules, tests and prompt changes.
2. **Authorized pilot — validate.** Invite one administrative team through a department champion. Introduce the tool in a staff huddle and publish a short Service Desk guide. Review every assessment alongside the current intake. Agree on accessibility, retention, escalation, backups, recovery and who can pause the pilot before opening access. Use comparable baseline cases and review first-pass routing, completion time, missed risk flags and override reasons. Pause if a restricted workflow advances without review or staff cannot reconcile reports on restore.
3. **Measured expansion — decide.** Expand only once the pilot improves triage without weakening screening. The department owns workflow facts and staff training. Business Systems owns decision rules, release review and triage quality. Service Desk owns first response. Platform operations owns host patching, monitoring and recovery. Security, Privacy, Records and Legal own their approvals. Review overrides and evidence monthly during the pilot, then quarterly if stable.

The architect remains involved through the first releases and the pilot review. Before leaving the project, walk through a real support incident with the owning team and agree on the changes supported by the evidence.

**Design references** [Microsoft architecture responsibilities](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/fundamentals) · [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard)
