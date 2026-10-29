""" Scan a project directory and collect documentation files. """

from pathlib import Path

# Define file types to scan and directories to skip.

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
    """ Find supported documentation files and return their paths and contents. """
    root = Path(project_path)

    # Reject paths that do not point to an existing directory
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {project_path}")

    documents = []

    # Walk through project files recursively.
    for file_path in root.rglob("*"):
        # Skip directories and files inside ignored directories
        if not file_path.is_file():
            continue
        if IGNORED_DIRECTORIES.intersection(file_path.relative_to(root).parts):
            continue

        # Keep only supported documentation file types.
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Read each file, skipping files that cannot be accessed or decoded.
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        # Store the relative path and text for later analysis.
        documents.append({
            "path": file_path.relative_to(root).as_posix(),
            "content": content,
        })

    # Return all successfully read documents
    return documents
