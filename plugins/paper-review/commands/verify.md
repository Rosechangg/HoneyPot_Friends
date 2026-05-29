---
description: 작성한 논문을 5단계로 검증 (journal-fit → claim-evidence → surface checklist → submission-hardmode-v2 → 통합 must-fix 리스트). 본인 작성 submission-hardmode-v2 엔진이 핵심.
---

# /paper-review:verify

작성한 논문 → 제출 직전 종합 검증 → must-fix 리스트.

## 사용법

```
/paper-review:verify <manuscript path> [--journal=ESWA] [--examples=./papers/examples/] [--mode=conservative]
```

### 예시

- `/paper-review:verify paper_draft.docx --journal=ESWA`
- `/paper-review:verify paper.md --journal="ACM CHI" --examples=./papers/chi_examples/ --mode=aggressive`

## 실행 흐름

`paper-review-orchestrator` 스킬을 로드하고 5단계 실행.

### Phase 1 — Journal Fit Check (`journal-fit-checker`)
- target 저널 scope/contribution type/분량/통계 엄격성 매칭
- **FAIL** 시 후속 phase 진행 전 사용자 확인 (저널 변경 또는 강행)

### Phase 2 — Claim ↔ Evidence Mapping (`claim-evidence-mapper`)
- 모든 contribution/numerical claim 추출 → 증거 매핑 표
- RED/FATAL (증거 없는 주장) 표시
- `claims.yaml` 생성 (submission-hardmode-v2 입력용)

### Phase 3 — Surface Quality Checklist (`eswa-paper-review-checklist`)
- 문장 흐름, 용어 일관성, 약어 정의, reference verification, figure/table 번호
- 기본 규칙(`paper-workflow:academic-paper-basics`)도 동시 적용

### Phase 4 — ★ Adversarial Reviewer Simulation (`submission-hardmode-v2`)
**본 파이프라인의 메인 엔진.** Phase 1~3 산출물을 컨텍스트로 invoke.

- Hostile reviewer simulation (3종 가상 리뷰어)
- Fatal/Major/Minor risk 분류 + mitigation plan
- Novelty differentiation (paper-finder pool 있으면 교차 검증)
- Statistical rigor enforcement

산출:
- `phase4_hardmode_report.md`
- `acceptance_probability.md`
- `must_fix.md` (우선순위별)

### Phase 5 — (선택) Reviewer Response Letter (`reviewer-response`)
이미 리뷰어 코멘트를 받았다면(revision 단계) Phase 5만 호출 가능. `/paper-review:respond` 명령으로 단독 실행.

## 입력 인자

| 플래그 | 의미 | 기본값 |
|--------|------|--------|
| `(positional)` | manuscript 경로 (md/docx/tex) | 필수 |
| `--journal=...` | target 저널 명 | 필수 |
| `--examples=path/` | 그 저널 accepted paper 3~5편 폴더 | (자동 검색) |
| `--mode=...` | `conservative` (기본) / `aggressive` | conservative |
| `--related-work=path/` | paper-finder가 만든 ranked.json 경로 | (없음) |
| `--out=path/` | 출력 디렉토리 | `review/<slug>/` |

## 사전 확인

1. manuscript가 docx면 `paper-workflow:paper-docx-manager` 규칙 적용 (이전 md 참조 금지, 백업)
2. journal-fit FAIL 시 강행 여부 확인
3. claim-evidence RED 시 약화/삭제 여부 확인

## 출력 디렉토리

```
review/<paper-slug>/
├── phase1_journal_fit.md
├── phase2_claim_evidence_map.md
├── phase2_claims.yaml
├── phase3_surface_checklist.md
├── phase4_hardmode_report.md
├── phase4_acceptance_probability.md
├── phase4_must_fix.md
└── summary.md
```

## 사후 안내

- `summary.md`에서 우선순위 Top 5 must-fix 항목 출력
- acceptance probability 추정치 표시
- "이 fix들을 적용한 후 다시 /paper-review:verify로 재검증 권장" 안내

## 다른 플러그인과의 연계

- `paper-finder`로 수집한 related work pool → `--related-work` 인자로 전달 → Phase 4 novelty differentiation 강화
- 검증 완료 후 paper-workflow:paper-figure 등으로 figure 재생성·docx 재변환 흐름으로 복귀
