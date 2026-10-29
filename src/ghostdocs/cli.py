"""Provide the command-line interface for GhostDocs."""

import argparse
from pathlib import Path

from ghostdocs.generator import DEFAULT_MODEL, generate_report

def main() -> None:
    """Parse command-line arguments and generate a repository report."""
    # Define the repository path and optional output/model arguments.
    parser = argparse.ArgumentParser(
        description="Find potentially forgotten knowledge in a repository."
    )
    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to the repository to analyze.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to save the report as a Markdown file.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL}).",
    )
    args = parser.parse_args()

    try:
        # Generate the report and display it in the terminal.
        report = generate_report(args.project_path, model=args.model)
        print(report)

        # Save the same report when an output path is provided.
        if args.output:
            args.output.write_text(report + "\n", encoding="utf-8")
            print(f"\nReport saved to: {args.output}")

    except (ValueError, RuntimeError, OSError) as exc:
        # Show expected errors without printing a traceback.
        parser.error(str(exc))

if __name__ == "__main__":
    main()
