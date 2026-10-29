"""Test GhostDocs report generation without requiring a running Ollama model."""

from unittest.mock import Mock
import pytest

from ghostdocs import generator

def test_generate_report_success(tmp_path, monkeypatch):
    """Verify repository analysis and Ollama report generation work together."""
    # Mock repository scanning and analysis to keep the test self-contained.
    documents = [{"path": "README.md", "content": "Example project"}]
    analysis = {
        "inventory": {
            "project_name": "example",
            "document_count": 1,
            "key_project_files": ["README.md"],
            "documentation_files": ["README.md"],
        },
        "findings": [],
    }

    monkeypatch.setattr(generator, "scan_projects", lambda path: documents)
    monkeypatch.setattr(
        generator, "analyze_project", lambda path, docs: analysis
    )
    monkeypatch.setattr(
        generator, "load_system_prompt", lambda: "System instructions"
    )
    monkeypatch.setattr(
        generator,
        "prepare_analysis_prompt",
        lambda context: f"Analyze this repository:\n{context}",
    )

    # Return a predictable response instead of calling the real model.
    mock_chat = Mock(
        return_value={"message": {"content": "# Example Report\n\nFindings."}}
    )
    monkeypatch.setattr(generator.ollama, "chat", mock_chat)

    result = generator.generate_report(tmp_path)

    assert result == "# Example Report\n\nFindings."
    mock_chat.assert_called_once()

    # Confirm the configured defaults are passed to Ollama.
    call_kwargs = mock_chat.call_args.kwargs
    assert call_kwargs["model"] == generator.DEFAULT_MODEL
    assert call_kwargs["options"]["num_ctx"] == generator.DEFAULT_NUM_CTX
    assert "README.md" in call_kwargs["messages"][1]["content"]


def test_generate_report_invalid_path(tmp_path):
    """Verify a path that is not a directory raises a clear error."""
    invalid_path = tmp_path / "missing-project"

    with pytest.raises(ValueError, match="Project path is not a directory"):
        generator.generate_report(invalid_path)


@pytest.mark.parametrize(
    ("argument", "value", "message"),
    [
        ("context_budget", 0, "Context budget must be greater than zero"),
        ("num_ctx", 0, "num_ctx must be greater than zero"),
    ],
)
def test_generate_report_invalid_limits(
    tmp_path, argument, value, message
):
    """Verify invalid context settings are rejected before model generation."""
    kwargs = {argument: value}

    with pytest.raises(ValueError, match=message):
        generator.generate_report(tmp_path, **kwargs)


def test_generate_report_ollama_error(tmp_path, monkeypatch):
    """Verify Ollama failures produce an actionable error message."""
    monkeypatch.setattr(generator, "scan_projects", lambda path: [])
    monkeypatch.setattr(
        generator,
        "analyze_project",
        lambda path, docs: {
            "inventory": {
                "project_name": "example",
                "document_count": 0,
                "key_project_files": [],
                "documentation_files": [],
            },
            "findings": [],
        },
    )
    monkeypatch.setattr(generator, "load_system_prompt", lambda: "Instructions")
    monkeypatch.setattr(
        generator, "prepare_analysis_prompt", lambda context: context
    )
    monkeypatch.setattr(
        generator.ollama,
        "chat",
        Mock(side_effect=ConnectionError("Ollama is unavailable")),
    )

    with pytest.raises(RuntimeError, match="Check that Ollama is running"):
        generator.generate_report(tmp_path)


def test_generate_report_empty_response(tmp_path, monkeypatch):
    """Verify an empty model response raises a clear error."""
    monkeypatch.setattr(generator, "scan_projects", lambda path: [])
    monkeypatch.setattr(
        generator,
        "analyze_project",
        lambda path, docs: {
            "inventory": {
                "project_name": "example",
                "document_count": 0,
                "key_project_files": [],
                "documentation_files": [],
            },
            "findings": [],
        },
    )
    monkeypatch.setattr(generator, "load_system_prompt", lambda: "Instructions")
    monkeypatch.setattr(
        generator, "prepare_analysis_prompt", lambda context: context
    )
    monkeypatch.setattr(
        generator.ollama,
        "chat",
        Mock(return_value={"message": {"content": "  "}}),
    )

    with pytest.raises(RuntimeError, match="Ollama returned an empty report"):
        generator.generate_report(tmp_path)
