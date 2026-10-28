""" Load and prepare GhostDocs prompt templates for repository analysis. """

from pathlib import Path

# Locate the prompt templates relative to this Python module.
PROMPTS_DIR = Path(__file__).parent / "prompts"

def load_template(filename: str) -> str:
    """ Read a prompt template and raise a clear error if it's missing. """
    template_path = PROMPTS_DIR / filename

    if not template_path.is_file():
        raise FileNotFoundError(
            f"Prompt template not found: {template_path}"
        )

    return template_path.read_text(encoding="utf-8")

def load_system_prompt() -> str:
    """ Load the system instructions used by GhostDocs. """
    return load_template("system.txt")

def prepare_analysis_prompt(repository_context: str) -> str:
    """ Insert untrusted repository context into the analysis template. """
    template = load_template("analysis.txt")
    placeholder = "{repository_context}"

    if placeholder not in template:
        raise ValueError(
            "Analysis template is missing the "
            "{repository_context} placeholder."
        )

    return template.replace(placeholder, repository_context)
