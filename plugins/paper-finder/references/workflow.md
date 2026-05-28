# Paper Finder Workflow

전체 파이프라인을 한 번에 보는 참고 문서. `paper-finder` SKILL.md가 이 흐름을 실행한다.

## End-to-End Flow

```
[User]
  ↓ keyword, must_include venues (optional), years (optional)
[Phase 1] venue-recommender
  ↓ required_venues, preferred_venues, search_categories
[Phase 2] arxiv + s2 parallel search
  ↓ arxiv.json, ss.json
[Phase 3] merge_and_rank.py
  ↓ ranked.json (top 30)
[Phase 4] paper-report-builder
  ↓ report.md, report.docx
[Phase 5] research-direction-brainstormer
  ↓ append "Suggested Research Directions" section
[User] ← report.md + report.docx (with directions)
```

## 기존 스킬 활용 매핑

| Phase | 활용 스킬 | 사용 위치 |
|-------|-----------|----------|
| Phase 1 | `academic-paper-strategist` | `references/search_strategy.md`의 키워드 확장 (primary/secondary/method) 패턴을 venue-recommender가 차용 |
| Phase 1 | `notion-rag` (옵션) | 사용자 보유 노트에서 이미 본 venue/방법론 컨텍스트 prime |
| Phase 2 | (없음, 자체 스크립트) | arXiv + S2 직접 호출 |
| Phase 3 | (없음, 자체 스크립트) | venue 별칭 사전 + citation log boost |
| Phase 4 | `paper-workflow:paper-docx-manager` | docx 백업 규칙 준수 |
| Phase 4 | `paper-workflow:experiment-to-table` | 표 포맷팅 컨벤션 (bold, ±std) 일부 차용 |
| Phase 5 | `brainstorming-research-ideas` (시스템) | 연구 방향 ideation (gap 분석 + 5개 방향 제안) |
| Phase 5 | `creative-thinking-for-research` (시스템, fallback) | brainstorming-research-ideas 실패 시 대체 |
| Phase 5 | `oh-my-claudecode:architect` (Task agent, fallback) | 시스템 스킬 둘 다 실패 시 |
| 전반 | `academic-paper-basics` | 약어/저자 표기 규칙 (et al., 학회명 약어) 적용 |
| 후처리 | `20-ml-paper-writing` (옵션) | citation/DOI 검증 (링크 dead 여부 점검) |

## 의존성

```bash
# 필수: 표준 라이브러리만 사용 (urllib, xml, json)
python --version  # >= 3.9

# .docx 출력용
pip install python-docx
```

선택:
- `S2_API_KEY` 환경변수 (rate limit 완화)
- `notion-rag` 사용 시 그 스킬의 의존성 (Notion DB 연결)

## 출력 디렉토리 컨벤션

```
<cwd>/papers/<keyword-slug>/
├── report.md              # 사용자가 바로 보는 표 + 상세
├── report.docx            # Word 레포트 (하이퍼링크 포함)
├── .paper-finder/         # 중간 산출물 (재실행 캐시)
│   ├── arxiv.json
│   ├── ss.json
│   └── ranked.json
└── (선택) papers_pdf/     # /read-paper 명령으로 다운받은 PDF
```

`<keyword-slug>`: 키워드를 소문자 + 하이픈으로 정규화 (예: "graph attention temporal" → "graph-attention-temporal")

## 실행 예시 (수동)

```bash
PLUGIN=~/.claude/plugins/marketplaces/my-marketplace/plugins/paper-finder
KEYWORD="graph attention temporal"
SLUG="graph-attention-temporal"
mkdir -p "papers/$SLUG/.paper-finder"

python "$PLUGIN/scripts/search_arxiv.py" \
  --query "$KEYWORD" --years 2022-2026 --max 60 \
  --out "papers/$SLUG/.paper-finder/arxiv.json"

python "$PLUGIN/scripts/search_semantic_scholar.py" \
  --query "$KEYWORD" --years 2022-2026 \
  --venues "CVPR,NeurIPS,ICML,ICLR,SIGGRAPH" \
  --max 60 --out "papers/$SLUG/.paper-finder/ss.json"

python "$PLUGIN/scripts/merge_and_rank.py" \
  --arxiv "papers/$SLUG/.paper-finder/arxiv.json" \
  --s2 "papers/$SLUG/.paper-finder/ss.json" \
  --required-venues "SIGGRAPH" \
  --preferred-venues "CVPR,NeurIPS,ICML,ICLR" \
  --keyword "$KEYWORD" --top 30 \
  --out "papers/$SLUG/.paper-finder/ranked.json"

python "$PLUGIN/scripts/build_report.py" \
  --input "papers/$SLUG/.paper-finder/ranked.json" \
  --keyword "$KEYWORD" \
  --required "SIGGRAPH" \
  --preferred "CVPR,NeurIPS,ICML,ICLR" \
  --out-md "papers/$SLUG/report.md" \
  --out-docx "papers/$SLUG/report.docx"
```

Phase 5는 슬래시 명령 흐름 안에서 Claude가 직접 brainstorming-research-ideas를 호출.
