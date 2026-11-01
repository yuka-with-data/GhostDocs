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

## How It Works

`GhostDocs` combines repository scanning, rule-based analysis, and local AI to generate a documentation analysis report.

1. Scan: Discover relevant files in the target repository.
2. Analyze: Identify potential knowledge gaps and unfinished business.
3. Build context: Prepare repository findings for AI analysis.
4. Investigate: Use Ollama to examine the findings and their supporting context.
5. Generate: Produce a Markdown report with observations and suggested actions.


## Requirements

- Python 3.12 or newer
- Ollama installed and running locally
- An Ollama model downloaded and available locally.

The default model is `gemma4:e4b`. To use another installed model, pass its name with the --model option:

```bash
# Example: use another locally installed Ollama model.
ghostdocs . --model llama3.2
```

## Installation

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```bash
# Create a virtual environment.
python -m venv .venv

# Activate on Windows PowerShell.
.venv\Scripts\Activate.ps1

# Or activate on macOS/Linux.
source .venv/bin/activate
```

Install `GhostDocs`:

```bash
# Install GhostDocs and its dependencies.
python -m pip install .
```

## Usage

Run `GhostDocs` from your terminal:

```bash
# Analyze the current repository.
ghostdocs .

# Analyze a different repository.
ghostdocs path/to/project

# Save the report as a Markdown file.
ghostdocs . --output reports/ghost-report.md

# Use a different installed Ollama model.
ghostdocs . --model llama3.2

# Display available CLI arguments.
ghostdocs --help
```

### CLI Options

| Argument       | Required | Description                                    |
| -------------- | -------- | ---------------------------------------------- |
| `project_path` | Yes      | Path to the repository to analyze.             |
| `--output`     | No       | Path to save the generated Markdown report.    |
| `--model`      | No       | Ollama model to use. Defaults to `gemma4:e4b`. |
| `--help`       | No       | Display available commands and options.        |

If `--output` is omitted, the report is printed directly in the terminal.
