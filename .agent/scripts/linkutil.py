"""linkutil.py - create the AI entrypoint links on macOS, Linux and Windows.

Order tried by `make_link`:
  1. symlink (always on macOS/Linux; on Windows needs Developer Mode or admin, else WinError 1314);
  2. directory junction (Windows only, folders only, no privilege needed);
  3. managed copy: the content is copied and recorded in `.antigravity-kit-copies.json` next to it,
     so a later sync knows the copy is ours, refreshes it when the source changes, and never touches
     a real file or folder it did not create.
The copy keeps the source bytes unchanged (no header), so frontmatter still starts on line 1.
"""

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

MANIFEST = ".antigravity-kit-copies.json"


def resolver_dir(hub: Path, name: str) -> Path:
    """Folder of a SIP resolver inside its hub.

    New layout: `<hub>/prompts/resolver/<name>` (versioned, outside the hub's own skills).
    Legacy layout: `<hub>/.agent/skills/<name>`. The new one wins when it exists; hubs not migrated yet keep working.
    """
    new = Path(hub) / "prompts" / "resolver" / name
    return new if new.is_dir() else Path(hub) / ".agent" / "skills" / name


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_dir():
        for p in sorted(path.rglob("*")):
            if p.is_file():
                h.update(p.relative_to(path).as_posix().encode())
                h.update(p.read_bytes())
    else:
        h.update(path.read_bytes())
    return h.hexdigest()


def load_manifest(target_dir: Path) -> dict:
    try:
        return json.loads((target_dir / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_manifest(target_dir: Path, data: dict) -> None:
    path = target_dir / MANIFEST
    if data:
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    elif path.exists():
        path.unlink()


def is_junction(path: Path) -> bool:
    check = getattr(os.path, "isjunction", None)
    if check:
        return check(path)
    return os.name == "nt" and path.is_dir() and not path.is_symlink() and bool(
        getattr(os.lstat(path), "st_reparse_tag", 0)
    )


def make_junction(link: Path, source: Path) -> bool:
    """Windows directory junction (no privilege needed). False elsewhere or when it fails."""
    if os.name != "nt":
        return False
    result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(source.resolve())], capture_output=True)
    return result.returncode == 0 and link.exists()


def _copy(link: Path, source: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, link)
    else:
        shutil.copyfile(source, link)


def _remove(link: Path) -> None:
    if is_junction(link):
        os.rmdir(link)
    elif link.is_dir() and not link.is_symlink():
        shutil.rmtree(link)
    else:
        link.unlink()


def make_link(link: Path, rel_target: str, source: Path, target_dir: Path | None = None) -> str:
    """Create `link` pointing at `source`. Returns "symlink", "junction" or "copy"."""
    target_dir = target_dir or link.parent
    try:
        link.symlink_to(rel_target, target_is_directory=source.is_dir())
        return "symlink"
    except (OSError, NotImplementedError):
        pass
    if source.is_dir() and make_junction(link, source):
        return "junction"
    _copy(link, source)
    manifest = load_manifest(target_dir)
    manifest[link.name] = _digest(source)
    save_manifest(target_dir, manifest)
    return "copy"


def managed_state(link: Path, source: Path, target_dir: Path | None = None) -> str | None:
    """None: not ours. "ok": junction to source, or a managed copy of the current source. "stale": managed copy behind."""
    target_dir = target_dir or link.parent
    if link.is_symlink() or not link.exists():
        return None
    if is_junction(link):
        return "ok" if link.resolve() == source.resolve() else None
    recorded = load_manifest(target_dir).get(link.name)
    if recorded is None:
        return None
    return "ok" if recorded == _digest(source) else "stale"


def refresh_copy(link: Path, source: Path, target_dir: Path | None = None) -> None:
    target_dir = target_dir or link.parent
    _remove(link)
    _copy(link, source)
    manifest = load_manifest(target_dir)
    manifest[link.name] = _digest(source)
    save_manifest(target_dir, manifest)


def managed_orphans(target_dir: Path, wanted) -> list[str]:
    """Names recorded as our copies that are no longer wanted (the source was removed or renamed)."""
    return [n for n in load_manifest(target_dir) if n not in wanted and (target_dir / n).exists()]


def remove_managed(target_dir: Path, name: str) -> None:
    manifest = load_manifest(target_dir)
    if name not in manifest:
        return
    _remove(target_dir / name)
    del manifest[name]
    save_manifest(target_dir, manifest)
