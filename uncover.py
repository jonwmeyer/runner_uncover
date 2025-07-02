#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    """Entry point: Validate input, check dependencies, run uncover, and handle results."""
    if len(sys.argv) < 2:
        print("[!] Error: Please provide a query_location for uncover")
        print("Usage: python3 uncover.py example.com")
        sys.exit(1)
    
    query_location = sys.argv[1]

    if not check_uncover_installed():
        print("[!] Error: uncover is not installed or not in PATH")
        print("Please install uncover first: https://uncover.projectdiscovery.io/uncover/get-started/")
        sys.exit(1)
    
    activate_venv()
    
    print(f"[*] Starting uncover query_location uncover for: {query_location}")
    exit_code = run_uncover_and_save(query_location)
    
    if exit_code == 0:
        print("[+] uncover completed successfully")
    else:
        print("[!] uncover completed with errors or warnings")
    
    sys.exit(exit_code)

def check_uncover_installed():
    """Return True if uncover is installed and available in PATH."""
    try:
        result = subprocess.run(
            ["/go/bin/uncover", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def activate_venv():
    """Detect and note if a virtual environment exists."""
    venv_path = Path("venv")
    if venv_path.exists() and venv_path.is_dir():
        print("[*] Virtual environment found")
        venv_python = venv_path / "bin" / "python3"
        if venv_python.exists():
            print("[*] Using virtual environment Python")
        else:
            print("[*] Virtual environment found but Python not detected")

def run_uncover_and_save(query_location):
    """Run uncover and save results to a timestamped file."""
    try:
        output = run_uncover(query_location)
        if output is None:
            print("[!] uncover failed or returned no output")
            return 1
        
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        filename = f"{timestamp}-uncover.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            f.write(output)
        print(f"[*] uncover results saved as {filepath}")
        return 0

    except Exception as e:
        print(f"[!] Error running uncover: {e}", file=sys.stderr)
        return 1 

def run_uncover(query_location):
    """Run uncover on the given query_location and return its output as a string, or None on error."""
    command = [
        "/go/bin/uncover",
        "-q", query_location,
        "-silent"
    ]
    print(f"[*] Executing: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
            check=False
        )
        if result.returncode == -9:
            print("[!] Warning: uncover process was killed by SIGKILL (likely due to memory/resource limits)")
            if result.stdout.strip():
                return result.stdout
            return None
        if result.returncode != 0:
            print(f"[!] uncover exited with code {result.returncode}")
            if result.stderr:
                print("uncover error output:")
                print(result.stderr)
            return result.stdout if result.stdout.strip() else None
        return result.stdout
    except subprocess.TimeoutExpired:
        print("[!] uncover timed out")
        return None
    except FileNotFoundError:
        print("[!] Error: uncover command not found. Please ensure uncover is installed and in PATH")
        return None
    except Exception as e:
        print(f"[!] Unexpected error running uncover: {e}")
        return None

if __name__ == "__main__":
    main() 