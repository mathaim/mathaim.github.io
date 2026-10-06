#!/usr/bin/env python3
"""Static checks for the site. Exit 0 = pass."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_IDS = ["about", "research", "publications", "service", "experience"]
REQUIRED_LINKS = [
    "mailto:mathaimadelyn@gmail.com",
    "https://github.com/mathaim",
    "https://www.linkedin.com/in/madelynmathai/",
    "assets/Madelyn_Mathai_CV.pdf",
]
BANNED = ["TODO", "TBD", "lorem", "placeholder", "href=\"#\""]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs = set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])


def main():
    errors = []
    index = ROOT / "index.html"
    if not index.exists():
        print("FAIL: index.html missing")
        return 1
    html = index.read_text()
    p = Collector()
    p.feed(html)

    for i in REQUIRED_IDS:
        if i not in p.ids:
            errors.append(f"missing section id #{i}")
    for link in REQUIRED_LINKS:
        if link not in p.refs:
            errors.append(f"missing link {link}")
    for ref in p.refs:
        if ref.startswith("#") and ref[1:] not in p.ids:
            errors.append(f"broken anchor {ref}")
        elif not re.match(r"^(https?:|mailto:|#)", ref):
            if not (ROOT / ref).exists():
                errors.append(f"missing local file {ref}")
    for word in BANNED:
        if word.lower() in html.lower():
            errors.append(f"banned text: {word}")

    for e in errors:
        print("FAIL:", e)
    print("PASS" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
