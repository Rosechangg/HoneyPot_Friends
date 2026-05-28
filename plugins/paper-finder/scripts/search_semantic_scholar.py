"""
Semantic Scholar Graph API 검색 (api.semanticscholar.org/graph/v1).

Usage:
    python search_semantic_scholar.py --query "graph attention temporal" \
        --venues "CVPR,ICCV,NeurIPS" --years 2022-2026 --max 50 --out ss.json

키 없이 작동 (rate limit: 100 req / 5min). 환경변수 S2_API_KEY 있으면 사용.
venue 필터는 서버측 publicationVenue.name 매칭 + 클라이언트측 별칭 매칭 둘 다 적용.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.semanticscholar.org/graph/v1/paper/search"

FIELDS = ",".join(
    [
        "paperId",
        "externalIds",
        "title",
        "abstract",
        "year",
        "venue",
        "publicationVenue",
        "publicationTypes",
        "authors.name",
        "citationCount",
        "influentialCitationCount",
        "tldr",
        "openAccessPdf",
        "url",
    ]
)


def fetch(query: str, year_range: str | None, venue_filter: str | None, limit: int, offset: int) -> dict:
    params = {
        "query": query,
        "limit": str(limit),
        "offset": str(offset),
        "fields": FIELDS,
    }
    if year_range:
        params["year"] = year_range
    if venue_filter:
        # Semantic Scholar supports `venue` as comma-separated exact matches against publicationVenue.name.
        # NOTE: long venue lists frequently produce 429s without an API key. Prefer client-side matching
        # (merge_and_rank.py uses an alias dictionary) and pass --strict-venue only when needed.
        params["venue"] = venue_filter

    url = API + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": "paper-finder/0.1 (research)"}
    api_key = os.environ.get("S2_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key

    req = urllib.request.Request(url, headers=headers)
    last_err: Exception | None = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                # 10/20/30/40/50/60s exponential-ish backoff. S2 free tier without key is ~1 req/sec
                # and bursty queries (long venue lists, multi-page) frequently trip the limiter.
                wait = 10 * (attempt + 1)
                print(f"[s2] HTTP {e.code}, sleeping {wait}s (attempt {attempt + 1}/6)", file=sys.stderr)
                time.sleep(wait)
                last_err = e
                continue
            raise
        except Exception as e:
            last_err = e
            time.sleep(3)
    raise RuntimeError(f"semantic scholar fetch failed after retries: {last_err}")


def normalize(p: dict) -> dict:
    ext = p.get("externalIds") or {}
    pub_venue = p.get("publicationVenue") or {}
    tldr = p.get("tldr") or {}
    pdf = p.get("openAccessPdf") or {}
    return {
        "source": "semantic_scholar",
        "s2_id": p.get("paperId", ""),
        "doi": ext.get("DOI", ""),
        "arxiv_id": ext.get("ArXiv", ""),
        "title": p.get("title", "") or "",
        "authors": [a.get("name", "") for a in (p.get("authors") or [])],
        "year": str(p.get("year") or ""),
        "abstract": p.get("abstract") or "",
        "venue_raw": p.get("venue") or pub_venue.get("name", "") or "",
        "venue_type": pub_venue.get("type", ""),
        "publication_types": p.get("publicationTypes") or [],
        "citation_count": p.get("citationCount") or 0,
        "influential_citation_count": p.get("influentialCitationCount") or 0,
        "tldr": tldr.get("text", "") if isinstance(tldr, dict) else "",
        "abs_url": p.get("url", "") or "",
        "pdf_url": pdf.get("url", "") if isinstance(pdf, dict) else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--years", default=None, help="e.g. 2022-2026")
    ap.add_argument("--venues", default=None, help="comma-separated venue names (publicationVenue.name match)")
    ap.add_argument("--max", type=int, default=50)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    print(f"[s2] query={args.query!r} venues={args.venues!r} years={args.years!r} max={args.max}", file=sys.stderr)

    results: list[dict] = []
    page = min(50, args.max)
    offset = 0
    while len(results) < args.max:
        try:
            data = fetch(args.query, args.years, args.venues, page, offset)
        except Exception as e:
            print(f"[s2] fetch error at offset={offset}: {e}", file=sys.stderr)
            break
        batch = data.get("data") or []
        if not batch:
            break
        for p in batch:
            results.append(normalize(p))
        total = data.get("total", 0)
        next_off = data.get("next")
        if next_off is None or len(batch) < page:
            break
        offset = next_off
        time.sleep(1.2)

    results = results[: args.max]
    Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[s2] wrote {len(results)} entries -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
