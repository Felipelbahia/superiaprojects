"""Project-specific checks for the fixture: every check_* function receives ctx and returns (ok, evidence)."""


def check_catalog_events_snake_case(ctx):
    import csv
    import re
    with open(ctx["root"] / "catalogo.csv", newline="", encoding="utf-8") as handle:
        bad = [row["nome"] for row in csv.DictReader(handle, delimiter=";") if not re.fullmatch(r"[a-z]+(_[a-z]+)*", row["nome"])]
    return not bad, "all snake_case" if not bad else f"not snake_case: {', '.join(bad)}"
