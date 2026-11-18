"""Scan a project directory and collect documentation files and metadata."""
# pylint: disable=duplicate-code

from pathlib import Path

# Define supported documentation types and directories to skip.
SUPPORTED_EXTENSIONS = {".md", ".mdx", ".rst", ".txt"}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
}


def scan_projects(project_path):
    """Find documentation files and collect repository metadata."""
    root = Path(project_path)

    # Reject paths that do not point to an existing directory.
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {project_path}")

    documents = []
    extension_counts = {}
    directory_counts = {}

    # Walk through project files recursively.
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(root)

        # Skip files inside ignored directories.
        if IGNORED_DIRECTORIES.intersection(relative_path.parts):
            continue

        extension = file_path.suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        # Read documentation, skipping inaccessible or undecodable files.
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        relative_path_str = relative_path.as_posix()

        # Collect document metadata.
        documents.append({
            "path": relative_path_str,
            "content": content,
            "extension": extension,
            "size": len(content.encode("utf-8")),
            "line_count": len(content.splitlines()),
        })

        # Count documentation formats.
        extension_counts[extension] = (
            extension_counts.get(extension, 0) + 1
        )

        # Count documentation files by directory.
        directory = relative_path.parent.as_posix()
        directory = directory if directory != "." else "root"

        directory_counts[directory] = (
            directory_counts.get(directory, 0) + 1
        )

    # Return documents and metadata for reporting.
    return {
        "documents": documents,
        "metadata": {
            "total_documents": len(documents),
            "extension_counts": extension_counts,
            "directory_counts": directory_counts,
        },
    }
