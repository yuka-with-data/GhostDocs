"""Test repository inventory and analysis helpers."""

from ghostdocs.analyzer import inventory_project, find_unfinished_business

def test_inventory_project():
    # Confirm the inventory identifies documentation and key files.
    documents = [
        {"path": "README.md", "content": "# Example"},
        {"path": "docs/setup.md", "content": "Setup instructions"},
        {"path": "pyproject.toml", "content": "[project]"},
    ]

    inventory = inventory_project("example-project", documents)

    assert inventory["project_name"] == "example-project"
    assert inventory["document_count"] == 3
    assert "README.md" in inventory["documentation_files"]
    assert "README.md" in inventory["key_project_files"]
    assert "pyproject.toml" in inventory["key_project_files"]

def test_find_unfinished_business():
    # Confirm markers are detected with their file paths and line numbers.
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

# Test README checks and the combined analysis result.
def test_check_documentation_basics():
    # Confirm missing and empty README files are detected.
    from ghostdocs.analyzer import check_documentation_basics

    assert check_documentation_basics([])[0]["type"] == "missing_readme"

    documents = [{"path": "README.md", "content": "  \n"}]
    findings = check_documentation_basics(documents)

    assert len(findings) == 1
    assert findings[0]["type"] == "empty_readme"


def test_check_documentation_basics_with_content():
    # Confirm a README with content produces no findings.
    from ghostdocs.analyzer import check_documentation_basics

    documents = [{"path": "README.md", "content": "# My Project"}]

    assert check_documentation_basics(documents) == []


def test_analyze_project():
    # Confirm the final analysis combines inventory and findings.
    from ghostdocs.analyzer import analyze_project

    documents = [
        {"path": "README.md", "content": "# Project\nTODO: Add setup"},
    ]

    result = analyze_project("example-project", documents)

    assert result["inventory"]["project_name"] == "example-project"
    assert result["inventory"]["document_count"] == 1
    assert any(
        finding["type"] == "unfinished_business"
        for finding in result["findings"]
    )
