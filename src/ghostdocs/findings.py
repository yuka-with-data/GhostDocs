
"""
Organize analyzer results into structured documentation findings.
"""

# Map analyzer finding types to broader knowledge-gap categories.
FINDING_CATEGORIES = {
    "unfinished_business": "unresolved_markers",
    "missing_readme": "documentation_completeness",
    "empty_readme": "documentation_completeness",
}


def build_findings(analysis):
    """Normalize and categorize findings from analyzer results."""
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

    # Return findings in a consistent structure.
    return structured_findings
