"""
arXiv API 검색.

Usage:
    python search_arxiv.py --query "graph attention temporal" --years 2022-2026 --max 50 --out arxiv.json

arXiv API는 무료/키 불필요. rate limit는 ~1 req/3s (export.arxiv.org 권장).
Categories filter는 옵션. 학회 venue는 arXiv에는 안 들어있으므로 후처리(Semantic Scholar 머지)에서 보강.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def build_query(keyword: str, years: tuple[int, int] | None, categories: list[str] | None) -> str:
    parts = [f"all:{keyword}"]
    if categories:
        cats = " OR ".join(f"cat:{c}" for c in categories)
        parts.append(f"({cats})")
    if years:
        lo, hi = years
        parts.append(f"submittedDate:[{lo}01010000 TO {hi}12312359]")
    return " AND ".join(parts)


def fetch_arxiv(query: str, start: int, max_results: int) -> str:
    params = {
        "search_query": query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    # Use https to avoid redirect loops some clients hit on http://export.arxiv.org
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "paper-finder/0.1 (research)"})

    # Small jitter before the first attempt to avoid synchronized retries when called twice in quick
    # succession from the same machine (which is exactly what /find-papers does).
    time.sleep(random.uniform(0.5, 2.5))

    last_err: Exception | None = None
    waits = [15, 30, 45, 60, 90, 120, 150, 180]  # ~12 minutes total worst case
    for attempt, wait in enumerate(waits):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                # add jitter so concurrent jobs don't lock-step
                jw = wait + random.uniform(0, 5)
                print(f"[arxiv] HTTP {e.code}, sleeping {jw:.1f}s (attempt {attempt + 1}/{len(waits)})", file=sys.stderr)
                time.sleep(jw)
                last_err = e
                continue
            raise
        except Exception as e:
            last_err = e
            time.sleep(5)
    raise RuntimeError(f"arxiv fetch failed after retries: {last_err}")


def parse_entries(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    out = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        arxiv_id = (entry.findtext("atom:id", default="", namespaces=ARXIV_NS) or "").strip()
        # http://arxiv.org/abs/2401.12345v1 -> 2401.12345
        short_id = arxiv_id.rsplit("/", 1)[-1].split("v")[0] if arxiv_id else ""

        title = (entry.findtext("atom:title", default="", namespaces=ARXIV_NS) or "").strip().replace("\n", " ")
        summary = (entry.findtext("atom:summary", default="", namespaces=ARXIV_NS) or "").strip().replace("\n", " ")
        published = (entry.findtext("atom:published", default="", namespaces=ARXIV_NS) or "").strip()
        year = published[:4] if published else ""

        authors = [
            (a.findtext("atom:name", default="", namespaces=ARXIV_NS) or "").strip()
            for a in entry.findall("atom:author", ARXIV_NS)
        ]

        pdf_link = ""
        abs_link = ""
        for link in entry.findall("atom:link", ARXIV_NS):
            rel = link.get("rel")
            href = link.get("href", "")
            title_attr = link.get("title", "")
            if title_attr == "pdf":
                pdf_link = href
            elif rel == "alternate":
                abs_link = href

        journal_ref = (entry.findtext("arxiv:journal_ref", default="", namespaces=ARXIV_NS) or "").strip()
        comment = (entry.findtext("arxiv:comment", default="", namespaces=ARXIV_NS) or "").strip()
        primary_cat_el = entry.find("arxiv:primary_category", ARXIV_NS)
        primary_cat = primary_cat_el.get("term", "") if primary_cat_el is not None else ""

        out.append(
            {
                "source": "arxiv",
                "arxiv_id": short_id,
                "title": title,
                "authors": authors,
                "year": year,
                "abstract": summary,
                "venue_raw": journal_ref,  # rarely populated; merge step backfills via Semantic Scholar
                "comment": comment,        # often contains "Accepted at CVPR 2024" etc.
                "primary_category": primary_cat,
                "abs_url": abs_link,
                "pdf_url": pdf_link,
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True, help="Search keyword/phrase")
    ap.add_argument("--years", default=None, help="e.g. 2022-2026")
    ap.add_argument("--categories", default=None, help="comma-separated arXiv categories e.g. cs.CV,cs.LG")
    ap.add_argument("--max", type=int, default=50)
    ap.add_argument("--out", required=True, help="output JSON path")
    args = ap.parse_args()

    years = None
    if args.years:
        lo, hi = args.years.split("-")
        years = (int(lo), int(hi))

    cats = [c.strip() for c in args.categories.split(",")] if args.categories else None
    query = build_query(args.query, years, cats)
    print(f"[arxiv] query={query!r} max={args.max}", file=sys.stderr)

    entries: list[dict] = []
    page_size = min(50, args.max)
    start = 0
    while len(entries) < args.max:
        try:
            xml_text = fetch_arxiv(query, start, page_size)
        except Exception as e:
            print(f"[arxiv] fetch error at start={start}: {e}", file=sys.stderr)
            break
        batch = parse_entries(xml_text)
        if not batch:
            break
        entries.extend(batch)
        if len(batch) < page_size:
            break
        start += page_size
        time.sleep(3.1)  # respect arXiv rate limit

    entries = entries[: args.max]
    Path(args.out).write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[arxiv] wrote {len(entries)} entries -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
