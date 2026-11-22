# Release verification

Verified November 19, 2026, Arizona time. All test descriptions were invented.

| Check | Observed result |
| --- | --- |
| Six solution classes | Unit tests passed for existing solution, self-service, automation, AI, hybrid and further discovery. Tests also covered mandatory questions, uncertain governance, and a consequential decision boundary. |
| Fire, Docker and local model | Record **193D1B5FD342**. Hybrid, Elevated, Tier 1. 19 answers and two local AI follow-up selections. The staff example identifies a late and conflicting note for review. |
| Police, Docker and browser | Export **6C9FE4EF5651**. Existing solution, Low, Tier 0. Finished in 10 questions with the mandatory checks. A separate browser run showed review and an assessment with a Markdown download. |
| Emergency Communications, Docker and local model | Record **39A72E78FCB1**. Automation, High, Tier 3. The generated report held advancement for data classification, potential CJIS and HIPAA applicability, and unresolved authorization. |
| Rules fallback | With inference disabled, the three sessions reached the same solution fit, risk and IT tier and downloaded complete reports. |
| MacBook offline | The app, local model and test client ran with outbound access permitted only on loopback. A public internet request failed under the same restriction. All three live sessions completed and downloaded locally. The Fire run recorded two model selections. |
| Review and repeat requests | The live tests rejected an early export and a stale update, retained the last response when navigating back, and confirmed that the saved assessment matched the downloaded record. |
| Public HTTPS | Through the Cloudflare edge at `flagproject.chrisclark.tech`, the three cases completed with browser-style HTTPS Origin headers and downloaded their reports. Fire **8B62BB4A2502**, Police **ED3FBA07230E**, Emergency Communications **12121765CBA8**. |
| Mac mini isolation | The new service used Compose project `flagcity-navigator`, host loopback port 8878 and volume `flagcity-navigator_navigator_state`. The existing `flagcity` container kept its container ID, startup time, volume and original hostname. |

In rules version 1.1.0, a fresh custom interview reached Self-service in **15 answers**, a second reached Automation in **15**, and a case with unsettled rules reached Further discovery in **11**. Potential CJI and an operational consequence added the required human-oversight question and preserved a hold. Selecting an external service reopened exception questions and ended in a governance hold. The same cases passed on the Mac mini and MacBook. The sample records in the table above are preserved exports from version 1.0.0.

