#!/usr/bin/env python3
"""Check SPF, DKIM and DMARC records of a sending domain.

Usage:
    python check_email_dns.py example.com [--selector google --selector resend]

Exit code 0 = all required records pass, 1 = at least one FAIL.
DKIM selectors are provider-specific, so DKIM is checked only for given --selector values.
"""

import argparse
import re
import subprocess
import sys


def txt_records(name: str) -> list[str]:
    try:
        out = subprocess.run(
            ["dig", "+short", "TXT", name], capture_output=True, text=True, timeout=10
        ).stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    records = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith('"'):
            records.append("".join(re.findall(r'"([^"]*)"', line)))
    return records


def check_spf(domain: str) -> tuple[str, str]:
    spf = [r for r in txt_records(domain) if r.lower().startswith("v=spf1")]
    if not spf:
        return "FAIL", f"No SPF record. Add a TXT on {domain}: v=spf1 include:<provider> ~all"
    if len(spf) > 1:
        return "FAIL", "More than one SPF record (invalid). Merge them into one."
    if not re.search(r"[~\-?]all\b", spf[0]):
        return "WARN", f"SPF has no 'all' mechanism: {spf[0]}"
    if re.search(r"\+all\b", spf[0]):
        return "FAIL", "SPF ends with +all (allows anyone to send)."
    return "PASS", spf[0]


def check_dmarc(domain: str) -> tuple[str, str]:
    dmarc = [r for r in txt_records(f"_dmarc.{domain}") if r.lower().startswith("v=dmarc1")]
    if not dmarc:
        return "FAIL", f"No DMARC record. Add a TXT on _dmarc.{domain}: v=DMARC1; p=none; rua=mailto:dmarc@{domain}"
    policy = re.search(r"\bp=(\w+)", dmarc[0])
    if policy and policy.group(1).lower() == "none":
        return "WARN", f"DMARC in monitor mode (p=none): {dmarc[0]}. Move to quarantine/reject once reports are clean."
    return "PASS", dmarc[0]


def check_dkim(domain: str, selector: str) -> tuple[str, str]:
    name = f"{selector}._domainkey.{domain}"
    records = txt_records(name)
    if any("p=" in r for r in records):
        return "PASS", f"{name} has a public key"
    # providers often use CNAME for DKIM
    try:
        cname = subprocess.run(
            ["dig", "+short", "CNAME", name], capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        cname = ""
    if cname:
        return "PASS", f"{name} -> {cname} (CNAME to provider)"
    return "FAIL", f"No DKIM key at {name}. Copy the record from your email provider's dashboard."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("domain")
    parser.add_argument("--selector", action="append", default=[], help="DKIM selector (repeatable)")
    args = parser.parse_args()
    domain = args.domain.strip().lower()

    results = [("SPF", *check_spf(domain)), ("DMARC", *check_dmarc(domain))]
    if args.selector:
        dkim = [(f"DKIM[{s}]", *check_dkim(domain, s)) for s in args.selector]
        if any(status == "PASS" for _, status, _ in dkim):
            # one valid selector is enough: other selectors are just wrong guesses
            dkim = [(n, "INFO" if st == "FAIL" else st, d) for n, st, d in dkim]
        results += dkim
    else:
        results.append(("DKIM", "SKIP", "Pass --selector <name> (see provider dashboard) to check DKIM"))

    for name, status, detail in results:
        print(f"[{status}] {name}: {detail}")
    return 1 if any(status == "FAIL" for _, status, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main())
