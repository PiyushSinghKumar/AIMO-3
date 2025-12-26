#!/usr/bin/env python3
"""
Push Kaggle notebook to Kaggle.

Usage: python3 scripts/push_notebook.py <notebook_name>
  notebook_name: ensemble, submission, gpt-oss, etc.
"""

import subprocess
import sys
import os
from pathlib import Path

def get_available_notebooks():
    """Get list of available notebooks with metadata."""
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        return []

    available = []
    for item in notebooks_dir.iterdir():
        if item.is_dir() and (item / "kernel-metadata.json").exists():
            available.append(item.name)

    return available

def main():
    # Get notebook name from command line (required)
    if len(sys.argv) < 2:
        available = get_available_notebooks()
        print("Error: Notebook name is required")
        print(f"\nUsage: python3 scripts/push_notebook.py <notebook_name>")
        if available:
            print(f"\nAvailable notebooks: {', '.join(available)}")
        sys.exit(1)

    notebook_name = sys.argv[1]

    # Validate notebook exists
    notebook_path = Path(f"notebooks/{notebook_name}")
    if not notebook_path.exists():
        available = get_available_notebooks()
        print(f"Error: notebooks/{notebook_name} does not exist")
        if available:
            print(f"\nAvailable notebooks: {', '.join(available)}")
        sys.exit(1)

    print(f"Pushing {notebook_name} to Kaggle...")
    print("=" * 70)

    # Change to notebook directory
    os.chdir(notebook_path)

    # Run kaggle kernels push via nix-shell
    try:
        result = subprocess.run(
            ["nix-shell", "--run", "kaggle kernels push", "../../shell.nix"],
            check=True,
            text=True
        )
        print("\n" + "=" * 70)
        print(f"✓ Successfully pushed {notebook_name}")
        print("=" * 70)
        return 0
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 70)
        print(f"✗ Failed to push {notebook_name}")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
