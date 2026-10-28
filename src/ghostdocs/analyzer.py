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
    """Return TODO, FIXME, and XXX markers found in documents."""
    markers = ("TODO", "FIXME", "XXX")
    findings = []

    # Check each line of each document for unfinished-work markers.
    for document in documents:
        for line_number, line in enumerate(
            document["content"].splitlines(), start=1
        ):
            for marker in markers:
                if marker in line.upper():
                    findings.append({
                        "type": "unfinished_business",
                        "path": document["path"],
                        "line": line_number,
                        "marker": marker,
                        "message": line.strip(),
                    })
                    break

    # Return all findings for the Ghost Report.
    return findings

def check_documentation_basics(documents):
    """ Report whether the project README is missing or empty. """
    readmes = [
        document
        for document in documents
        if Path(document["path"]).name.lower() in {
            "readme.md", "readme.mdx", "readme.rst", "readme.txt"
        }
    ]

    # Report a missing README if none was found.
    if not readmes:
        return [{
            "type": "missing_readme",
            "path": "README.md",
            "message": "No README file found.",
        }]

    # Report README files that contain no meaningful content.
    findings = []
    for readme in readmes:
        if not readme["content"].strip():
            findings.append({
                "type": "empty_readme",
                "path": readme["path"],
                "message": "README file is empty.",
            })

    return findings

# Combine the inventory and deterministic findings for later AI analysis.
def analyze_project(project_path, documents):
    """ Colelct repo context and combine analysis findings. """
    inventory = inventory_project(project_path, documents)

    # Run the basic checks and combine their findings.
    findings = find_unfinished_business(documents)
    findings.extend(check_documentation_basics(documents))

    # Return a consistent result for the report generator.
    return {
        "inventory": inventory,
        "findings": findings,
    }
