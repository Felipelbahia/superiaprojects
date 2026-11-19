#!/usr/bin/env python3
"""
Master Checklist Runner - Antigravity Kit
==========================================

Orchestrates all validation scripts in priority order.
Use this for incremental validation during development.

Usage:
    python scripts/checklist.py .                    # Run core checks
    python scripts/checklist.py . --url <URL>        # Include performance checks

Priority Order:
    P0: Security Scan (vulnerabilities, secrets)
    P1: Lint & Type Check (code quality)
    P1: Env Diff Check (no config, .env, migration or database target in the diff; ALLOW_ENV_DIFF=1 releases)
    P1: Scope Check (the diff stays inside the plan's `Scope:` line; ALLOW_SCOPE_DIFF=1 releases)
    P2: Schema Validation (if database exists)
    P3: Test Runner (unit/integration tests; a Node project with an npm script `test:fast` runs only that quick subset, flagged in the output; run the full suite before closing a change)
    P4: UX Audit (psychology laws, accessibility)
    P5: SEO Check (meta tags, structure)
    P6: Performance (lighthouse - requires URL)

Not applicable (per project):
    A project may declare in `.agent/checklist.json` that a non-critical check does not
    apply to it, always with a reason. The check is skipped and shown as such:
        {"not_applicable": {"UX Audit": "no web app; email HTML is validated by scripts/validate_html_templates.py"}}
    Critical checks (Security Scan, Lint Check) cannot be declared. An empty reason,
    an unknown check name or invalid JSON stops the checklist with exit 1.
"""

import json
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

# Define priority-ordered checks
CORE_CHECKS = [
    ("Security Scan", ".agent/skills/vulnerability-scanner/scripts/security_scan.py", True),
    ("Lint Check", ".agent/skills/lint-and-validate/scripts/lint_runner.py", True),
    ("Env Diff Check", ".agent/scripts/env_diff_check.py", True),
    ("Scope Check", ".agent/scripts/scope_check.py", False),
    ("Schema Validation", ".agent/skills/database-design/scripts/schema_validator.py", False),
    ("Test Runner", ".agent/skills/testing-patterns/scripts/test_runner.py", False),
    ("UX Audit", ".agent/skills/frontend-design/scripts/ux_audit.py", False),
]

PERFORMANCE_CHECKS = [
    ("Lighthouse Audit", ".agent/skills/performance-profiling/scripts/lighthouse_audit.py", True),
    ("Playwright E2E", ".agent/skills/webapp-testing/scripts/playwright_runner.py", False),
]

PROJECT_CONFIG = ".agent/checklist.json"


def load_not_applicable(project_path: Path) -> dict:
    """Return {check name: reason} declared by the project; exit 1 if the declaration is invalid."""
    config_path = project_path / PROJECT_CONFIG
    if not config_path.is_file():
        return {}
    try:
        declared = json.loads(config_path.read_text(encoding="utf-8")).get("not_applicable", {})
    except (json.JSONDecodeError, AttributeError) as e:
        print_error(f"{PROJECT_CONFIG}: invalid ({e})")
        sys.exit(1)
    checks = {name: required for name, _, required in CORE_CHECKS + PERFORMANCE_CHECKS}
    errors = []
    for name, reason in declared.items():
        if name not in checks:
            errors.append(f"unknown check '{name}' (valid: {', '.join(checks)})")
        elif checks[name]:
            errors.append(f"'{name}' is critical and cannot be declared not applicable")
        elif not isinstance(reason, str) or not reason.strip():
            errors.append(f"'{name}' needs a reason")
    for error in errors:
        print_error(f"{PROJECT_CONFIG}: {error}")
    if errors:
        sys.exit(1)
    return {name: reason.strip() for name, reason in declared.items()}


def not_applicable_result(name: str, reason: str) -> dict:
    print_warning(f"{name}: not applicable ({reason})")
    return {"name": name, "passed": True, "output": "", "skipped": True, "reason": reason}


def check_script_exists(script_path: Path) -> bool:
    """Check if script file exists"""
    return script_path.exists() and script_path.is_file()

def run_script(name: str, script_path: Path, project_path: str, url: Optional[str] = None) -> dict:
    """
    Run a validation script and capture results
    
    Returns:
        dict with keys: name, passed, output, skipped
    """
    if not check_script_exists(script_path):
        print_warning(f"{name}: Script not found, skipping")
        return {"name": name, "passed": True, "output": "", "skipped": True}
    
    print_step(f"Running: {name}")
    
    # Build command
    cmd = [sys.executable, str(script_path), project_path]
    if url and ("lighthouse" in script_path.name.lower() or "playwright" in script_path.name.lower()):
        cmd.append(url)
    
    # Run script
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        passed = result.returncode == 0
        
        if passed:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
        
        return {
            "name": name,
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr,
            "skipped": False
        }
    
    except subprocess.TimeoutExpired:
        print_error(f"{name}: TIMEOUT (>5 minutes)")
        return {"name": name, "passed": False, "output": "", "error": "Timeout", "skipped": False}
    
    except Exception as e:
        print_error(f"{name}: ERROR - {str(e)}")
        return {"name": name, "passed": False, "output": "", "error": str(e), "skipped": False}

