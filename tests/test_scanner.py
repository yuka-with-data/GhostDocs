"""Test the documentation scanner."""

import pytest
from ghostdocs.scanner import scan_projects

def test_scan_finds_supported_files(tmp_path):
    """Confirm supported files are collected with their contents."""
    (tmp_path / "README.md").write_text("# Project", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Project notes", encoding="utf-8")
    (tmp_path / "script.py").write_text("print('hello')", encoding="utf-8")

    results = scan_projects(tmp_path)
    documents = results["documents"]

    assert len(documents) == 2
    assert {doc["path"] for doc in documents} == {
        "README.md",
        "notes.txt",
    }


def test_scan_collects_document_metadata(tmp_path):
    """Confirm documentation metadata is collected correctly."""
    (tmp_path / "README.md").write_text("# Project\nDescription", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Project notes", encoding="utf-8")

    results = scan_projects(tmp_path)
    metadata = results["metadata"]

    assert metadata["total_documents"] == 2
    assert metadata["extension_counts"] == {
        ".md": 1,
        ".txt": 1,
    }
    assert metadata["directory_counts"] == {
        "root": 2,
    }


def test_scan_skips_ignored_directories(tmp_path):
    """Confirm documentation inside ignored directories is not collected."""
    ignored_dir = tmp_path / ".venv"
    ignored_dir.mkdir()
    (ignored_dir / "notes.md").write_text("Ignore me", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Keep me", encoding="utf-8")

    results = scan_projects(tmp_path)

    assert len(results["documents"]) == 1
    assert results["documents"][0]["path"] == "README.md"


def test_scan_empty_directory(tmp_path):
    """Confirm an empty project returns empty results and metadata."""
    results = scan_projects(tmp_path)

    assert not results["documents"]
    assert results["metadata"]["total_documents"] == 0
    assert not results["metadata"]["extension_counts"]
    assert not results["metadata"]["directory_counts"]


def test_scan_rejects_missing_directory(tmp_path):
    """Confirm an invalid directory raises a clear error."""
    missing_path = tmp_path / "missing"

    with pytest.raises(ValueError):
        scan_projects(missing_path)
