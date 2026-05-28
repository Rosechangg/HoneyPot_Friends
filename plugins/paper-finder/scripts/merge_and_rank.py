"""
arXiv + Semantic Scholar 결과를 dedup하고 venue 매칭/랭킹.

Usage:
    python merge_and_rank.py --arxiv arxiv.json --s2 ss.json \
        --required-venues "CVPR,SIGGRAPH" \
        --preferred-venues "NeurIPS,ICML,ICLR,ICCV,ECCV" \
        --keyword "graph attention temporal" \
        --top 30 --out ranked.json

매칭 키 우선순위: DOI > arxiv_id > title(소문자, 공백 정규화).
랭킹: required venue 매치 +100, preferred venue 매치 +50, citation log boost, abstract 키워드 일치.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


def norm_title(t: str) -> str:
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def venue_aliases(name: str) -> set[str]:
    """학회/저널 별칭 사전. 정규화된 소문자 토큰 집합 반환."""
    name = (name or "").lower()
    tokens = {name}
    # 주요 conference 약자 ↔ 풀네임 매핑
    mapping = {
        "cvpr": ["ieee/cvf conference on computer vision and pattern recognition", "computer vision and pattern recognition"],
        "iccv": ["ieee/cvf international conference on computer vision", "international conference on computer vision"],
        "eccv": ["european conference on computer vision"],
        "neurips": ["neural information processing systems", "nips", "advances in neural information processing systems"],
        "icml": ["international conference on machine learning"],
        "iclr": ["international conference on learning representations"],
        "aaai": ["aaai conference on artificial intelligence"],
        "siggraph": ["acm siggraph", "acm transactions on graphics"],
        "siggraph asia": ["siggraph asia"],
        "tog": ["acm transactions on graphics"],
        "chi": ["chi conference on human factors in computing systems", "human factors in computing systems"],
        "iui": ["intelligent user interfaces", "acm conference on intelligent user interfaces"],
        "uist": ["user interface software and technology"],
        "cscw": ["computer-supported cooperative work"],
        "t-pami": ["transactions on pattern analysis and machine intelligence", "tpami", "pami"],
        "ijcv": ["international journal of computer vision"],
        "eswa": ["expert systems with applications"],
        "kbs": ["knowledge-based systems"],
        "ins": ["information sciences"],
    }
    for short, longs in mapping.items():
        if short in tokens or any(long_name in name for long_name in longs):
            tokens.add(short)
            tokens.update(longs)
    return tokens


def venue_match(paper_venue: str, target_venue: str, comment: str = "") -> bool:
    """paper의 venue/comment가 target venue와 매칭되는지."""
    if not target_venue:
        return False
    target_aliases = venue_aliases(target_venue)
    haystack = (paper_venue + " " + comment).lower()
    for alias in target_aliases:
        if alias and alias in haystack:
            return True
    return False


def merge(arxiv_items: list[dict], s2_items: list[dict]) -> list[dict]:
    by_doi: dict[str, dict] = {}
    by_arxiv: dict[str, dict] = {}
    by_title: dict[str, dict] = {}

    def key_or_add(item: dict) -> dict:
        doi = (item.get("doi") or "").lower().strip()
        ax = (item.get("arxiv_id") or "").strip()
        tk = norm_title(item.get("title", ""))
        if doi and doi in by_doi:
            return by_doi[doi]
        if ax and ax in by_arxiv:
            return by_arxiv[ax]
        if tk and tk in by_title:
            return by_title[tk]
        if doi:
            by_doi[doi] = item
        if ax:
            by_arxiv[ax] = item
        if tk:
            by_title[tk] = item
        return item

    merged: list[dict] = []
    # Semantic Scholar 우선 (venue 정보 신뢰도 높음)
    for it in s2_items:
        existing = key_or_add(it)
        if existing is it:
            merged.append(it)
        # 같은 paper면 둘 다 갖고 있으니 skip

    for it in arxiv_items:
        existing = key_or_add(it)
        if existing is it:
            merged.append(it)
        else:
            # arXiv에만 있는 필드 보강
            for k in ("pdf_url", "comment", "primary_category"):
                if not existing.get(k) and it.get(k):
                    existing[k] = it[k]
            if not existing.get("arxiv_id") and it.get("arxiv_id"):
                existing["arxiv_id"] = it["arxiv_id"]

    return merged


def score(item: dict, keyword: str, required: list[str], preferred: list[str]) -> tuple[float, dict]:
    venue = item.get("venue_raw", "") or ""
    comment = item.get("comment", "") or ""
    reasons = {}

    s = 0.0
    matched_required = [v for v in required if venue_match(venue, v, comment)]
    if matched_required:
        s += 100.0 * len(matched_required)
        reasons["required_match"] = matched_required

    matched_pref = [v for v in preferred if venue_match(venue, v, comment)]
    if matched_pref:
        s += 50.0
        reasons["preferred_match"] = matched_pref

    citations = item.get("citation_count", 0) or 0
    if citations > 0:
        cs = 10.0 * math.log1p(citations)
        s += cs
        reasons["citation_score"] = round(cs, 2)

    influential = item.get("influential_citation_count", 0) or 0
    if influential > 0:
        s += 5.0 * influential
        reasons["influential"] = influential

    kw_tokens = [t.lower() for t in re.findall(r"[a-zA-Z]+", keyword)]
    text = ((item.get("title") or "") + " " + (item.get("abstract") or "")).lower()
    kw_hits = sum(1 for t in kw_tokens if t in text)
    if kw_hits:
        s += 3.0 * kw_hits
        reasons["keyword_hits"] = kw_hits

    if item.get("year"):
        try:
            y = int(item["year"])
            s += max(0.0, (y - 2018) * 1.5)
            reasons["recency_bonus"] = round(max(0.0, (y - 2018) * 1.5), 2)
        except Exception:
            pass

    return s, reasons


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arxiv", required=True)
    ap.add_argument("--s2", required=True)
    ap.add_argument("--required-venues", default="", help="comma-separated venues that MUST match (filtered in)")
    ap.add_argument("--preferred-venues", default="", help="comma-separated venues that boost score")
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--require-strict", action="store_true",
                    help="if set, drop papers that don't match any required venue")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    arxiv_items = json.loads(Path(args.arxiv).read_text(encoding="utf-8")) if Path(args.arxiv).exists() else []
    s2_items = json.loads(Path(args.s2).read_text(encoding="utf-8")) if Path(args.s2).exists() else []

    required = [v.strip() for v in args.required_venues.split(",") if v.strip()]
    preferred = [v.strip() for v in args.preferred_venues.split(",") if v.strip()]

    merged = merge(arxiv_items, s2_items)
    print(f"[merge] arxiv={len(arxiv_items)} s2={len(s2_items)} -> merged={len(merged)}", file=sys.stderr)

    scored = []
    for it in merged:
        s, reasons = score(it, args.keyword, required, preferred)
        if args.require_strict and required and "required_match" not in reasons:
            continue
        it["_score"] = round(s, 2)
        it["_reasons"] = reasons
        scored.append(it)

    scored.sort(key=lambda x: x["_score"], reverse=True)
    top = scored[: args.top]

    Path(args.out).write_text(json.dumps(top, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[merge] wrote top {len(top)} -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
