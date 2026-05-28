---
name: paper-report-builder
description: "랭킹된 논문 JSON을 받아 Markdown 표 + Word(.docx) 레포트를 생성한다. paper-finder Phase 4에서 사용. 링크 우선순위 DOI > S2 > arXiv > PDF, docx에는 클릭 가능 하이퍼링크 삽입"
allowed-tools: Read Write Bash
---

# Paper Report Builder

랭킹된 논문 JSON → 깔끔한 표 레포트 (.md + .docx).

## 입력
- `ranked.json` (paper-finder Phase 3 결과)
- `keyword`, `required`, `preferred` (메타)
- `out-md`, `out-docx` 경로

## 출력 형식

### Markdown 표 컬럼
| # | Title | Authors | Venue (Year) | Cites | TL;DR | Link |

- Title: 120자 제한
- Authors: 3명까지 + " et al."
- TL;DR: Semantic Scholar tldr 우선, 없으면 abstract 240자
- Link: DOI > abs_url > arXiv > PDF 중 첫 번째 사용 가능한 것

### Detailed Entries 섹션
각 논문마다:
- 전체 저자
- DOI, arXiv ID, PDF URL (모두 하이퍼링크)
- Citation count
- 전체 abstract
- 점수 + 매칭 이유 (`_reasons`)

## docx 출력

- python-docx 사용. 미설치 시 md만 생성하고 안내 메시지 출력.
- 페이지 여백 1.5cm (표가 잘 들어가도록)
- Style: `Light Grid Accent 1` 표 스타일
- 하이퍼링크는 raw XML로 삽입 (python-docx 내장 미지원)

## 실행

```bash
python "$PLUGIN_DIR/scripts/build_report.py" \
  --input .paper-finder/ranked.json \
  --keyword "graph attention temporal" \
  --required "CVPR,SIGGRAPH" \
  --preferred "NeurIPS,ICML" \
  --out-md papers/graph-attention-temporal/report.md \
  --out-docx papers/graph-attention-temporal/report.docx
```

## 워크플로우 규칙

paper-workflow 플러그인의 docx 백업 규칙을 따른다 (`paper-docx-manager` 참조):
- 출력 docx 경로에 기존 파일이 있으면 `report_backup_<timestamp>.docx`로 백업
- 사용자가 "덮어쓰기"를 명시한 경우만 백업 생략

## 의존성 안내

python-docx 없으면:
```bash
pip install python-docx
```
