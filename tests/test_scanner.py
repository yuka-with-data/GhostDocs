"""Test the documentation scanner."""

import pytest

from ghostdocs.scanner import scan_projects

def test_scan_finds_supported_files(tmp_path):
    # Confirm supported files are collected with their contents.
    (tmp_path / "README.md").write_text("# Project", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Project notes", encoding="utf-8")
    (tmp_path / "script.py").write_text("print('hello')", encoding="utf-8")

    documents = scan_projects(tmp_path)

    assert len(documents) == 2
    assert {doc["path"] for doc in documents} == {
        "README.md",
        "notes.txt",
    }


def test_scan_skips_ignored_directories(tmp_path):
    # Confirm documentation inside ignored directories is not collected.
    ignored_dir = tmp_path / ".venv"
    ignored_dir.mkdir()
    (ignored_dir / "notes.md").write_text("Ignore me", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Keep me", encoding="utf-8")

    documents = scan_projects(tmp_path)

    assert len(documents) == 1
    assert documents[0]["path"] == "README.md"


def test_scan_empty_directory(tmp_path):
    # Confirm an empty project returns an empty list.
    assert scan_projects(tmp_path) == []


def test_scan_rejects_missing_directory(tmp_path):
    # Confirm an invalid directory raises a clear error.
    missing_path = tmp_path / "missing"

    with pytest.raises(ValueError):
        scan_projects(missing_path)
