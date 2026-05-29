---
description: paper-finder가 만든 directions.md(Phase 5)를 기반으로 academic-paper-strategist 스킬을 호출해 detailed paper outline까지 자동 생성. Phase 6에 해당.
---

# /paper-finder:outline

paper-finder 5-phase 결과(directions.md)를 받아 **실제 논문 outline**까지 자동 생성. paper-workflow의 `/paper-workflow:paper-compose`에 바로 전달 가능.

## 사용법

```
/paper-finder:outline <directions.md path> [--platform=arXiv|PhilArchive|CHI|...] [--direction=1|2|3|4|5]
```

### 예시

- `/paper-finder:outline papers/human-ai-interaction/directions.md --platform=CHI --direction=1`
- `/paper-finder:outline papers/<slug>/directions.md` (interactive: 사용자에게 방향 1~5 중 선택 요청)

## 실행 흐름

`academic-paper-strategist` 스킬을 로드하고 3-phase 실행.

### Strategist Phase 1 — Platform Analysis
- target 플랫폼 식별 (arXiv, PhilArchive, PhilSci-Archive, 학회·저널)
- 3~5편 sample paper 분석으로 스타일/포맷 학습
- 산출: `platform_style_guide.md`

### Strategist Phase 2 — Theoretical Framework
- paper-finder의 ranked.json + directions.md를 입력으로 lit search 결과 재활용
- 선택한 방향의 gap을 더 구체화 (gap_analysis.py)
- 산출: `literature_review.md`, `gap_analysis.md`

### Strategist Phase 3 — Outline Optimization
- 8~12 chapter detailed outline 작성
- reviewer perspective self-assessment (evaluate_samples.py)
- 산출: `optimized_outline.md`

## 출력 디렉토리

```
papers/<slug>/outline/
├── platform_style_guide.md
├── literature_review.md
├── gap_analysis.md
├── optimized_outline.md      # ★ 메인 산출물 (paper-workflow:paper-compose 입력)
└── reviewer_assessment.md
```

## 입력 인자

| 플래그 | 의미 | 기본값 |
|--------|------|--------|
| `(positional)` | directions.md 경로 | 필수 |
| `--platform=...` | target 플랫폼/저널 | (interactive) |
| `--direction=N` | directions.md의 N번째 방향 (1~5) | (interactive) |
| `--examples=path/` | 그 플랫폼 sample paper 폴더 | (자동 검색) |
| `--out=path/` | 출력 디렉토리 | `papers/<slug>/outline/` |

## 다음 단계

outline 생성 후 paper-workflow로 본문 작성:

```bash
/paper-workflow:paper-compose papers/<slug>/outline/optimized_outline.md
```

## 다른 스킬과의 연계

- 입력: `paper-finder` 5-phase 결과 (ranked.json, directions.md)
- 산출: `paper-workflow:academic-paper-composer`의 입력 outline
- 검증: 본문 작성 완료 후 `paper-review:verify`로 제출 전 검증
