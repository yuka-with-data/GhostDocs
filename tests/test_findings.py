"""Test repository inventory, findings, and analysis helpers."""

from ghostdocs.analyzer import (
    inventory_project,
    find_unfinished_business,
    check_documentation_basics,
    assess_documentation_health,
    analyze_project,
)


def create_scan_results(documents):
    """Build scanner results with documentation metadata for testing."""
    extension_counts = {}
    directory_counts = {}

    for document in documents:
        path = document["path"]
        extension = "." + path.rsplit(".", 1)[-1].lower()

        extension_counts[extension] = extension_counts.get(extension, 0) + 1

        directory = path.rsplit("/", 1)[0] if "/" in path else "root"
        directory_counts[directory] = directory_counts.get(directory, 0) + 1

    return {
        "documents": documents,
        "metadata": {
            "total_documents": len(documents),
            "extension_counts": extension_counts,
            "directory_counts": directory_counts,
        },
    }


def test_inventory_project():
    """Confirm the inventory identifies documentation and key files."""
    documents = [
        {"path": "README.md", "content": "# Example"},
        {"path": "docs/setup.md", "content": "Setup instructions"},
        {"path": "pyproject.toml", "content": "[project]"},
    ]

    scan_results = create_scan_results(documents)
    inventory = inventory_project("example-project", scan_results)

    assert inventory["project_name"] == "example-project"
    assert inventory["document_count"] == 3
    assert "README.md" in inventory["documentation_files"]
    assert "README.md" in inventory["key_project_files"]
    assert "pyproject.toml" in inventory["key_project_files"]
    assert inventory["documentation_metadata"]["total_documents"] == 3


def test_find_unfinished_business():
    """Confirm markers are detected with file paths and line numbers."""
    documents = [
        {
            "path": "README.md",
            "content": "# Project\nTODO: Add setup instructions\nAll done.",
        },
        {
            "path": "docs/notes.md",
            "content": "FIXME: Verify this workflow\nXXX: Explain this decision",
        },
    ]

    findings = find_unfinished_business(documents)

    assert len(findings) == 3
    assert findings[0]["path"] == "README.md"
    assert findings[0]["line"] == 2
    assert findings[0]["marker"] == "TODO"
    assert findings[1]["marker"] == "FIXME"
    assert findings[2]["marker"] == "XXX"


def test_check_documentation_basics():
    """Confirm missing and empty README files are detected."""
    assert check_documentation_basics([])[0]["type"] == "missing_readme"

    documents = [{"path": "README.md", "content": "  \n"}]
    findings = check_documentation_basics(documents)

    assert len(findings) == 1
    assert findings[0]["type"] == "empty_readme"


def test_check_documentation_basics_with_content():
    """Confirm a README with content produces no findings."""
    documents = [{"path": "README.md", "content": "# My Project"}]

    assert not check_documentation_basics(documents)


def test_assess_documentation_health():
    """Confirm documentation health uses inventory and existing findings."""
    documents = [
        {"path": "README.md", "content": "# Project"},
        {"path": "docs/setup.md", "content": "Setup instructions"},
    ]

    scan_results = create_scan_results(documents)
    inventory = inventory_project("example-project", scan_results)
    findings = [
        {"type": "unfinished_business", "path": "README.md"},
        {"type": "empty_readme", "path": "docs/setup.md"},
    ]

    health = assess_documentation_health(inventory, findings)

    assert health["document_count"] == 2
    assert health["issue_count"] == 2
    assert health["has_readme"] is True
    assert health["extension_counts"] == {".md": 2}


def test_analyze_project():
    """Confirm the final analysis includes inventory, findings, and health."""
    documents = [
        {"path": "README.md", "content": "# Project\nTODO: Add setup"},
    ]

    scan_results = create_scan_results(documents)
    result = analyze_project("example-project", scan_results)

    assert result["inventory"]["project_name"] == "example-project"
    assert result["inventory"]["document_count"] == 1
    assert result["health"]["document_count"] == 1
    assert result["health"]["issue_count"] == 1
    assert any(
        finding["type"] == "unfinished_business"
        for finding in result["findings"]
    )
