---
name: revision-workflow
description: Journal paper revision 전체 워크플로우 오케스트레이터. 리뷰어 코멘트를 받았을 때 호출 — 코멘트 파싱/분류(실험 vs 텍스트)·노력 산정 → (필요 시) 추가 실험·강건성 검증 → Response-to-Reviewers letter(표 포맷, 기존 accepted 서식 보존) → point-by-point Authors' Response 작성 → 본문 수정(green 하이라이트) → 검증까지 한 흐름으로 진행한다. reviewer-response / claim-evidence-mapper / eswa-paper-review-checklist (이 플러그인) + paper-workflow의 word-equation-rendering / experiment-to-table / paper-docx-manager / figure-pipeline를 단계별로 묶는다. 트리거: revision, 리비전, reviewer comments, response to reviewers, rebuttal, 심사평 대응.
---

# Journal Paper Revision Workflow

리뷰어 코멘트를 받은 시점부터 revised manuscript + Response-to-Reviewers 제출까지의 전체 흐름을 오케스트레이션한다. 각 단계는 전용 스킬을 호출하고, 산출물을 다음 단계로 넘긴다.

## 입력 (시작 전 확인)
- 리뷰어 코멘트 (review.txt / editor letter / PDF)
- 현재 manuscript (.docx)
- **기존에 accept된 같은 저널 response letter** (있으면 서식·톤·보일러플레이트 베이스로 재사용 — 새로 만들지 말 것)
- 실험 코드·데이터 (추가 실험이 기존 코드 재실행으로 가능한지 판단용)

## 핵심 원칙 (모든 단계 공통)
1. **톤**: 감사 + 건설적. 방어적·거절 톤 금지("infeasible", "cannot" 등 지양).
2. **변경 표시**: revised manuscript의 모든 수정은 **green 하이라이트**. response의 Edited Section에 Section/Line/Table/Eq 명시.
3. **정직성 > 과장**: 작은 마진을 "우월"로 over-claim 하지 말 것. 강건성이 marginal이면 **안정성·일반화·overfit 회피·구조 불변**으로 framing. 절대 성능 낮은 부분은 한계로 분리 기술.
4. **재사용 우선**: 추가 실험은 기존 데이터/모델/코드 재활용 우선, 신규 피험자 데이터는 최후.
5. **검증된 수치만**: 응답에 인용하는 모든 수치는 본문 표/results 파일과 재현 검증 후 사용.

---

## Phase 1 — 코멘트 파싱 & 트래킹 (분류 + 노력 산정)
리뷰어별로 코멘트를 ID로 분해(R1-1, R2-3, R4-1a ...)하고 추적 시트를 만든다.
- 각 코멘트: **분류 = 실험(experiment) / 텍스트(text) / 둘다**, 노력(★·일), 기존 자산(재사용 가능 코드/결과), 대응 전략, 수정 섹션.
- 리뷰어 간 **공통 이슈는 cross-reference**로 묶어 일관 대응.
- 산출물: `<Paper>_Reviewer_Comments.xlsx` (Source / Comment / 분류 / 추가실험 / 텍스트수정 / 노력 / 대응전략 / 수정섹션) + Cross-Reference + Work-Estimate 시트.
- **Skill:** `claim-evidence-mapper` (이 플러그인) — 각 코멘트가 요구하는 claim ↔ 뒷받침 실험/표/figure 매핑.

## Phase 2 — 추가 실험 & 강건성 검증 (실험 분류 코멘트만)
- 기존 코드 재사용으로 결과 산출 → `results.json` + 학술 표.
- **강건성 필수 점검**: 단일 split·단일 seed 결과는 multi-seed/CV·OOF로 재확인. paired test(Wilcoxon)/CI로 작은 마진의 유의성 확인. 본문 헤드라인 수치 재현으로 검증.
- over-claim 방지: 결과가 marginal이면 주장 수위를 안정성/일반화로 낮춘다 (핵심 원칙 3).
- **Skill:** `experiment-to-table` (paper-workflow) — JSON/CSV → bold-best·±std·p-value 표.

## Phase 3 — Response letter scaffold (서식 보존)
- **기존 accepted response를 복제**해 베이스로 사용 → orientation(landscape 등)·폰트·자간·표 너비·상단 보일러플레이트 **그대로 보존**, 내용만 교체.
- 표 4열: **Comment # | Reviewer's Comments | Authors' Responses | Edited Section**.
- 먼저 **리뷰어 코멘트만 채우고** Authors' Responses·Edited Section은 공백(이후 하나씩 작성).
- Editor 응답은 기존 범용 문구 재사용(감사 + green 하이라이트 안내).
- **Skill:** `paper-docx-manager` (paper-workflow) — 편집 전 백업, docx source-of-truth.

## Phase 4 — Point-by-point Authors' Response 작성
코멘트 하나씩, 추적 시트 순서대로.
- **Skill:** `reviewer-response` (이 플러그인) — 4단계 패턴(① 감사+인정 → ② 대응 요약/방법 → ③ 구체 결과·수치 → ④ 수정 위치). 대응 유형별(실험추가/해명/한계인정/Future Work) 템플릿.
- 수치 직접 인용, cross-reference로 일관성, 거절 톤 금지.

## Phase 5 — 본문 수정 (revised manuscript)
- `paper-docx-manager`로 **백업 먼저**.
- 변경 사항 **green 하이라이트**, Edited Section의 Line/Table/Eq와 일치.
- **Skill:** `word-equation-rendering` (paper-workflow) — 수식(η², Shapley, R² 등) LaTeX→Word OMML 깨짐 없이.
- **Skill:** `figure-pipeline` (paper-workflow) — 그림 재생성/재플롯·docx 임베드 백업.
- 표는 `experiment-to-table` 산출물 사용.

## Phase 6 — 검증 (제출 전, 항상 마지막)
- `verify_reviewer_response.py` 자동검증: forbidden token, 거절 톤, cross-reference, 약어 첫 등장 풀이 (reviewer-response 스킬 내장).
- **Skill:** `eswa-paper-review-checklist` (이 플러그인) — 흐름·용어·레퍼런스·표/그림·톤 표면 품질.
- (선택) 제출 직전 종합 검증은 `paper-review` 플러그인의 `/paper-review:verify` (journal-fit → claim-evidence → checklist → submission-hardmode-v2).

---

## 산출물 체크리스트
- [ ] `<Paper>_Reviewer_Comments.xlsx` (분류·노력·전략)
- [ ] `Reviewer<N>_Strategy.md` (리뷰어별 접근 전략)
- [ ] 추가 실험 `results.json` + 표 (+ 강건성 검증)
- [ ] `Response_to_Reviewers.docx` (표 포맷, 서식 보존)
- [ ] revised manuscript (green 하이라이트)
- [ ] 검증 통과 (verify 스크립트 + checklist)

## 관련 스킬 매핑
| 단계 | 스킬 | 플러그인 |
|------|------|----------|
| 1 코멘트 매핑 | claim-evidence-mapper | paper-revision |
| 2 결과 표 | experiment-to-table | paper-workflow |
| 3 백업/버전 | paper-docx-manager | paper-workflow |
| 4 응답 작성 | reviewer-response | paper-revision |
| 5 수식 | word-equation-rendering | paper-workflow |
| 5 그림 | figure-pipeline | paper-workflow |
| 6 표면 품질 | eswa-paper-review-checklist | paper-revision |
| 6 종합 검증 | submission-hardmode-v2 / paper-review-orchestrator | paper-review |
