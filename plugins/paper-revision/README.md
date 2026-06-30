# paper-revision

**Journal paper revision 워크플로우 통합 플러그인.** 리뷰어 코멘트를 받은 시점부터 revised
manuscript + Response-to-Reviewers 제출까지 한 흐름으로 묶는다. (제출 *전* 검증은 자매 플러그인
[`paper-review`](../paper-review) 담당 — 이쪽은 제출 *후* 리비전 담당.)

## 한눈에

| 구성 | 이름 | 역할 |
|------|------|------|
| **오케스트레이터** | `revision-workflow` | 리비전 전체 6단계(파싱·분류 → 실험·강건성 → letter scaffold → 응답 → 본문수정 → 검증) |
| 스킬 | `reviewer-response` | 4단계 패턴 point-by-point Authors' Response 작성 (+ verify 스크립트) |
| 스킬 | `claim-evidence-mapper` | 코멘트가 요구하는 claim ↔ 뒷받침 실험/표/figure 매핑 |
| 스킬 | `eswa-paper-review-checklist` | ESWA 표면 품질 체크리스트(흐름·용어·레퍼런스·표/그림·톤) |
| 커맨드 | `/paper-revision:revision` | 전체 워크플로우 실행 |
| 커맨드 | `/paper-revision:respond` | 응답 letter 단독 작성 |

## 워크플로우 (6단계)

1. **코멘트 파싱·분류** — 리뷰어별 ID 분해, 실험 vs 텍스트 분류, 노력 산정 → 추적 Excel
2. **추가 실험·강건성** — 기존 코드 재사용, multi-seed/OOF/paired test로 robust 확인 (over-claim 금지)
3. **Response letter scaffold** — 기존 accepted response 서식 보존(landscape·폰트·자간·표), 4열 표, 코멘트만 먼저
4. **Point-by-point 응답** — reviewer-response 4단계(감사→대응→수치→수정위치)
5. **본문 수정** — 백업 후 green 하이라이트, 수식(word-equation-rendering)·표(experiment-to-table)
6. **검증** — verify 스크립트 + eswa-paper-review-checklist

## 핵심 원칙
- 톤: 감사 + 건설적 (거절 톤 금지)
- 변경은 green 하이라이트 + Edited Section(Section/Line/Table/Eq) 명시
- **정직성 > 과장**: marginal한 결과는 안정성·일반화·구조불변으로 framing, 절대 성능 낮은 부분은 한계로 분리
- 기존 데이터/모델/코드 재사용 우선

## 자매 플러그인과의 분담
- **paper-revision** (이 플러그인): 리뷰 받은 *후* 리비전 — 코멘트 대응·응답 letter·본문 수정
- **paper-review**: 제출 *전* 검증 — journal-fit / submission-hardmode-v2 / 5-phase orchestrator
- **paper-workflow**: 작성·편집 공용 도구 — word-equation-rendering / experiment-to-table / paper-docx-manager / figure-pipeline

## 라이선스
MIT. Author: Rosechang.
