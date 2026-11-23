"""Shared helpers: config loading, file globs and registries (deliverable-verification)."""

import csv
import fnmatch
import glob
import json
import posixpath
import re
from pathlib import Path

ID_SPLIT = re.compile(r"^(.*?)(\d+)$")


def load_config(path):
    """Read the JSON config; paths inside it are relative to `root` (default: the config's folder)."""
    path = Path(path).resolve()
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["_root"] = (path.parent / cfg.get("root", ".")).resolve()
    cfg["_config_dir"] = path.parent
    return cfg


def read(root, rel):
    return (Path(root) / rel).read_text(encoding="utf-8")


def files(root, patterns, exclude=()):
    """Expand glob patterns under root; `exclude` globs match the posix path relative to root."""
    root = Path(root)
    found = []
    for pattern in patterns:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in found and not any(fnmatch.fnmatch(rel, ex) for ex in exclude):
                found.append(rel)
    return found


def generated_output(cfg):
    doc = cfg.get("document")
    return [glob.escape(posixpath.normpath(doc["output"]))] if doc else []


def registry_rows(root, spec):
    """Return the list of ids, one per row (duplicates kept: rows are counted, not unique ids)."""
    if "csv" in spec:
        opts = spec["csv"]
        with open(Path(root) / spec["file"], newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, delimiter=opts.get("delimiter", ","))
            return [row[opts["id_column"]].strip() for row in reader]
    return re.findall(spec["row_regex"], read(root, spec["file"]), re.M)


def csv_shape_errors(root, spec):
    """Rows of a CSV registry whose column count differs from the header (they silently shift a table)."""
    if "csv" not in spec:
        return []
    with open(Path(root) / spec["file"], newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle, delimiter=spec["csv"].get("delimiter", ",")))
    width = len(rows[0]) if rows else 0
    return [f"line {n}: {len(row)} columns (header: {width})" for n, row in enumerate(rows[1:], 2) if row and len(row) != width]


def load_registries(cfg):
    return {name: registry_rows(cfg["_root"], spec) for name, spec in cfg.get("registries", {}).items()}


def split_id(identifier):
    """'A-007' -> ('A-', 7, 3); ids without trailing digits -> None."""
    match = ID_SPLIT.match(identifier)
    if not match:
        return None
    prefix, digits = match.groups()
    return prefix, int(digits), len(digits)
