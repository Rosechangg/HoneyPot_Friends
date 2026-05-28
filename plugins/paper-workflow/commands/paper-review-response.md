---
description: 리뷰어 코멘트를 분석해 point-by-point Authors' Response를 생성한다 (reviewer-response 스킬 활용)
---

# /paper-review-response

저널 리뷰어 코멘트에 대한 Authors' Response 문서를 만든다.

## 동작

1. `reviewer-response` 스킬의 4단계 패턴과 대응 유형별 템플릿을 로드한다.
2. 리뷰어 코멘트 파일을 분석해 항목별로 분리한다.
3. 각 코멘트를 4가지 유형으로 분류한다:
   - **Major revision** — 본문 수정 + 응답
   - **Minor clarification** — 응답만, 본문 변경 최소
   - **Disagree** — 근거를 들어 정중히 반박
   - **Already addressed** — 본문 위치를 인용해 답변
4. point-by-point 응답을 마크다운/docx로 출력한다.

## 인자

- `$1`: 리뷰어 코멘트 파일 (예: `reviews/round1_reviewer1.md` 또는 docx)
- `$2` (선택): 본문 파일 (수정 위치 인용용)

## 주의

- em-dash 사용 금지 (사용자 글로벌 규칙).
- 모든 응답은 정중한 톤 + 객관적 근거 + 본문 변경 위치 명시.
- 본문을 동시에 수정해야 하는 경우 `paper-workflow` 스킬의 docx 백업 규칙을 따른다.
