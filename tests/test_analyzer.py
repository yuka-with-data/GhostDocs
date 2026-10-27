"""Test repository inventory and analysis helpers."""

from ghostdocs.analyzer import inventory_project

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