LAUNCH_SKILL_DIR = ".agent/skills/launch-readiness/scripts"

def run_launch_check(name: str, script_path: Path, script_args: List[str]) -> dict:
    """Run an opt-in launch-readiness script (own CLI, not the project-path convention)."""
    if not check_script_exists(script_path):
        print_warning(f"{name}: Script not found, skipping")
        return {"name": name, "passed": True, "output": "", "skipped": True}

    print_step(f"Running: {name}")
    result = subprocess.run(
        [sys.executable, "-I", str(script_path), *script_args],
        capture_output=True, text=True, timeout=120
    )
    print(result.stdout)
    passed = result.returncode == 0
    (print_success if passed else print_error)(f"{name}: {'PASSED' if passed else 'FAILED'}")
    return {"name": name, "passed": passed, "output": result.stdout, "skipped": False}

def print_summary(results: List[dict]):
    """Print final summary report"""
    print_header("📊 CHECKLIST SUMMARY")
    
    passed_count = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed_count = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped_count = sum(1 for r in results if r.get("skipped"))
    
    print(f"Total Checks: {len(results)}")
    print(f"{Colors.GREEN}✅ Passed: {passed_count}{Colors.ENDC}")
    print(f"{Colors.RED}❌ Failed: {failed_count}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏭️  Skipped: {skipped_count}{Colors.ENDC}")
    print()
    
    # Detailed results
    for r in results:
        if r.get("skipped"):
            status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}✅{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌{Colors.ENDC}"
        
        reason = f": not applicable ({r['reason']})" if r.get("reason") else ""
        print(f"{status} {r['name']}{reason}")
    
    print()
    
    if failed_count > 0:
        print_error(f"{failed_count} check(s) FAILED - Please fix before proceeding")
        return False
    else:
        print_success("All checks PASSED ✨")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Run Antigravity Kit validation checklist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/checklist.py .                      # Core checks only
  python scripts/checklist.py . --url http://localhost:3000  # Include performance
        """
    )
    parser.add_argument("project", help="Project path to validate")
    parser.add_argument("--url", help="URL for performance checks (lighthouse, playwright)")
    parser.add_argument("--skip-performance", action="store_true", help="Skip performance checks even if URL provided")
    parser.add_argument("--email-domain", help="Sending domain: also check SPF/DKIM/DMARC (launch-readiness)")
    parser.add_argument("--dkim-selector", action="append", default=[], help="DKIM selector for --email-domain (repeatable)")
    parser.add_argument("--check-links", action="store_true", help="Also check links of --url (launch-readiness)")

    args = parser.parse_args()
    
    project_path = Path(args.project).resolve()
    
    if not project_path.exists():
        print_error(f"Project path does not exist: {project_path}")
        sys.exit(1)
    
    print_header("🚀 ANTIGRAVITY KIT - MASTER CHECKLIST")
    print(f"Project: {project_path}")
    print(f"URL: {args.url if args.url else 'Not provided (performance checks skipped)'}")
    
    results = []
    not_applicable = load_not_applicable(project_path)

    shared_repo_path = Path(__file__).resolve().parent.parent.parent

    # Run core checks
    print_header("📋 CORE CHECKS")
    for name, script_path, required in CORE_CHECKS:
        if name in not_applicable:
            results.append(not_applicable_result(name, not_applicable[name]))
            continue
        script = project_path / script_path
        if not check_script_exists(script):
            script = shared_repo_path / script_path

        result = run_script(name, script, str(project_path))
        results.append(result)
        
        # If required check fails, stop
        if required and not result["passed"] and not result.get("skipped"):
            print_error(f"CRITICAL: {name} failed. Stopping checklist.")
            print_summary(results)
            sys.exit(1)
    
    # Run performance checks if URL provided
    if args.url and not args.skip_performance:
        print_header("⚡ PERFORMANCE CHECKS")
        for name, script_path, required in PERFORMANCE_CHECKS:
            if name in not_applicable:
                results.append(not_applicable_result(name, not_applicable[name]))
                continue
            script = project_path / script_path
            if not check_script_exists(script):
                script = shared_repo_path / script_path
            result = run_script(name, script, str(project_path), args.url)
            results.append(result)
    
    # Opt-in launch-readiness checks (only when their flags are given)
    if args.email_domain or (args.check_links and args.url):
        print_header("🚀 LAUNCH READINESS")
        launch_dir = project_path / LAUNCH_SKILL_DIR
        if not launch_dir.exists():
            launch_dir = shared_repo_path / LAUNCH_SKILL_DIR
        if args.email_domain:
            selectors = [a for s in args.dkim_selector for a in ("--selector", s)]
            results.append(run_launch_check("Email DNS (SPF/DKIM/DMARC)", launch_dir / "check_email_dns.py", [args.email_domain, *selectors]))
        if args.check_links and args.url:
            results.append(run_launch_check("Site Links", launch_dir / "check_site_links.py", [args.url]))

    # Print summary
    all_passed = print_summary(results)
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
