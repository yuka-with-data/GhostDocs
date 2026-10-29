"""Generate a repository knowledge report using a local Ollama model."""

from pathlib import Path
import ollama

from ghostdocs.analyzer import analyze_project
from ghostdocs.prompts import load_system_prompt, prepare_analysis_prompt
from ghostdocs.scanner import scan_projects

# Set sensible defaults for small personal repositories.
DEFAULT_MODEL = "gemma4:e4b"
DEFAULT_CONTEXT_BUDGET = 24_000
DEFAULT_NUM_CTX = 16_384

def generate_report(
    project_path: str | Path,
    model: str = DEFAULT_MODEL,
    context_budget: int = DEFAULT_CONTEXT_BUDGET,
    num_ctx: int = DEFAULT_NUM_CTX,
) -> str:
    """Analyze a repository and return a Markdown report."""
    # Validate inputs before scanning or calling Ollama.
    project_path = Path(project_path)
    if not project_path.is_dir():
        raise ValueError(f"Project path is not a directory: {project_path}")
    if context_budget <= 0:
        raise ValueError("Context budget must be greater than zero.")
    if num_ctx <= 0:
        raise ValueError("num_ctx must be greater than zero.")

    # Scan and analyze the repository using the existing modules.
    documents = scan_projects(project_path)
    analysis = analyze_project(project_path, documents)

    # Prepare a compact context from the inventory, findings, and documents.
    repository_context = (
        f"Project inventory and findings:\n{analysis}\n\n"
    )

    for document in documents:
        section = (
            f"--- FILE: {document['path']} ---\n"
            f"{document['content']}\n\n"
        )

        # Stop adding files when the character budget is reached.
        if len(repository_context) + len(section) > context_budget:
            break

        repository_context += section

    # Prepare prompts for the local model.
    system_prompt = load_system_prompt()
    analysis_prompt = prepare_analysis_prompt(repository_context)

    try:
        # Generate the report with the configured Ollama context window.
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": analysis_prompt},
            ],
            options={"num_ctx": num_ctx},
        )
    except Exception as exc:
        # Provide a useful error without exposing a full traceback by default.
        raise RuntimeError(
            f"Could not generate a report using '{model}'. "
            "Check that Ollama is running and the model is installed."
        ) from exc

    report = response.get("message", {}).get("content", "").strip()
    if not report:
        raise RuntimeError("Ollama returned an empty report.")

    return report
