
"""Tests for structured documentation findings."""

from ghostdocs.findings import build_findings


def test_build_findings_categorizes_unfinished_business():
    """Ensure unfinished markers receive the correct category."""
    analysis = {
        "findings": [{
            "type": "unfinished_business",
            "path": "docs/setup.md",
            "line": 12,
            "message": "TODO: Update setup instructions.",
        }]
    }

    result = build_findings(analysis)

    assert result == [{
        "category": "unresolved_markers",
        "type": "unfinished_business",
        "path": "docs/setup.md",
        "line": 12,
        "evidence": "TODO: Update setup instructions.",
    }]


def test_build_findings_categorizes_missing_readme():
    """Ensure missing README findings are categorized."""
    analysis = {
        "findings": [{
            "type": "missing_readme",
            "path": "README.md",
            "message": "No README file found.",
        }]
    }

    result = build_findings(analysis)

    assert result[0]["category"] == "documentation_completeness"
    assert result[0]["line"] is None


def test_build_findings_categorizes_empty_readme():
    """Ensure empty README findings are categorized."""
    analysis = {
        "findings": [{
            "type": "empty_readme",
            "path": "README.md",
            "message": "README file is empty.",
        }]
    }

    result = build_findings(analysis)

    assert result[0]["category"] == "documentation_completeness"


def test_build_findings_handles_empty_findings():
    """Ensure an empty analysis produces an empty list."""
    assert build_findings({"findings": []}) == []


def test_build_findings_handles_missing_findings_key():
    """Ensure missing findings data produces an empty list."""
    assert build_findings({}) == []
