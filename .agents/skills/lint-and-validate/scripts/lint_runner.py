#!/usr/bin/env python3
"""
Lint Runner - Unified linting and type checking
Runs appropriate linters based on project type.

Usage:
    python lint_runner.py <project_path> [--since REF] [--all]

Supports:
    - Node.js: npm run lint, npx tsc --noEmit
    - Python: ruff check, mypy

Python projects in a git repo lint only the files touched (rule "Lint what you touch"):
modified or new .py files since HEAD, or since REF with --since. Old findings in files
nobody touched do not fail the run. --all lints the whole project; outside a git repo
everything is linted.
"""

import contextlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Fix Windows console encoding
with contextlib.suppress(AttributeError, ValueError, OSError):
    getattr(sys.stdout, 'reconfigure')(encoding='utf-8', errors='replace')  # noqa: B009


def touched_python_files(project_path: Path, since: str = "HEAD") -> list[str] | None:
    """Python files modified or new since `since` (default HEAD), relative to project_path.

    Returns None when project_path is not inside a git repo (the caller lints everything).
    """
    def git(*args: str) -> str | None:
        try:
            proc = subprocess.run(["git", *args], cwd=str(project_path), capture_output=True, check=False,
                                  text=True, encoding="utf-8", errors="replace", timeout=60)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return proc.stdout if proc.returncode == 0 else None

    if git("rev-parse", "--is-inside-work-tree") is None:
        return None
    changed = git("diff", "--name-only", "--diff-filter=ACMR", "--relative", since)
    new = git("ls-files", "--others", "--exclude-standard")
    if changed is None or new is None:
        return None
    names = {n for n in (changed + new).splitlines() if n.endswith(".py")}
    return sorted(n for n in names if (project_path / n).is_file())


def detect_project_type(project_path: Path, python_files: list[str] | None = None) -> dict:
    """Detect project type and available linters."""
    result: dict[str, Any] = {
        "type": "unknown",
        "linters": []
    }
    
    # Node.js project
    package_json = project_path / "package.json"
    if package_json.exists():
        result["type"] = "node"
        try:
            pkg = json.loads(package_json.read_text(encoding='utf-8'))
            scripts = pkg.get("scripts", {})
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            # Check for lint script
            if "lint" in scripts:
                result["linters"].append({"name": "npm lint", "cmd": ["npm", "run", "lint"]})
            elif "eslint" in deps:
                result["linters"].append({"name": "eslint", "cmd": ["npx", "eslint", "."]})
            
            # Check for TypeScript
            if "typescript" in deps or (project_path / "tsconfig.json").exists():
                result["linters"].append({"name": "tsc", "cmd": ["npx", "tsc", "--noEmit"]})
                
        except (OSError, ValueError, AttributeError) as e:
            result["warning"] = f"package.json not read: {e}"
    
    # Python project
    if (project_path / "pyproject.toml").exists() or (project_path / "requirements.txt").exists():
        result["type"] = "python"
        
        # python_files None = lint everything; a list = only those files (empty = nothing touched)
        targets = ["."] if python_files is None else python_files
        if targets:
            result["linters"].append({"name": "ruff", "cmd": ["ruff", "check", *targets]})
            if (project_path / "mypy.ini").exists() or (project_path / "pyproject.toml").exists():
                result["linters"].append({"name": "mypy", "cmd": ["mypy", *targets]})
        else:
            result["note"] = "no Python files touched: ruff and mypy skipped"
    
    return result


def run_linter(linter: dict, cwd: Path) -> dict:
    """Run a single linter and return results."""
    result = {
        "name": linter["name"],
        "passed": False,
        "output": "",
        "error": ""
    }
    
    try:
        proc = subprocess.run(
            linter["cmd"],
            cwd=str(cwd),
            check=False,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120
        )
        
        result["output"] = proc.stdout[:2000] if proc.stdout else ""
        result["error"] = proc.stderr[:500] if proc.stderr else ""
        result["passed"] = proc.returncode == 0
        
    except FileNotFoundError:
        result["error"] = f"Command not found: {linter['cmd'][0]}"
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout after 120s"
    except OSError as e:
        result["error"] = str(e)
    
    return result


def main():
    args = sys.argv[1:]
    since = "HEAD"
    if "--since" in args:
        i = args.index("--since")
        since = args[i + 1] if i + 1 < len(args) else "HEAD"
        del args[i:i + 2]
    lint_all = "--all" in args
    args = [a for a in args if a != "--all"]
    project_path = Path(args[0] if args else ".").resolve()
    
    print(f"\n{'='*60}")
    print("[LINT RUNNER] Unified Linting")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Detect project type
    python_files = None if lint_all else touched_python_files(project_path, since)
    project_info = detect_project_type(project_path, python_files)
    print(f"Type: {project_info['type']}")
    print(f"Linters: {len(project_info['linters'])}")
    if project_info.get("note"):
        print(project_info["note"])
    print("-"*60)
    
    if not project_info["linters"]:
        print("No linters found for this project type.")
        output = {
            "script": "lint_runner",
            "project": str(project_path),
            "type": project_info["type"],
            "checks": [],
            "passed": True,
            "message": "No linters configured"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    # Run each linter
    results = []
    all_passed = True
    
    for linter in project_info["linters"]:
        print(f"\nRunning: {linter['name']}...")
        result = run_linter(linter, project_path)
        results.append(result)
        
        if result["passed"]:
            print(f"  [PASS] {linter['name']}")
        else:
            print(f"  [FAIL] {linter['name']}")
            if result["error"]:
                print(f"  Error: {result['error'][:200]}")
            all_passed = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for r in results:
        icon = "[PASS]" if r["passed"] else "[FAIL]"
        print(f"{icon} {r['name']}")
    
    output = {
        "script": "lint_runner",
        "project": str(project_path),
        "type": project_info["type"],
        "checks": results,
        "passed": all_passed
    }
    
    print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