The exercise establishes working triage and recovery when local inference is unavailable. A City-approved pilot still needs usability and accessibility testing with staff, representative concurrency and response-time measurements, review of security and retention, and a witnessed restore.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/rehearse.py --require-model
```

## Custom browser rehearsals and analyst dashboard

Three newly written, detailed fictional workflows were submitted as custom interviews through the real browser on the MacBook and again on the Docker deployment through a local SSH tunnel. The Mac mini records are visible in the hosted analyst dashboard. The expected classification, reported risk, IT route and governance status matched across both runs.

| Workflow | Questions | Result | Branch and follow-up evidence |
| --- | --- | --- | --- |
| Police radio charger returns | 10 | Existing solution, Low risk, Tier 0 department-led | The next question after confirming the saved report asked why people were missing it. All six required screening questions ran before review. Mac mini record **EA3A01AFD0BB**. |
| Fire training classroom restock | 15 | Self-service, Low risk, Tier 0 department-led | The predictable output, single team and approved spreadsheet completed the routine route. No unrelated interpretation or example question appeared. Mac mini record **57361FF277A9**. |
| Emergency Communications headset inspection corrective-action review | 19 | Hybrid, High risk, Tier 3 hold | Once the input revealed variable comments, missing labels and conflicting notes, the model picked a concrete example and then human judgment. Output, exceptions and prior approval were confirmed before review. Mac mini record **A25BB694C1B0**. |

The dashboard was tested in a browser for incorrect credentials, sign-in, matrix drill-down, report preview, matching CSV filters and sign-out. HTTPS checks verified that anonymous users cannot fetch analytics or exports, cross-origin logins are rejected, session cookies use secure attributes, and logout invalidates the session. The high-benefit, high-effort filter returned the expected held Hybrid submission and the CSV agreed with the dashboard count.


## Official exercise crosswalk

| Required by BSAII_Final_Exercise.docx | Where to verify |
| --- | --- |
| Working AI skill or agent, prompt and Markdown inputs | Run the [hosted Navigator](https://flagproject.chrisclark.tech) or use the [installation guide](operations.md). The [runtime prompt](../inputs/interviewer.md) is loaded by the app. [Development prompts and inputs](development.md) documents the inputs and human corrections. |
| One completed sample from an actual run | The [headset inspection assessment](../examples/comms-headset-inspection-assessment.md) is the current application download from browser record **A25BB694C1B0**. The [PDF reading copy](../panel/Headset-Inspection-Assessment.pdf) contains the same report. |
| Written brief | The [brief](../panel/Project-Brief.pdf) covers the problem, stakeholder questions paired with assumptions, priorities, scope and exclusions, risks, phases, rollout and who owns the system over time. |
| Nontechnical staff and fictional data | The staff interface uses plain-language questions. The [brief](project-brief.md#risks-governance-and-source-authority) covers CJIS and HIPAA review, with fictional descriptions throughout. |
| 20-minute live walkthrough, a 30-minute panel discussion and offline fallback | The [deck](../panel/Flagstaff-Navigator.pptx) and [script](../panel/live-demo.md) cover the live Police interview, three distinct results, the actual dashboard, architecture and ownership. The MacBook has the exact three sample reports. The local PDF and offline Markdown exports back up the browser. |
| Explain how AI was used and where judgment changed the design | The [development record](development.md#what-i-would-discuss-about-using-ai) and [discussion prompts](../panel/live-demo.md#thirty-minute-panel-discussion) cover the limits on the model and the shorter route introduced after browser testing. |

## Submission receipt and IT follow-up

Version 1.3 collects name and email at the start of a custom interview. A browser test submitted a sample, copied the assessment ID, opened the exact ID as a signed-in analyst, and marked it reviewed. Reloading the participant’s receipt showed the updated review status. The hosted HTTPS and MacBook API tests verified that anonymous requests cannot read contact details or mark records reviewed, repeated review requests preserve the first review time, and contact fields are absent from public responses and exports. The analyst details provide a mail draft link for manual follow-up. Sample contacts and workflow details used for verification were invented.

## Request at a glance

Version 1.4 generated summaries for all three saved cases in the signed-in analyst view. In the browser, Police described the borrowed chargers and help using an existing feature, Fire described the list of supplies below minimum, and Emergency Communications described the headset follow-up list and human approval before tools share updates. The original recommendations appeared below each summary. Hosted HTTPS checks verified that the summary requires sign-in and rejects requests from another origin. Reopening the report used the saved summary. With local inference disabled and no saved summary, the assessment showed the original goal excerpt and the approval condition.

## Panel feedback rehearsal

On November 20, 2026, the browser showed the editing notice during the Fire interview and again before submission. After answering **What do you work from?**, the local model selected the follow-up **Where does someone have to interpret information?** The browser also verified that the saved headset assessment placed the first IT action above the Hybrid recommendation and displayed the question and answer behind its data classification check.

The Mac mini produced three fresh exports, including the Fire drill case **AF07A1A1FBD4** and the held retrospective queue **B37DE05ED967**. The held download places the first action above the recommendation and lists Information Security once with its assigned checks. The 0–10 values are labeled screening scores. The app, model and rehearsal client also completed all three scenarios on the MacBook under a loopback-only network policy.

## Staff experience

Browser testing verified that a custom Police intake saved after 10 answers, Back restored the previous answer, and the receipt provided a copyable assessment ID and expandable assessment. At a 390-pixel browser width, the practice Emergency Communications intake reached a receipt with its first governance action visible. The Fire, Police and Emergency Communications rehearsal cases kept their expected classifications, risk levels and IT involvement on the hosted build.

## Workflow follow-up

Browser tests using the local model covered three opening answers. A complete description passed through to the existing-tool question and reached the Police assessment after nine answers. A partial description prompted only for how the task finishes. A proposed tool by itself prompted for the full current workflow. The saved Police assessment showed excerpts from the opening answer. Automated tests checked the no-model fallback, edits, and all six required governance checks.

## Earlier answers and Flagstaff WIP

Version 1.6.0 carried an opening data detail into a later governance question and offered an excerpt from the second response when asking about inputs and human review. A fictional Fire interview completed in 18 questions. It retained all six governance checks and the human review question. Review and the generated Hybrid assessment cited the opening example as an acceptance test instead of asking for it again. Tests verified that an incomplete example still gets a follow-up and revising an earlier answer clears its context. The Fire, Police, and Emergency Communications rehearsals retained their expected outcomes with the local model enabled and disabled. The staff and analyst pages displayed Flagstaff WIP on the hosted and local copies.

## Plain-language staff questions

Version 1.7.0 adds visible optional notes and a collapsed “Why are we asking?” explanation on each question. A fictional Police browser rehearsal reused a detailed opening answer, carried a note about training into the next question, and finished in nine questions with all six required checks. The response “I’m not sure” about ownership and permission kept the existing-feature recommendation and placed advancement on hold for IT. Automated tests confirmed that staff can submit without filling in optional notes and that an unknown data category goes on hold.

## Fire classroom setup recap

The team wants a draft recap from free-form classroom logistics notes. A coordinator verifies each point against the original notes before sharing. The [generated assessment](../examples/fire-classroom-recap-assessment.md) scored 9/10 for AI and 3/10 for automation. It recommended AI and IT advisory review, recorded Elevated risk, and flagged human oversight for review. The hosted and MacBook copies saved custom assessment **39670BB9AB0E** and **FF0B78BE432A**, respectively. The dashboard aggregate on each copy counted one AI recommendation, including under Custom interviews.

The practice scenario reached the same recommendation, risk level, and IT tier with local inference enabled and disabled. Both runs retained the six required governance checks and human review before use. The three earlier practice scenarios kept their expected outcomes in both rehearsals.

The analyst view and Markdown download show plain-language next steps for the saved classroom recap on both deployments. The rules supply the steps using fixed wording, so the same instructions appear with local inference disabled. Qwen still writes the short request summary from intake answers. With the revised prompt it returned “Staff want a draft to capture classroom setup and handout changes for the next instructor.”

## Five new panel cases

Version 1.8.0 replaces the public practice cases. The Mac mini and MacBook databases were backed up and verified, then both dashboards showed zero completed submissions before the five new cases were submitted. The [current case guide](../panel/demo-cases.md) records both sets of IDs. The classifications, risk levels and IT tiers matched with Qwen enabled and disabled. The staff renewal case showed Self-service with a mandatory data review, and the practice-kit case recorded two local model follow-up choices when Qwen was available.

## AI display guide and panel walkthrough

The sixth case, [draft a training room display guide](../examples/comms-display-guide-assessment.md), scored 9/10 for AI and 3/10 for automation. It reached AI, Elevated risk, Tier 1 with human oversight review both with and without Qwen. The hosted record **B760D6BFD09D** and MacBook record **CD6265F34926** each took 18 questions and included two local AI follow-up selections. The staff answer identifies a 45-minute baseline, ten made-up test sets, and a target of at least 15 minutes saved including review.

A browser rehearsal completed the custom Police room calendar case in ten questions. It verified the opening quote at the tools question, the question help, and the receipt ID. The signed-in analyst rehearsal checked the six dashboard categories, opened the Fire renewal hold, and verified the data classification evidence. The revised slides and walkthrough use those cases.

## Fire badge access practice case

The seventh scenario recommends automated checks for an incoming request. The records manager still approves access and Building Security makes badge changes. The hosted report **141FCEC95C66** and MacBook report **56D378C69ACA** completed in 17 questions. Both recorded Automation, High impact if wrong, High risk, and a Tier 3 governance hold for the staff data and the consequences of a wrong badge change. The rules-only rehearsal produced the same result. [Hosted assessment export](../examples/fire-badge-access-assessment.md)

The panel walkthrough now pairs the ten-question Police room calendar with the seventeen-question Fire badge case. The analyst browser check verified the Automation and High impact filter, the two reasons for the badge hold, and the exported questions about rules, failed checks, and human approval. [Demo script](../panel/live-demo.md)
