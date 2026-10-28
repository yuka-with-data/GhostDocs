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
