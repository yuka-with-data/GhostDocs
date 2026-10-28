""" Generate a repository knowledge report using a local Ollama model. """

from pathlib import Path
import ollama

from ghostdocs.analyzer import analyze_project
from ghostdocs.prompts import load_system_prompt, prepare_analysis_prompt
from ghostdocs.scanner import scan_projects

# Set default for the local model and repo-context size.
DEFAULT_MODEL = "gemma4:e4b"
DEFAULT_CONTEXT_BUDGET = 24_000

def build_repository_context(
        project_path: str | Path,
    documents: list[dict[str, str]],
    analysis: dict,
    context_budget: int = DEFAULT_CONTEXT_BUDGET,
) -> str:
    """ Build a prioritized repository context within a character budget. """
    pass
