# Appendix C — Prompts and development notes

Flagstaff WIP uses three Markdown prompts at runtime. Open the original files below to see what the app asks Qwen to do.

| Original file | Purpose |
| --- | --- |
| [inputs/interviewer.md](../inputs/interviewer.md) | Selects a follow-up from the eligible questions supplied by the app. |
| [inputs/process.md](../inputs/process.md) | Extracts exact details about the start, steps, and finish of the current task from the opening answer. |
| [inputs/summary.md](../inputs/summary.md) | Drafts the plain-language request summary for IT. |
| [docs/development.md](development.md) | Records the build directions, input files, and corrections made during testing. |

The [standalone HTML brief](../presentation/The-Brief.html) also has inline previews and download links for all four original Markdown files. Download the HTML and open it in a browser to use those controls. The [fictional scenario inputs](../inputs/scenarios.json) and [question bank](../navigator/questions.py) are available in this repository.
