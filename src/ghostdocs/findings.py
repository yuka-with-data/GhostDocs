"""Organize analyzer results into structured documentation findings."""

# Map analyzer finding types to broader knowledge-gap categories.
FINDING_CATEGORIES = {
    "unfinished_business": "unresolved_markers",
    "missing_readme": "documentation_completeness",
    "empty_readme": "documentation_completeness",
}


def build_findings(analysis):
    """Normalize findings and collect documentation intelligence."""
    structured_findings = []

    # Process each raw finding returned by the analyzer.
    for finding in analysis.get("findings", []):
        finding_type = finding["type"]

        structured_findings.append({
            "category": FINDING_CATEGORIES.get(
                finding_type, "uncategorized"
            ),
            "type": finding_type,
            "path": finding["path"],
            "line": finding.get("line"),
            "evidence": finding["message"],
        })

    # Collect documentation inventory for the report.
    inventory = analysis.get("inventory", {})
    metadata = inventory.get("documentation_metadata", {})

    documentation_overview = {
        "document_count": inventory.get("document_count", 0),
        "extension_counts": metadata.get("extension_counts", {}),
        "directory_counts": metadata.get("directory_counts", {}),
        "documentation_files": inventory.get(
            "documentation_files", []
        ),
    }

    # Collect documentation health indicators.
    documentation_health = analysis.get("health", {})

    # Return structured findings and reporting data.
    return {
        "findings": structured_findings,
        "documentation_overview": documentation_overview,
        "documentation_health": documentation_health,
    }
