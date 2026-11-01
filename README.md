# 👻 GhostDocs

> A local-first documentation analysis tool that uncovers forgotten knowledge in software repositories using Ollama.

## What is GhostDocs?

Every software proejct accumulates knowledge over time. Some decisions go undocumented, old instructions become outdated, and important context gets lost.

`GhostDocs` helps maintainers investigate these potential knowledge gaps by analysing repository content with a locally Ollama model.

Its goal is to answer one question:

> What important knowledge has this repository lost, forgotten, or failed to document?

**Unlike traditional documentation linters**, `GhostDocs` focuses on understanding potential gaps in project knowledge rather than checking Markdown formatting or broken links.

## What It Does

- Scans repositories to discover relevant project files and documentation.
- Identifies potential knowledge gaps using rule-based analysis.
- Uses local AI analysis through Ollama to investigate findings and their context.
- Generates Markdown reports organized into three sections:
    - 👻 Lost Knowledge
    - 🕯️ Ghost Sightings
    - 🎃 Resurrection Plan

`GhostDocs` is designed to help maintainers reflect on what their projects might be missing and decide what deserves further investigation.
