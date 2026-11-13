# GhostDocs Architecture

This directory contains the core modules responsible for scanning repositories, analyzing documnetation, organizing findings, and generating AI-assisted knowledge reports.

## Module Responsibilities

| Module | Responsibility |
| ------- | ---------------- |
| `scanner.py` | Scans repository files and collects their content. |
| `analyzer.py` | Collects project inventory and detects basic documentation issues. |
| `findings.py` | Normalizes, categorizes, and structures evidence from analyzer results. |
| `generator.py` | Prepares repository context and uses a local Ollama model to generate Markdown reports. |
| `prompts.py` | Loads system instructions and prepares analysis prompts. |
| `cli.py` | Provides the command-line interface for running GhostDocs. |

## Processing Workflow

```txt
Repository
    ↓
scanner.py
    ↓
analyzer.py
    ↓
findings.py
    ↓
generator.py
    ↓
GhostDocs Report (.md)
```

## Design Principles

- Seperation of Responsibilities: Each module has a clearly defined role.
- Evidence-Based Analysis: Findings should be supported by repository evidenc.
- Local-First AI: Report generation uses a locally running Ollama model.
- Extensibility: New detection capabilities can be added without necessarily complicating existing modules.
