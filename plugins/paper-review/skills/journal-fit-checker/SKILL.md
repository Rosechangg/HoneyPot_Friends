---
name: journal-fit-checker
description: "Target 저널의 scope/typical contribution type/평균 분량/요구 통계 엄격성을 paper와 매칭해 desk rejection 위험을 사전 차단. paper-review Phase 1에서 사용. submission-hardmode-v2의 scope alignment 입력"
allowed-tools: Read Write Glob Grep WebSearch
---

# Journal Fit Checker

논문이 *target 저널과 맞는지*를 제출 전에 검증. **Desk rejection이 가장 흔한 사유**가 scope 불일치 / contribution type mismatch이므로, 이 단계에서 걸러내면 6~8주 시간 절약.

## 사용 시점

- "이 논문 ESWA에 낼만 한가?", "T-PAMI vs IJCV 어디가 맞아?"
- paper-review-orchestrator Phase 1
- /paper-review:verify 명령의 첫 단계

## 입력

| 항목 | 필수 | 비고 |
|------|------|------|
| Manuscript | ✅ | abstract + introduction이면 충분 |
| Target journal name | ✅ | "ESWA", "T-PAMI", "CHI" 등 |
| Journal examples folder | ⬜ | 3~5편 accepted paper. 없으면 WebSearch로 자동 수집 |

## 검증 차원 6개

### 1. Scope 정합성
- target 저널의 *Aims and Scope* 페이지 검색 (WebSearch)
- paper의 abstract/intro에서 주된 분야·문제·메서드 추출
- semantic match: 0~1 score

### 2. Contribution Type 매칭
저널마다 환영하는 contribution 유형이 다름:

| 저널 | 주된 contribution |
|------|------------------|
| ESWA, KBS | application-oriented, real-world dataset, system pipeline |
| T-PAMI, IJCV | methodological novelty + theoretical analysis |
| Nature Comms, npj | impact + 명확한 사회적/산업적 implication |
| CHI, IUI | user study + interaction design + qualitative depth |
| NeurIPS, ICML | new method + benchmark improvement + ablation 충분 |

paper의 contribution 리스트와 target 저널의 유형을 매칭.

### 3. 분량 정합성
- target 저널의 평균 page count + 그림/표 비율
- 본인 paper의 현재 분량과 비교 → "너무 짧음/너무 김" 경고

### 4. 통계 엄격성 요구 수준
- HCI 계열 (CHI, IMWUT): effect size + within-subjects 보고 강제
- ML 계열 (NeurIPS): multiple seeds + std deviation 강제
- 의료 (npj, MIA): CI + power analysis 강제
- 본인 paper의 통계 보고가 그 수준에 미치는지 체크

### 5. Related work 깊이
- 저널이 요구하는 related work 분량 (보통 1~2 paragraph vs 1 page 이상)
- paper-finder가 수집한 related work pool과 교차: target 저널에서 자주 인용되는 paper가 cite되어 있는지

### 6. Reviewer pool 추정
- 그 저널 최근 EIC/AE 명단 → 본인 paper의 cite와 겹치는지
- 자주 reviewer 풀에 들어가는 lab의 paper를 본인이 cite했는지 (관심 끌기)

## 출력

`phase1_journal_fit.md` — 다음 구조:

```markdown
# Journal Fit Report

## Verdict: PASS / WARN / FAIL

## Scores
| Dimension | Score | Note |
|-----------|-------|------|
| Scope 정합성 | 0.82 | (scope 페이지 발췌) |
| Contribution type | 0.65 | application 강하나 methodological novelty 약함 |
| 분량 | 0.90 | 평균 14page, 본인 12page → 약간 짧음 |
| 통계 엄격성 | 0.40 | **effect size 누락** |
| Related work 깊이 | 0.75 | top venue 5편 중 3편 cite |
| Reviewer pool fit | 0.55 | (추정) |

## Required Fixes (Pre-Submission)
1. [FATAL] effect size 보고 누락 → Results 섹션 전반 수정
2. [WARN] methodological novelty를 abstract에서 명시
3. [INFO] 분량 +2 page 권장 (related work 보강)

## Alternative Journal Recommendations
- 현재 paper가 더 잘 맞을 저널 2~3개 (점수 함께)
```

## Fail 처리

- `FAIL` 판정이 나면 orchestrator가 후속 Phase 2~4 진행 전에 *사용자 확인* 요청
- "그래도 강행" 선택 시 phase4 hardmode가 자동으로 desk rejection probability를 높게 산출
- "저널 변경" 선택 시 alternative 저널 후보 표시

## 다른 스킬과의 흐름

- 입력: paper-finder의 related work pool (있으면) → 차원 5 강화
- 출력: submission-hardmode-v2의 Phase 1 (Scope Alignment) 입력으로 사용
