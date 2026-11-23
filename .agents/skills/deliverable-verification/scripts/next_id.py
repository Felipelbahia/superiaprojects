"""Print the next free id of every registry, per prefix (deliverable-verification).

Usage: python3 -I next_id.py --config verification.json
Never guess an id: run this before adding a row.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_config, load_registries, split_id  # noqa: E402


def next_ids(ids):
    """{prefix: next id} keeping the widest zero padding seen for that prefix."""
    top = {}
    for identifier in ids:
        parts = split_id(identifier)
        if parts:
            prefix, number, width = parts
            best = top.get(prefix, (0, 0))
            top[prefix] = (max(best[0], number), max(best[1], width))
    return {prefix: f"{prefix}{number + 1:0{width}d}" for prefix, (number, width) in sorted(top.items())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    cfg = load_config(parser.parse_args().config)
    for name, ids in load_registries(cfg).items():
        odd = [i for i in ids if not split_id(i)]
        nexts = ", ".join(next_ids(ids).values()) or "(empty registry: pick the first id by hand)"
        note = f"  (ids without a trailing number, ignored: {', '.join(odd)})" if odd else ""
        print(f"{name}: {len(ids)} rows -> next {nexts}{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
