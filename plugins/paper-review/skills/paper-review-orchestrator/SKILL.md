---
name: paper-review-orchestrator
description: "작성한 논문의 제출 전 최종 검증을 5단계로 오케스트레이션. (1) journal-fit-checker로 scope 정합성, (2) claim-evidence-mapper로 클레임-증거 매핑, (3) eswa-paper-review-checklist로 표면 품질, (4) submission-hardmode-v2(메인 검증 엔진)로 적대적 리뷰어 시뮬+fatal risk+novelty diff+stat rigor, (5) reviewer-response로 응답 letter 작성. /paper-review:verify 명령으로 호출"
allowed-tools: Read Write Edit Bash Glob Grep Skill Task
---

# Paper Review Orchestrator

작성한 논문(또는 draft) + target 저널을 입력받아 제출 전 검증을 5단계로 수행하는 오케스트레이터.

## 사용 시점

- "리뷰해줘", "검증해줘", "submission hardmode", "이 논문 ESWA에 낼만 한가?"
- `/paper-review:verify` 명령

## 입력

| 항목 | 필수 | 예시 |
|------|------|------|
| Manuscript (md/docx) | ✅ | `paper_draft.docx` |
| Target journal | ✅ | `ESWA`, `T-PAMI`, `CHI`, `Nature Comms` |
| Experimental results | ⬜ | JSON/yaml (claim-evidence 매핑용) |
| Journal examples | ⬜ | 3~5편 accepted paper 폴더 |
| Mode | ⬜ | `conservative` (기본) / `aggressive` |

## 5단계 파이프라인

### Phase 1 — Journal Fit Check
**Skill:** `journal-fit-checker` (이 플러그인)

target 저널의 scope·평균 분량·요구하는 통계 엄격성·typical contribution type을 paper와 매칭. desk rejection 위험 사전 차단.

산출물: `phase1_journal_fit.md` (PASS/WARN/FAIL + 사유)

### Phase 2 — Claim ↔ Evidence Mapping
**Skill:** `claim-evidence-mapper` (이 플러그인)

paper 본문에서 모든 contribution claim·numerical claim을 추출 → 그 클레임을 뒷받침하는 실험 결과·표·figure를 매핑. **증거 없는 클레임은 over-claiming 위험**으로 표시.

산출물: `phase2_claim_evidence_map.md` (표: Claim / Supporting Result / Statistical Strength / Limitation)

### Phase 3 — Surface Quality Checklist
**Skill:** `eswa-paper-review-checklist` (이 플러그인 내, 원래 paper-workflow에서 이동됨)

- 문장 흐름·전환어 다양성
- 용어 일관성 (한 개념 = 한 용어)
- 약어 정의/재사용 규칙
- Reference verification
- Figure/table 번호 일관성
- (ESWA에 특화되지만 다른 저널에도 통용)

산출물: `phase3_surface_checklist.md`

### Phase 4 — Adversarial Reviewer Simulation (★ Main verification engine)
**Skill:** `submission-hardmode-v2` (이 플러그인 내, 본 파이프라인의 핵심)

`Skill` 도구로 `submission-hardmode-v2`를 직접 invoke. Phase 1~3의 산출물을 컨텍스트로 전달 (journal fit / claim-evidence map / surface checklist).

이 단계가 paper-review의 **메인 검증 엔진**이고 다른 phase는 모두 이 단계의 입력을 정제하는 보조 역할:
- **Hostile reviewer simulation** — gatekeeper, methodology critic, novelty critic 3종 가상 리뷰어가 reject 사유 사냥
- **Fatal risk mitigation** — desk reject / major revision / minor revision 단계별 mitigation plan
- **Novelty differentiation analysis** — paper-finder의 related work pool과 교차 검증 가능 (있으면 입력)
- **Statistical rigor enforcement** — target 저널 통계 표준에 맞춰 effect size, multiple comparison correction, power 보고 강제

산출물:
- `phase4_hardmode_report.md` — 적대적 리뷰어 코멘트 + fatal risk list + mitigation plan
- `acceptance_probability.md` — 추정 채택 확률 (저널 baseline 대비)
- `must_fix.md` — 제출 전 반드시 고쳐야 할 리스트 (Fatal > Major > Minor 우선순위)

submission-hardmode-v2의 `DESIGN_SPEC.yaml`에 정의된 5-phase 내부 흐름이 그대로 호출된다 (orchestrator가 wrap만 함).

### Phase 5 — Reviewer Response Letter (선택)
**Skill:** `reviewer-response` (이 플러그인)

이미 리뷰어 코멘트를 받은 상태(revision 단계)라면 Phase 5 단독 실행 가능. point-by-point response letter를 4단계 패턴(이해 → 인정/반박 → 수정 위치 → 인용)으로 작성.

`/paper-review:respond` 명령으로 단독 호출도 가능.

## 출력 디렉토리

```
<cwd>/review/<paper-slug>/
├── phase1_journal_fit.md
├── phase2_claim_evidence_map.md
├── phase3_surface_checklist.md
├── phase4_hardmode_report.md
├── phase5_response_letter.md       # 선택
└── summary.md                       # 5 phase 통합 요약 + acceptance probability + must-fix list
```

## 실패 모드 처리

- Phase 1 FAIL (scope 불일치) → 후속 phase 진행 전 사용자에게 "저널 변경 권유" 메시지
- Phase 2에서 증거 없는 fatal claim 발견 → Phase 4 hardmode가 자동으로 fatal risk로 escalate
- submission-hardmode-v2 미설치 → 안내 + `oh-my-claudecode:architect` 에이전트로 fallback
- Manuscript가 docx면 paper-workflow의 `paper-docx-manager` 규칙 따라 처리 (이전 md 참조 금지, 백업)

## 다른 플러그인과의 연계

- **paper-finder** → related work 풀 확보 → Phase 4 novelty differentiation의 입력
- **paper-workflow** → Manuscript 작성·번역·figure → 본 플러그인의 입력 source
- **paper-review (본 플러그인)** → 제출 직전 검증
