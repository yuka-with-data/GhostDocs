"""Test GhostDocs command-line behavior without calling Ollama."""

from pathlib import Path
from unittest.mock import patch
import pytest

from ghostdocs.cli import main

def test_main_prints_report(monkeypatch, capsys):
    """Verify the CLI prints the generated report."""
    monkeypatch.setattr("sys.argv", ["ghostdocs", "."])

    with patch("ghostdocs.cli.generate_report", return_value="# Test Report"):
        main()

    captured = capsys.readouterr()
    assert captured.out == "# Test Report\n"

def test_main_saves_report(tmp_path, monkeypatch, capsys):
    """Verify the CLI saves the report to the requested file."""
    output_file = tmp_path / "report.md"
    monkeypatch.setattr(
        "sys.argv",
        ["ghostdocs", ".", "--output", str(output_file)],
    )

    with patch("ghostdocs.cli.generate_report", return_value="# Test Report"):
        main()

    assert output_file.read_text(encoding="utf-8") == "# Test Report\n"
    assert f"Report saved to: {output_file}" in capsys.readouterr().out

def test_main_passes_custom_model(monkeypatch):
    """Verify the CLI passes a custom model to report generation."""
    monkeypatch.setattr(
        "sys.argv",
        ["ghostdocs", ".", "--model", "test-model"],
    )

    with patch("ghostdocs.cli.generate_report", return_value="# Report") as mock:
        main()

    mock.assert_called_once_with(Path("."), model="test-model")

def test_main_handles_generation_error(monkeypatch, capsys):
    """Verify expected errors are shown without a Python traceback."""
    monkeypatch.setattr("sys.argv", ["ghostdocs", "."])

    with patch(
        "ghostdocs.cli.generate_report",
        side_effect=RuntimeError("Ollama is unavailable."),
    ):
        with pytest.raises(SystemExit) as exc_info:
            main()

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "Ollama is unavailable." in captured.err
    assert "Traceback" not in captured.err
