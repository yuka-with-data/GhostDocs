"""Shared test utilities for GhostDocs."""
# pylint: disable=duplicate-code

def create_scan_results(documents):
    """Build scan results with document and directory metadata."""
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
