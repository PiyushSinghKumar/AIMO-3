#!/usr/bin/env python3
"""
Fetch Kaggle notebook execution logs and status.

Usage: python3 scripts/get_notebook_logs.py [notebook_name]
  notebook_name: ensemble (default), submission, gpt-oss, etc.
"""

import subprocess
import json
import os
import sys
from pathlib import Path

def load_metadata(notebook_name):
    """Load kernel metadata from JSON file."""
    metadata_path = Path(f"notebooks/{notebook_name}/kernel-metadata.json")

    if not metadata_path.exists():
        return None

    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            return metadata.get('id')
    except Exception as e:
        print(f"Error reading metadata: {e}")
        return None

def get_available_notebooks():
    """Get list of available notebooks from notebooks directory."""
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        return []

    available = []
    for item in notebooks_dir.iterdir():
        if item.is_dir() and (item / "kernel-metadata.json").exists():
            available.append(item.name)

    return available

# Get notebook name from command line (required)
if len(sys.argv) < 2:
    available = get_available_notebooks()
    print("Error: Notebook name is required")
    print(f"\nUsage: python3 scripts/get_notebook_logs.py <notebook_name>")
    if available:
        print(f"\nAvailable notebooks: {', '.join(available)}")
    sys.exit(1)

notebook_name = sys.argv[1]

# Load kernel slug from metadata
KERNEL_SLUG = load_metadata(notebook_name)

if not KERNEL_SLUG:
    available = get_available_notebooks()
    print(f"Error: Could not find metadata for notebook '{notebook_name}'")
    if available:
        print(f"Available notebooks: {', '.join(available)}")
    sys.exit(1)

LOGS_DIR = f"./logs/{notebook_name}"

def run_command(cmd):
    """Run a command and return output."""
    try:
        # Use nix-shell to run kaggle commands
        nix_cmd = ["nix-shell", "--run", " ".join(cmd)]
        result = subprocess.run(
            nix_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def get_kernel_status():
    """Get the current status of the kernel."""
    print(f"Checking status for: {KERNEL_SLUG}")
    print("=" * 70)

    stdout, stderr, code = run_command([
        "kaggle", "kernels", "status", KERNEL_SLUG
    ])

    if stdout:
        print(stdout)
    if stderr:
        print("Errors:", stderr)

    return code == 0

def get_kernel_output():
    """Download kernel output/logs."""
    print("\n" + "=" * 70)
    print("Fetching kernel output...")
    print("=" * 70 + "\n")

    # Remove old logs
    if os.path.exists(LOGS_DIR):
        import shutil
        shutil.rmtree(LOGS_DIR)

    os.makedirs(LOGS_DIR, exist_ok=True)

    stdout, stderr, code = run_command([
        "kaggle", "kernels", "output",
        KERNEL_SLUG,
        "--path", LOGS_DIR
    ])

    if stdout:
        print(stdout)
    if stderr and "403" not in stderr:  # Ignore 403 errors (common for private kernels)
        print("Errors:", stderr)

    return code == 0

def display_logs():
    """Display downloaded log files."""
    if not os.path.exists(LOGS_DIR):
        print("\nNo logs directory found - kernel may not have executed yet")
        return

    log_files = list(Path(LOGS_DIR).glob("*"))

    if not log_files:
        print("\nNo log files found in logs directory")
        return

    print("\n" + "=" * 70)
    print(f"Found {len(log_files)} file(s) in {LOGS_DIR}:")
    print("=" * 70)

    for f in log_files:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

    # Display text files
    for log_file in log_files:
        if log_file.suffix in ['.log', '.txt', '.out', '']:
            try:
                print("\n" + "=" * 70)
                print(f"Content of: {log_file.name}")
                print("=" * 70)
                with open(log_file, 'r') as f:
                    content = f.read()
                    if content:
                        print(content)
                    else:
                        print("(empty file)")
            except Exception as e:
                print(f"Could not read {log_file.name}: {e}")

def main():
    print("Kaggle Notebook Log Fetcher")
    print("=" * 70 + "\n")

    # Get status
    status_ok = get_kernel_status()

    # Try to get output
    output_ok = get_kernel_output()

    # Display logs
    display_logs()

    print("\n" + "=" * 70)
    print("To view logs on Kaggle website:")
    print(f"https://www.kaggle.com/code/{KERNEL_SLUG}")
    print("=" * 70)

    if not status_ok and not output_ok:
        print("\n⚠ Warning: Could not fetch logs via API")
        print("You may need to:")
        print("  1. Check if the kernel has been executed")
        print("  2. Verify the kernel slug is correct")
        print("  3. Check your Kaggle API credentials")

if __name__ == "__main__":
    main()
