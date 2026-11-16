"""Analyze scanned repository content for documentation intelligence."""

from pathlib import Path

# Identify project files that provide useful context.
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


def inventory_project(project_path, scan_results):
    """Return a summary of project documentation and metadata."""
    root = Path(project_path)
    documents = scan_results["documents"]

    inventory = {
        "project_name": root.name,
        "documentation_files": [],
        "key_project_files": [],
        "document_count": len(documents),
        "documentation_metadata": scan_results["metadata"],
    }

    # Record scanned documentation paths and identify key project files.
    for document in documents:
        path = document["path"]
        inventory["documentation_files"].append(path)

        if Path(path).name.lower() in KEY_FILE_NAMES:
            inventory["key_project_files"].append(path)

    return inventory


def find_unfinished_business(documents):
    """Return TODO, FIXME, and XXX markers found in documents."""
    markers = ("TODO", "FIXME", "XXX")
    findings = []

    # Check each line for unfinished-work markers.
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

    return findings


def check_documentation_basics(documents):
    """Report whether the project README is missing or empty."""
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


def assess_documentation_health(inventory, findings):
    """Generate lightweight documentation health indicators."""
    metadata = inventory["documentation_metadata"]

    # Count basic documentation issues.
    issue_types = {
        "missing_readme",
        "empty_readme",
        "unfinished_business",
    }

    issue_count = sum(
        1 for finding in findings
        if finding["type"] in issue_types
    )

    return {
        "document_count": inventory["document_count"],
        "issue_count": issue_count,
        "has_readme": any(
            Path(path).name.lower().startswith("readme.")
            for path in inventory["documentation_files"]
        ),
        "extension_counts": metadata["extension_counts"],
    }


def analyze_project(project_path, scan_results):
    """Collect repository context and combine analysis findings."""
    documents = scan_results["documents"]

    inventory = inventory_project(project_path, scan_results)

    # Run deterministic checks.
    findings = find_unfinished_business(documents)
    findings.extend(check_documentation_basics(documents))

    # Assess documentation health using existing findings.
    health = assess_documentation_health(inventory, findings)

    return {
        "inventory": inventory,
        "findings": findings,
        "health": health,
    }
