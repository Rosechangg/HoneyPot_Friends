---
description: 키워드로 arXiv + Semantic Scholar 병렬 검색 → 학회/저널 필터링 → Markdown + Word 표 레포트 + 연구 방향 제안까지 자동 실행
---

# /find-papers

키워드 기반 학술 논문 자동 수집 + 표 레포트 + 연구 방향 브레인스토밍.

## 사용법

```
/find-papers <키워드> [--required=CVPR,SIGGRAPH] [--years=2022-2026] [--top=30] [--out=papers/<slug>]
```

### 예시
- `/find-papers graph attention temporal` — 키워드만, venue는 자동 추천
- `/find-papers "vision transformer" --required=CVPR,ICCV --years=2023-2026`
- `/find-papers "graph neural network traffic" --required=KDD --top=50`

## 실행 흐름

`paper-finder` 스킬을 로드하고 다음 5단계를 순차 실행한다.

### Phase 1 — Venue 추천 (`venue-recommender`)
- 키워드 분석 → 분야 분류
- `--required`로 받은 venue는 무조건 포함
- 분야별 top venue를 `preferred`에 추가
- `references/venues.md` 카탈로그 참조

### Phase 2 — 병렬 검색
arXiv와 Semantic Scholar API를 동시에 호출. 백그라운드 Bash로 한쪽을 돌리고 메인에서 다른 쪽 실행.

```bash
# arXiv (background)
python scripts/search_arxiv.py --query "..." --years ... --max 60 \
  --out .paper-finder/arxiv.json &

# Semantic Scholar (foreground; broad search, tldr + citation)
# 기본 venue 필터 없음 — 별칭 매칭은 merge 단계에서 수행 (429 회피)
python scripts/search_semantic_scholar.py --query "..." \
  --years ... --max 60 --out .paper-finder/ss.json

wait
```

### Phase 3 — 머지 + 랭킹
DOI/arXiv-id/제목으로 dedup. venue 매칭(별칭 사전) + citation log boost + 키워드 hit + recency로 점수화.

`--required`가 있으면 사용자에게 `--require-strict`(필수 venue 외 제거) 적용 여부 확인.

### Phase 4 — 레포트 생성 (`paper-report-builder`)
- `report.md`: 표 (#/Title/Authors/Venue/Cites/TL;DR/Link) + Detailed Entries
- `report.docx`: 동일 구조 + 클릭 가능 하이퍼링크
- 기존 docx 있으면 자동 백업 (paper-workflow 규칙)

### Phase 5 — 연구 방향 제안 (`research-direction-brainstormer`)
랭킹된 논문을 컨텍스트로 `brainstorming-research-ideas` 스킬을 invoke:
- 현재 분야의 gap 3개
- 그 gap을 메우는 방향 5개
- 각 방향의 실현 가능성

먼저 `<out>/directions.md`로 저장 후, build_report.py의 `--append-directions` 옵션으로 `report.md` + `report.docx` 끝에 통합:

```bash
python scripts/build_report.py \
  --out-md "<out>/report.md" \
  --out-docx "<out>/report.docx" \
  --append-directions "<out>/directions.md"
```

이미 "Suggested Research Directions" 섹션이 있으면 idempotent하게 skip.

## 입력 인자 파싱

| 플래그 | 의미 | 기본값 |
|--------|------|--------|
| `(positional)` | 키워드 (따옴표 또는 단어 나열) | 필수 |
| `--required=...` | 콤마 구분 필수 venue | (없음) |
| `--years=YYYY-YYYY` | 연도 범위 | 최근 5년 |
| `--top=N` | 결과 상위 N개 | 30 |
| `--out=path/` | 출력 디렉토리 | `papers/<slug>/` |
| `--strict` | 필수 venue 외 제거 | off |
| `--no-brainstorm` | Phase 5 skip | off |

## 사전 확인

작업 시작 전 다음을 사용자에게 한 번 확인:
1. 필수로 포함할 venue가 있나? (없으면 자동 추천만)
2. 연도 범위 (기본 최근 5년)
3. Phase 5(연구 방향 브레인스토밍) 포함 여부

## 사후 안내

레포트 생성 후 사용자에게:
- `report.md` 경로 출력 (IDE에서 클릭 가능하게 마크다운 링크)
- `report.docx` 경로 출력
- 인상적인 논문이 보이면 그 번호를 알려주면 PDF 다운로드/요약 가능하다고 안내

## 의존성

- Python ≥ 3.9 (표준 라이브러리만)
- `python-docx` (docx 출력 시; 없으면 md만 생성하고 설치 안내)
- 선택: `S2_API_KEY` 환경변수
