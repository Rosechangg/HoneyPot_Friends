---
description: 리뷰어 코멘트(received reviews) → 4단계 패턴 point-by-point response letter 생성 (reviewer-response 스킬 활용)
---

# /paper-review:respond

리뷰어 코멘트를 받았을 때 point-by-point response letter 자동 작성.

## 사용법

```
/paper-review:respond <reviewer comments path> [--manuscript=paper.docx] [--out=response.md]
```

### 예시

- `/paper-review:respond reviews.md --manuscript=paper_revised.docx`
- `/paper-review:respond reviewer_comments.pdf --out=response_letter_v2.md`

## 실행 흐름

`reviewer-response` 스킬(이 플러그인 내)을 로드하고 4단계 패턴으로 작성.

### 4단계 응답 패턴

각 코멘트마다:
1. **이해** — 리뷰어가 지적한 핵심을 paraphrase ("We appreciate the reviewer's observation that…")
2. **인정 또는 반박** — 동의/부분동의/반박 명확히 (회피·우회 금지)
3. **수정 위치** — manuscript 어느 위치에 어떻게 반영했는지 명시 (Section 4.2, L120-135)
4. **인용** — 수정된 본문 그대로 인용 (변경 추적 가능하게)

### 코멘트 유형별 템플릿

| 유형 | 응답 전략 |
|------|----------|
| Additional experiment 요구 | 실제 추가실험 결과 표 + 본문 위치 |
| Clarification 요구 | 본문 수정 + 명확화 paragraph 인용 |
| 부분동의 (방법론 의문) | 한계 명시 + 후속 연구로 패러디·약화 |
| 명백한 misread | 정중히 반박 + manuscript의 어느 줄에서 비롯되었을지 추측·보강 |
| 통계적 의문 | effect size, CI, multiple comparison correction 등 보강 |

## 입력 인자

| 플래그 | 의미 | 기본값 |
|--------|------|--------|
| `(positional)` | 리뷰어 코멘트 파일 (md/pdf/docx) | 필수 |
| `--manuscript=...` | 현재 manuscript (수정 위치 참조용) | (없으면 위치 인용 생략) |
| `--out=path` | 출력 response letter 경로 | `response_letter.md` |
| `--editor-letter` | Editor 응답까지 포함 | off |

## 출력

```markdown
# Response to Reviewers

## Reviewer 1
### Comment R1.1
> [리뷰어 원문]

**Response:**
We appreciate the reviewer's observation that…

[1-이해 / 2-인정 또는 반박 / 3-수정 위치 / 4-인용]

We have revised Section 4.2 (L120-135) to address this concern:

> [수정된 manuscript 본문 그대로 인용]

(반복)
```

## 검증과의 연계

- response letter 작성 후 `/paper-review:verify`로 *revised manuscript*를 다시 한 번 검증 권장
- 특히 추가 실험 결과가 추가된 경우 `claim-evidence-mapper`로 새 클레임 정리 필수

## 주의

- **em-dash(—) 사용 금지** ([feedback memory](C:/Users/ADMIN/.claude/projects/d--Research/memory/feedback_no_em_dash.md)) — 콜론·괄호·쉼표로 대체
- 회피·우회 표현 금지 ("We thank the reviewer" 같은 의례적 인사 최소화)
- 모든 약속(추가 실험, 본문 수정)은 *실제로* manuscript에 반영되었는지 검증
