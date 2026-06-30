---
description: Journal paper revision 전체 워크플로우 실행 (revision-workflow 스킬). 리뷰어 코멘트 → 분류·노력산정 → (필요시) 추가 실험·강건성 → Response letter(표) → point-by-point 응답 → 본문 수정(green) → 검증.
---

# /paper-revision:revision

리뷰어 코멘트를 받은 시점부터 revised manuscript + Response-to-Reviewers 제출까지 한 흐름으로 진행한다.

## 사용법
```
/paper-revision:revision <review comments path> [--manuscript=paper.docx] [--accepted-response=prev_response.docx] [--code=<experiment dir>]
```

### 예시
- `/paper-revision:revision review.txt --manuscript=Manuscript.docx --accepted-response=../prev/Response_to_Reviewers.docx`
- `/paper-revision:revision reviewer_comments.pdf --code=./experiments`

## 실행 흐름
`revision-workflow` 스킬을 로드해 Phase 1~6을 순서대로 수행한다:
1. **코멘트 파싱·분류** → 추적 Excel (실험 vs 텍스트, 노력, 전략) + claim-evidence 매핑
2. **추가 실험·강건성** → 기존 코드 재사용, results 표, multi-seed/OOF/paired test로 robust 확인
3. **Response letter scaffold** → 기존 accepted response 서식 보존, 4열 표, 코멘트만 먼저 채움
4. **Point-by-point 응답** → reviewer-response 4단계 패턴 (감사→대응→수치→수정위치)
5. **본문 수정** → 백업 후 green 하이라이트, word-equation-rendering / experiment-to-table
6. **검증** → verify 스크립트 + eswa-paper-review-checklist

## 원칙
- 톤: 감사 + 건설적, 거절 톤 금지
- 변경은 green 하이라이트 + Edited Section 명시
- 정직성 > 과장: marginal한 결과는 안정성·일반화로 framing
- 기존 데이터/코드 재사용 우선

세부 단계·스킬 매핑은 `revision-workflow` 스킬 참조. 응답만 단독 작성은 `/paper-revision:respond`.
