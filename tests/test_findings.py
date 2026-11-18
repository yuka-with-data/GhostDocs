"""Tests for structured finding generation."""

from ghostdocs.findings import build_findings


def test_build_findings():
    """Confirm findings are categorized and documentation data is collected."""
    analysis = {
        "findings": [
            {
                "type": "unfinished_business",
                "path": "README.md",
                "line": 3,
                "message": "TODO: Add installation instructions",
            },
            {
                "type": "missing_readme",
                "path": "README.md",
                "message": "README is missing",
            },
        ],
        "inventory": {
            "document_count": 2,
            "documentation_metadata": {
                "extension_counts": {".md": 2},
                "directory_counts": {"root": 1, "docs": 1},
            },
            "documentation_files": ["README.md", "docs/setup.md"],
        },
        "health": {"issue_count": 1},
    }

    result = build_findings(analysis)

    assert len(result["findings"]) == 2
    assert result["findings"][0]["category"] == "unresolved_markers"
    assert result["findings"][0]["type"] == "unfinished_business"
    assert result["findings"][0]["line"] == 3
    assert result["findings"][0]["evidence"] == (
        "TODO: Add installation instructions"
    )

    assert result["findings"][1]["category"] == (
        "documentation_completeness"
    )

    assert result["documentation_overview"]["document_count"] == 2
    assert result["documentation_overview"]["extension_counts"] == {
        ".md": 2
    }
    assert result["documentation_overview"]["documentation_files"] == [
        "README.md",
        "docs/setup.md",
    ]

    assert result["documentation_health"]["issue_count"] == 1


def test_build_findings_empty():
    """Confirm empty analysis produces valid default reporting data."""
    result = build_findings({})

    assert not result["findings"]
    assert result["documentation_overview"]["document_count"] == 0
    assert not result["documentation_overview"]["extension_counts"]
    assert not result["documentation_overview"]["documentation_files"]
    assert not result["documentation_health"]
