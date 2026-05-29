# paper-review

작성한 논문의 **제출 전 최종 검증** 플러그인. 본인이 만든 `submission-hardmode-v2`를 메인 엔진으로, 그 앞단에 입력 정제 (journal-fit / claim-evidence / surface checklist), 뒷단에 응답 (reviewer-response)을 묶었다.

## 무엇을 하나?

1. **journal-fit-checker** — target 저널의 scope/contribution type/통계 엄격성/분량과 paper의 정합성 검증, desk rejection 사전 차단
2. **claim-evidence-mapper** — 모든 contribution/numerical claim 추출 → 증거 매핑 표 → 증거 없는 over-claim 표시
3. **eswa-paper-review-checklist** — 문장 흐름, 용어 일관성, 약어 정의, reference verification 등 표면 품질
4. **★ submission-hardmode-v2** — 메인 검증 엔진. 적대적 리뷰어 시뮬(3종) + fatal risk mitigation + novelty differentiation + statistical rigor
5. **reviewer-response** — 리뷰어 코멘트 받은 후 4단계 패턴 point-by-point response letter

## 사용

```bash
# 제출 직전 종합 검증 (5단계)
/paper-review:verify paper.docx --journal=ESWA --examples=./papers/eswa_examples/

# Revision 단계 — 리뷰어 응답만
/paper-review:respond reviews.md --manuscript=paper_revised.docx
```

## 구조

```
paper-review/
├── .claude-plugin/plugin.json
├── commands/
│   ├── verify.md                              # /paper-review:verify (5-phase)
│   └── respond.md                             # /paper-review:respond
├── skills/
│   ├── paper-review-orchestrator/             # 5-phase 오케스트레이션
│   ├── journal-fit-checker/                   # Phase 1
│   ├── claim-evidence-mapper/                 # Phase 2
│   ├── eswa-paper-review-checklist/           # Phase 3 (paper-workflow에서 이동)
│   ├── submission-hardmode-v2/                # ★ Phase 4 메인 엔진 (본인 작성)
│   │   ├── SKILL.md
│   │   ├── DESIGN_SPEC.yaml
│   │   ├── README.md
│   │   └── references/
│   └── reviewer-response/                     # Phase 5 (paper-workflow에서 이동)
└── README.md
```

## 5단계 파이프라인

```
paper draft + target journal
        ↓
[Phase 1] journal-fit-checker
        ↓ (scope/contribution/분량/통계 엄격성 매칭)
[Phase 2] claim-evidence-mapper
        ↓ (claims.yaml → submission-hardmode-v2 Phase 2 입력)
[Phase 3] eswa-paper-review-checklist
        ↓ (표면 품질 보고서)
[Phase 4] ★ submission-hardmode-v2 (메인 엔진)
        ↓ hardmode 보고서 + acceptance probability + must_fix.md
        ↓
review 결과 사용자 검토 → manuscript 수정 → 재검증
        ↓ (제출 → 리뷰어 코멘트 도착)
[Phase 5] reviewer-response
        ↓
response_letter.md (point-by-point, 4단계 패턴)
```

## 다른 플러그인과의 연계

- **paper-finder** — 수집한 related work pool을 Phase 4 novelty differentiation에 cross-ref 입력으로 전달
- **paper-workflow** — manuscript 작성·번역·figure 파이프라인이 본 플러그인의 입력 source
- **paper-review (본 플러그인)** — 제출 직전 최종 게이트

## 본인이 만든 submission-hardmode-v2가 핵심

이 플러그인은 본질적으로 `submission-hardmode-v2`라는 **본인 자작 검증 엔진**을 마켓플레이스용으로 packaging한 것. 다른 4개 스킬은 그 엔진이 더 정확하게 동작하도록 입력을 정제하거나 (Phase 1~3) 출력을 생산적으로 연결하는 (Phase 5) 역할.

`submission-hardmode-v2/DESIGN_SPEC.yaml`이 메인 엔진의 7-phase 내부 흐름을 정의한다 — orchestrator가 그것을 wrap만 한다.
