#!/usr/bin/env python3
"""Vet a package name BEFORE installing it (slopsquatting / typosquatting check).

AI coding tools sometimes invent package names. Attackers register those names with malware.
This checks that the package exists and looks like a real, maintained project.

Usage:
    python3 vet_package.py npm express
    python3 vet_package.py pypi requests --min-downloads 5000 --min-age-days 90

Exit code 1 = FAIL (package does not exist). WARN items exit 0 unless --strict is given.
Network: registry.npmjs.org, api.npmjs.org, pypi.org, pypistats.org (stdlib only).
"""

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request

UA = {"User-Agent": "vibecoding-security-audit vet_package"}

POPULAR = {
    "npm": [
        "react", "react-dom", "next", "vue", "angular", "svelte", "express", "lodash", "axios", "typescript",
        "webpack", "vite", "eslint", "prettier", "jest", "mocha", "chalk", "commander", "moment", "dayjs",
        "zod", "prisma", "mongoose", "sequelize", "pg", "mysql2", "redis", "dotenv", "cors", "body-parser",
        "jsonwebtoken", "bcrypt", "bcryptjs", "uuid", "nodemon", "socket.io", "tailwindcss", "postcss",
        "autoprefixer", "rxjs", "openai", "stripe", "firebase", "supabase", "@supabase/supabase-js", "cheerio",
        "puppeteer", "playwright", "sharp", "multer", "helmet", "morgan", "yargs", "inquirer", "glob", "rimraf",
    ],
    "pypi": [
        "requests", "numpy", "pandas", "scipy", "matplotlib", "flask", "django", "fastapi", "uvicorn", "pydantic",
        "sqlalchemy", "psycopg2", "pytest", "boto3", "beautifulsoup4", "scikit-learn", "tensorflow", "torch",
        "openai", "anthropic", "langchain", "httpx", "aiohttp", "pillow", "pyyaml", "cryptography", "redis",
        "celery", "click", "rich", "typer", "black", "ruff", "mypy", "setuptools", "wheel", "urllib3", "jinja2",
        "selenium", "playwright", "stripe", "supabase", "python-dotenv", "gunicorn", "alembic", "pytz",
    ],
}


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def lookalikes(name: str, registry: str, max_distance: int = 2) -> list[str]:
    """Popular names within `max_distance` edits of `name` (never the name itself)."""
    n = name.lower()
    if len(n) < 5:  # short names produce noise
        return []
    return [p for p in POPULAR[registry] if p != n and edit_distance(n, p) <= max_distance]


def get_json(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch_npm(name: str) -> dict | None:
    try:
        doc = get_json(f"https://registry.npmjs.org/{name.replace('/', '%2F')}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    latest = doc.get("dist-tags", {}).get("latest")
    version = doc.get("versions", {}).get(latest, {})
    try:
        downloads = get_json(f"https://api.npmjs.org/downloads/point/last-week/{name}").get("downloads")
    except Exception:  # noqa: BLE001 - downloads are a signal, not required
        downloads = None
    scripts = version.get("scripts", {})
    return {
        "created": doc.get("time", {}).get("created"),
        "weekly_downloads": downloads,
        "has_repo": bool(doc.get("repository") or version.get("repository")),
        "maintainers": len(doc.get("maintainers", [])),
        "install_scripts": sorted(k for k in scripts if k in ("preinstall", "install", "postinstall")),
        "deprecated": bool(version.get("deprecated")),
    }


def fetch_pypi(name: str) -> dict | None:
    try:
        doc = get_json(f"https://pypi.org/pypi/{name}/json")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    uploads = [f["upload_time_iso_8601"] for files in doc.get("releases", {}).values() for f in files]
    info = doc.get("info", {})
    try:
        downloads = get_json(f"https://pypistats.org/api/packages/{name}/recent")["data"]["last_week"]
    except Exception:  # noqa: BLE001
        downloads = None
    return {
        "created": min(uploads) if uploads else None,
        "weekly_downloads": downloads,
        "has_repo": bool(info.get("project_urls") or info.get("home_page")),
        "maintainers": 1 if (info.get("author") or info.get("maintainer")) else 0,
        "install_scripts": [],
        "deprecated": any(f.get("yanked") for files in doc.get("urls", []) for f in [files]),
    }


def assess(name: str, registry: str, meta: dict | None, min_downloads: int, min_age_days: int, now=None) -> list[tuple[str, str]]:
    """Pure function: returns [(status, message)] with status FAIL / WARN / PASS."""
    if meta is None:
        return [("FAIL", f"'{name}' does not exist on {registry}. Likely invented by the AI: do not install it, and do not let anyone register it.")]
    now = now or dt.datetime.now(dt.timezone.utc)
    out = []
    if meta["created"]:
        created = dt.datetime.fromisoformat(meta["created"].replace("Z", "+00:00"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=dt.timezone.utc)
        age = (now - created).days
        out.append(("WARN", f"first published only {age} days ago") if age < min_age_days else ("PASS", f"first published {age} days ago"))
    else:
        out.append(("WARN", "no publish date found"))
    dl = meta["weekly_downloads"]
    if dl is None:
        out.append(("WARN", "weekly downloads unavailable"))
    else:
        out.append(("WARN", f"only {dl} downloads last week") if dl < min_downloads else ("PASS", f"{dl} downloads last week"))
    out.append(("PASS", "has a repository link") if meta["has_repo"] else ("WARN", "no repository link: cannot read the source"))
    if meta["install_scripts"]:
        out.append(("WARN", f"runs code on install: {', '.join(meta['install_scripts'])}. Read it first."))
    if meta["deprecated"]:
        out.append(("WARN", "latest version is deprecated or yanked"))
    similar = lookalikes(name, registry)
    if similar:
        out.append(("WARN", f"name is close to popular package(s): {', '.join(similar)}. Typo?"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("registry", choices=["npm", "pypi"])
    ap.add_argument("name")
    ap.add_argument("--min-downloads", type=int, default=1000, help="weekly downloads below this is a WARN")
    ap.add_argument("--min-age-days", type=int, default=30, help="first publish newer than this is a WARN")
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN too")
    args = ap.parse_args()

    try:
        meta = (fetch_npm if args.registry == "npm" else fetch_pypi)(args.name)
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] could not reach the registry ({e}); vet by hand before installing")
        return 1 if args.strict else 0
    results = assess(args.name, args.registry, meta, args.min_downloads, args.min_age_days)
    for status, msg in results:
        print(f"[{status}] {args.name}: {msg}")
    failed = any(s == "FAIL" for s, _ in results)
    warned = any(s == "WARN" for s, _ in results)
    return 1 if failed or (args.strict and warned) else 0


if __name__ == "__main__":
    sys.exit(main())
