#!/usr/bin/env python3
"""
Push Kaggle notebook to Kaggle.

Usage: python3 scripts/push_notebook.py [notebook_name]
  notebook_name: ensemble (default) or submission
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get notebook name from command line or use default
    notebook_name = sys.argv[1] if len(sys.argv) > 1 else "ensemble"

    # Validate notebook exists
    notebook_path = Path(f"notebooks/{notebook_name}")
    if not notebook_path.exists():
        print(f"Error: notebooks/{notebook_name} does not exist")
        print("\nAvailable notebooks:")
        for item in Path("notebooks").iterdir():
            if item.is_dir():
                print(f"  - {item.name}")
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
