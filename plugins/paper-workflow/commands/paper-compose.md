---
description: paper-finder의 outline을 받아 academic-paper-composer 스킬을 호출해 chapter-by-chapter 본문 작성. 각 chapter마다 품질 체크, 완료 후 final evaluation.
---

# /paper-workflow:paper-compose

detailed outline → submission-ready manuscript. 각 chapter마다 iterative quality check 수행.

## 사용법

```
/paper-workflow:paper-compose <optimized_outline.md path> [--format=md|tex|docx] [--out=path/]
```

### 예시

- `/paper-workflow:paper-compose papers/human-ai-interaction/outline/optimized_outline.md`
- `/paper-workflow:paper-compose ./outline.md --format=docx --out=draft/`

## 실행 흐름

`academic-paper-composer` 스킬을 로드. 다음 단계로 진행.

### Step 1 — Outline Parsing
- `optimized_outline.md`에서 chapter 구조·핵심 주장·예상 분량 추출
- platform_style_guide.md가 있으면 (paper-finder:outline 출력) 함께 로드

### Step 2 — Chapter-by-Chapter Writing
각 chapter마다:
1. chapter 본문 작성 (academic-paper-basics 규칙 자동 적용)
2. `chapter_quality_check.py`로 7개 dimension 평가:
   - Argument coherence (1-10)
   - Evidence sufficiency (1-10)
   - Logical flow (1-10)
   - Citation accuracy (1-10)
   - Voice consistency (1-10)
   - Platform conformity (1-4)
   - Limitations stated (yes/no)
3. score < 7인 dimension은 그 chapter 재작성

### Step 3 — Cross-Chapter Consistency
- 용어 일관성 (한 개념 = 한 용어)
- 약어 정의/재사용 규칙
- chapter 간 transition 자연스러움
- 인용 일관성

### Step 4 — Final Evaluation
- `final_evaluation.py`로 10개 dimension 종합 평가
- Recommend: Submit immediately / Implement optional improvements / Required revisions
- 산출: `final_evaluation_report.md`

## 출력

```
<out>/
├── manuscript.md (또는 .tex / .docx)
├── chapter_quality_logs/
│   ├── chapter1_quality.md
│   ├── chapter2_quality.md
│   └── ...
└── final_evaluation_report.md
```

## 자동 적용되는 규칙 (paper-workflow의 기본 규칙)

- `academic-paper-basics` — 약어 정의, 흐름, 용어, 톤, 숫자 표기
- em-dash(—) 금지 ([feedback memory](../../README.md))
- `paper-docx-manager` — docx 출력 시 백업 + source-of-truth 원칙

## 입력 인자

| 플래그 | 의미 | 기본값 |
|--------|------|--------|
| `(positional)` | optimized_outline.md 경로 | 필수 |
| `--format=...` | 출력 형식 (md / tex / docx) | md |
| `--out=path/` | 출력 디렉토리 | `draft/` |
| `--platform-guide=path` | platform_style_guide.md 경로 | (outline과 같은 디렉토리 자동 탐색) |
| `--rewrite-threshold=N` | 이 점수 미만 dimension은 재작성 (기본 7) | 7 |

## 다음 단계

본문 작성 완료 후:

```bash
# 제출 전 검증
/paper-review:verify <out>/manuscript.docx --journal=<target>

# 한→영 번역 필요 시
/paper-workflow:paper-translate
```

## 다른 스킬과의 연계

- 입력: `paper-finder:outline`의 산출물 (optimized_outline.md)
- 자동 적용: `academic-paper-basics`, `paper-docx-manager`, `academic-paper-composer`
- 후속: `paper-review:verify`로 검증
