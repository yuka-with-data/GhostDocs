
"""Test GhostDocs prompt template loading and preparation."""

import pytest

from ghostdocs import prompts


def test_load_system_prompt():
    """Verify the system prompt loads as non-empty text."""
    result = prompts.load_system_prompt()

    assert isinstance(result, str)
    assert result.strip()


def test_load_template_missing_file():
    """Verify a missing template raises a clear error."""
    with pytest.raises(FileNotFoundError, match="Prompt template not found"):
        prompts.load_template("missing.txt")


def test_prepare_analysis_prompt():
    """Verify repository context replaces the template placeholder."""
    context = "README.md: Example project documentation"

    result = prompts.prepare_analysis_prompt(context)

    assert context in result
    assert "{repository_context}" not in result
    assert "<repository_data>" in result
    assert "</repository_data>" in result


def test_prepare_analysis_prompt_missing_placeholder(monkeypatch):
    """Verify an invalid analysis template raises a clear error."""

    # Replace template loading with a template that lacks the placeholder.
    monkeypatch.setattr(
        prompts,
        "load_template",
        lambda filename: "Analysis instructions without a placeholder.",
    )

    with pytest.raises(ValueError, match="repository_context"):
        prompts.prepare_analysis_prompt("Example repository context")
