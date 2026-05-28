---
name: paper-finder
description: "키워드 기반 학술 논문 자동 검색 오케스트레이터. arXiv + Semantic Scholar 병렬 검색 → venue 필터링/랭킹 → Markdown 표 + Word 레포트 생성 → 연구 방향 브레인스토밍까지 5단계 파이프라인. /find-papers 명령으로 호출"
allowed-tools: Read Write Edit Bash Glob Grep Skill Task
---

# Paper Finder

키워드와 (선택적) 필수 학회/저널 목록을 받아 관련 논문을 자동으로 수집·랭킹·레포트화하는 오케스트레이터.

## 사용 시점

다음과 같은 요청이 들어오면 이 스킬을 트리거한다.

- "X 키워드에 대해 최근 논문 찾아줘"
- "CVPR/SIGGRAPH에서 Y 관련 논문 정리해줘"
- "/find-papers" 명령
- "관련 연구 조사", "literature review", "문헌조사"

## 입력

| 항목 | 필수 | 예시 |
|------|------|------|
| 키워드 | ✅ | `"graph attention temporal"` |
| 필수 포함 venue | ⬜ | `CVPR, SIGGRAPH` (사용자 지정. 없으면 추천만) |
| 연도 범위 | ⬜ | `2022-2026` (기본: 최근 5년) |
| Top N | ⬜ | `30` (기본 30) |
| 출력 디렉토리 | ⬜ | `papers/<keyword-slug>/` (기본: 현재 디렉토리) |

## 5단계 파이프라인

### Phase 1: Venue Recommendation
**Skill:** `venue-recommender` (이 플러그인 내 sub-skill)

키워드를 분석해 그 분야의 top venue를 자동 추천한다. 사용자가 지정한 **필수 venue**가 있으면 그것을 required로 강제하고, 추천 venue는 preferred 풀에 더한다.

산출물: `required_venues = [...]`, `preferred_venues = [...]`

### Phase 2: Parallel Search
arXiv API + Semantic Scholar API를 **병렬로** 호출한다. 한 호출은 백그라운드로 돌릴 수 있다.

```bash
# 1) arXiv (rate-limit 3s/req)
python "$PLUGIN_DIR/scripts/search_arxiv.py" \
  --query "<expanded keyword>" \
  --years 2022-2026 \
  --max 60 \
  --out .paper-finder/arxiv.json

# 2) Semantic Scholar (tldr + citation; venue 매칭은 merge 단계에서)
python "$PLUGIN_DIR/scripts/search_semantic_scholar.py" \
  --query "<expanded keyword>" \
  --years 2022-2026 \
  --max 60 \
  --out .paper-finder/ss.json
# NOTE: 기본은 venue 파라미터 없이 broad search.
# venue 정확 매칭이 꼭 필요하면 `--venues "CHI,IUI,..."` 추가.
# S2 free tier에서 venue 리스트가 길면 429를 자주 받으므로 권장하지 않음.
```

키워드 확장은 `academic-paper-strategist`의 `search_strategy.md` 패턴을 따른다 (primary + secondary + methodological).

### Phase 3: Merge & Rank
DOI > arXiv ID > 정규화 제목 순으로 dedup. venue 매칭(별칭 사전 포함) + citation log boost + 키워드 hit + recency.

```bash
python "$PLUGIN_DIR/scripts/merge_and_rank.py" \
  --arxiv .paper-finder/arxiv.json \
  --s2 .paper-finder/ss.json \
  --required-venues "CVPR,SIGGRAPH" \
  --preferred-venues "NeurIPS,ICML,ICLR" \
  --keyword "<original keyword>" \
  --top 30 \
  --out .paper-finder/ranked.json
```

**필수 venue가 명시된 경우** `--require-strict` 옵션으로 해당 venue 외 논문을 제외할지 사용자에게 확인.

### Phase 4: Report (Markdown + Word)
**Skill:** `paper-report-builder`

```bash
python "$PLUGIN_DIR/scripts/build_report.py" \
  --input .paper-finder/ranked.json \
  --keyword "<keyword>" \
  --required "CVPR,SIGGRAPH" \
  --preferred "NeurIPS,ICML,ICLR" \
  --out-md papers/<slug>/report.md \
  --out-docx papers/<slug>/report.docx
```

- 표: `# | Title | Authors | Venue (Year) | Cites | TL;DR | Link`
- Link 우선순위: DOI > S2 url > arXiv abs > PDF
- python-docx 미설치 시 안내하고 md만 생성

### Phase 5: Research Direction Brainstorming
**Skill:** `research-direction-brainstormer` (이 플러그인 sub-skill, brainstorming-research-ideas로 핸드오프)

랭킹된 논문들을 컨텍스트로 사용해 발견된 gap/trend 기반 연구 방향 3~5개를 제안. 출력은 레포트 끝부분에 "## Suggested Research Directions" 섹션으로 append.

## 환경

- `$PLUGIN_DIR`: `~/.claude/plugins/marketplaces/my-marketplace/plugins/paper-finder`
- Python ≥ 3.9, `python-docx` (docx 출력 시)
- 선택: `S2_API_KEY` 환경변수 (rate limit 완화)

## 실패 모드 처리

- arXiv timeout → Semantic Scholar 결과만으로 진행
- Semantic Scholar 429 → 5/10/15초 지수 백오프 (스크립트 내장)
- venue 매칭 0건 → `--require-strict` 해제 권유
- python-docx 미설치 → md만 생성 + 설치 안내

## 출력 디렉토리 구조

```
papers/<keyword-slug>/
├── report.md
├── report.docx
└── .paper-finder/        # 중간 산출물 (재실행 시 캐시)
    ├── arxiv.json
    ├── ss.json
    └── ranked.json
```
