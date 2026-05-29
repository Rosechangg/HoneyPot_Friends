# paper-finder

키워드 기반 학술 논문 자동 검색 + 표 레포트 + 연구 방향 제안 플러그인.

## 무엇을 하나?

1. 사용자가 키워드 + (선택) 필수 학회/저널 입력
2. 그 분야의 top venue를 자동 추천 (`venue-recommender`)
3. arXiv + Semantic Scholar 병렬 검색
4. 중복 제거 + venue 매칭 + 인용수/recency 기반 랭킹
5. **Markdown 표 + Word(.docx)** 레포트 생성 (`paper-report-builder`)
6. 발견된 논문 기반 연구 방향 3~5개 자동 제안 (`research-direction-brainstormer` → `brainstorming-research-ideas`)
7. **★ (Phase 6, 선택) detailed paper outline 자동 생성** (`academic-paper-strategist`) — `/paper-workflow:paper-compose`에 바로 전달 가능

## 사용

```bash
# Phase 1~5: 탐색 + 표 레포트 + 방향 제안
/paper-finder:find-papers <키워드> [--required=CVPR,SIGGRAPH] [--years=2022-2026] [--top=30]

# Phase 6 (선택): 방향 → optimized outline
/paper-finder:outline papers/<slug>/directions.md --platform=<target> --direction=N
```

## 구조

```
paper-finder/
├── .claude-plugin/plugin.json
├── commands/
│   ├── find-papers.md            # Phase 1~5
│   └── outline.md                # ★ Phase 6 (academic-paper-strategist)
├── skills/
│   ├── paper-finder/             # 메인 오케스트레이터
│   ├── venue-recommender/        # Phase 1
│   ├── paper-report-builder/     # Phase 4
│   ├── research-direction-brainstormer/  # Phase 5
│   └── academic-paper-strategist/        # ★ Phase 6 (본인 자작)
│       ├── SKILL.md
│       ├── scripts/{evaluate_samples,gap_analysis}.py
│       └── references/{quality_standards,search_strategy}.md
├── scripts/
│   ├── search_arxiv.py           # arXiv API
│   ├── search_semantic_scholar.py # S2 API
│   ├── merge_and_rank.py         # dedup + ranking
│   └── build_report.py           # md + docx
├── references/
│   ├── venues.md                 # 분야별 top venue 카탈로그
│   └── workflow.md               # 전체 흐름
└── README.md
```

## 의존성

- Python ≥ 3.9 (표준 라이브러리만)
- `python-docx` (docx 출력 시)
- 선택: `S2_API_KEY` (Semantic Scholar rate limit 완화)

## Changelog

### 0.2.0 (2026-05-29)
- **★ Phase 6 신설:** `academic-paper-strategist` 스킬을 sub-skill로 번들 (본인 자작) + 신규 슬래시 명령 `/paper-finder:outline`. directions.md → optimized_outline.md 까지 자동.
- `/paper-finder:outline`은 별도 호출 (메인 `/find-papers`에는 자동 포함 안 됨 — 방향 선택이 interactive 필요).
- 산출 outline은 paper-workflow의 `/paper-compose`에 바로 전달 가능 → end-to-end 흐름 완성.

### 0.1.2 (2026-05-28)
- **arXiv:** retry 횟수 5 → 8회, 백오프 15/30/45/60/90/120/150/180s (총 최대 ~12분). 첫 호출 전 0.5–2.5s jitter + 매 retry 0–5s jitter로 두 API 동시 호출 시 lock-step 회피. **실측: 동시 호출 시 첫 5회 모두 429였던 케이스를 v0.1.2에서 통과**.
- **build_report.py:** `--append-directions <path.md>` 옵션 신설. Phase 5 결과(`directions.md`)를 기존 `report.md`/`report.docx`에 idempotent하게 append (이미 "Suggested Research Directions" 섹션 있으면 skip). docx는 naive md→docx 렌더링 (headings·tables·bullets·blockquotes).
- **build_report.py:** `--input` 옵션 optional화. `--append-directions`만으로 단독 호출 가능 (Phase 4 따로, Phase 5 따로 실행 가능).
- **lint:** 미사용 import 제거 (`WD_ALIGN_PARAGRAPH`, `RGBColor`, top-level `OxmlElement` 등).

### 0.1.1 (2026-05-28)
- **arXiv:** API URL을 `http://` → `https://`로 변경. 일부 클라이언트에서 발생하던 redirect loop (HTTP 301) 회피.
- **arXiv:** 429/5xx 응답에 대해 10/20/30/40/50초 지수 백오프 retry 추가 (`search_arxiv.py`).
- **Semantic Scholar:** 429/5xx retry를 6회 / 최대 60초 백오프로 확장.
- **Semantic Scholar:** venue 파라미터는 길게 보낼수록 429를 잘 유발해서, **기본 동작은 venue 파라미터 없이 broad search** + `merge_and_rank.py`의 별칭 사전이 client-side 매칭. 정확 매칭이 필요하면 `--venues` 명시.
- **워크플로우:** `paper-finder` SKILL.md 및 `find-papers.md`에 위 변경 반영. find-papers 명령 흐름에서 S2 호출은 venue 필터 없이 broad search 기본.

### 0.1.0 (2026-05-28)
- 초기 릴리스. 4 sub-skill + `/find-papers` 명령, arXiv + S2 병렬 검색, md+docx 레포트, brainstorming-research-ideas 통합.

## 활용하는 기존 스킬

| 스킬 | 위치 | 사용처 |
|------|------|--------|
| `academic-paper-strategist` | global | Phase 1 키워드 확장 (search_strategy 패턴) |
| `notion-rag` | global | (옵션) 본인 노트와 교차 검색 |
| `paper-workflow:paper-docx-manager` | plugin | docx 백업 규칙 |
| `paper-workflow:experiment-to-table` | plugin | 표 포맷 컨벤션 |
| `academic-paper-basics` | global | 약어/저자 표기 규칙 |
| `brainstorming-research-ideas` | system | Phase 5 연구 방향 ideation |
| `creative-thinking-for-research` | system | Phase 5 fallback |
| `oh-my-claudecode:architect` | OMC agent | Phase 5 최종 fallback |
