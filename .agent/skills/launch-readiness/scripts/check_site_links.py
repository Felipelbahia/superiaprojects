#!/usr/bin/env python3
"""Check links of a page: empty/'#' hrefs, broken HTTP links, malformed WhatsApp links.

Usage:
    python check_site_links.py https://example.com
    python check_site_links.py path/to/page.html      # offline: only static checks + HTTP for absolute links

Exit code 0 = no FAIL, 1 = at least one FAIL.
Form delivery (does the lead e-mail/webhook arrive?) cannot be verified by a script: test it by hand.
"""

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (launch-readiness link checker)"}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []  # (href, visible text)
        self._href = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href = dict(attrs).get("href", "")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(t for t in self._text if t)))
            self._href = None


def check_whatsapp(href: str) -> str | None:
    parsed = urllib.parse.urlparse(href)
    if parsed.netloc == "wa.me":
        number = parsed.path.strip("/")
    elif parsed.netloc.endswith("whatsapp.com"):
        number = urllib.parse.parse_qs(parsed.query).get("phone", [""])[0]
    else:
        return None
    if not re.fullmatch(r"\d{10,15}", number):
        return f"WhatsApp number '{number}' must be digits only with country code (e.g. 5571999999999), no +, spaces or dashes"
    return None


def http_status(url: str) -> int | str:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=UA, method=method)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return e.code
        except Exception as e:  # noqa: BLE001 - network errors are reported, not raised
            return f"error: {e}"
    return "error"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("target", help="URL or local .html file")
    args = parser.parse_args()

    is_url = args.target.startswith(("http://", "https://"))
    if is_url:
        req = urllib.request.Request(args.target, headers=UA)
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        base = args.target
    else:
        html = Path(args.target).read_text(encoding="utf-8")
        base = ""

    parser_ = LinkParser()
    parser_.feed(html)

    failures, checked = 0, set()
    for href, text in parser_.links:
        label = text or href or "(empty)"
        if href.strip() in ("", "#") or href.lower().startswith("javascript:"):
            print(f"[FAIL] '{label}': empty or placeholder link ({href or 'no href'})")
            failures += 1
            continue
        if href.startswith(("mailto:", "tel:")):
            continue
        wa_error = check_whatsapp(href)
        if wa_error:
            print(f"[FAIL] '{label}': {wa_error}")
            failures += 1
            continue
        if href.startswith("#"):
            if f'id="{href[1:]}"' not in html and f"id='{href[1:]}'" not in html:
                print(f"[FAIL] '{label}': anchor {href} has no matching id")
                failures += 1
            continue
        url = urllib.parse.urljoin(base, href) if base else href
        if not url.startswith(("http://", "https://")) or url in checked:
            continue
        checked.add(url)
        status = http_status(url)
        if isinstance(status, int) and status < 400:
            print(f"[PASS] {url} ({status})")
        elif (isinstance(status, int) and status in (401, 403, 429, 999)) or (
            isinstance(status, str) and "timed out" in status
        ):
            print(f"[WARN] {url} ({status}) blocked or slow for automated requests: open it by hand")
        else:
            print(f"[FAIL] '{label}': {url} -> {status}")
            failures += 1

    print(f"\n{len(parser_.links)} links read, {failures} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
