""" Analyze scanned repository content for signs of forgotten knowledge. """

from pathlib import Path

# Identify project files that provide useful context
KEY_FILE_NAMES = {
    "readme.md",
    "contributing.md",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "makefile",
    "dockerfile",
}

def inventory_project(project_path, documents):
    root = Path(project_path)
    inventory = {
        "project_name": root.name,
        "documentation_files": [],
        "key_project_files": [],
        "document_count": len(documents),
    }

    # Record the paths of documentation files already scanned.
    for document in documents:
        path = document["path"]
        inventory["documentation_files"].append(path)

        # Identify key files by their filenames
        if Path(path).name.lower() in KEY_FILE_NAMES:
            inventory["key_project_files"].append(path)

    # Return the inventory for later analysis
    return inventory

# Find unfinished-work markers in scanned documentation
def find_unfinished_business(documents):
    pass
