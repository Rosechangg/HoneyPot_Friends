---
id: "skill-reviewer-response-001"
name: reviewer-response
description: "저널 리뷰어 코멘트 파싱 → 실험 매핑 → point-by-point response letter 생성"
source: "extracted"
createdAt: "2026-04-09T10:00:00Z"
triggers:
  - "reviewer"
  - "리뷰어"
  - "revision"
  - "response letter"
  - "rebuttal"
  - "reviewer comments"
  - "리비전"
  - "심사평"
  - "point-by-point"
tags:
  - "research"
  - "paper-writing"
  - "peer-review"
  - "journal-submission"
quality: 85
usageCount: 0
---

# Problem

저널 revision 시 리뷰어 코멘트에 대한 point-by-point response를 작성하는 과정이 수동적이고 시간이 많이 걸린다. 코멘트별로 어떤 실험(A1~A10)이 대응하는지 매핑하고, 결과를 인용하고, 학술적 톤으로 응답을 작성해야 한다.

# Solution

## Step 1: 리뷰어 코멘트 구조화

Excel 또는 텍스트에서 리뷰어 코멘트를 파싱:
```
Reviewer 1:
  Comment 1.1: "The authors should clarify..."
  Comment 1.2: "It is unclear whether..."
Reviewer 2:
  Comment 2.1: "The experimental setup..."
```

각 코멘트를 분류:
- **Major**: 추가 실험 필요, 방법론 질문
- **Minor**: 표현 수정, typo, clarification
- **Positive**: 칭찬 (간단히 감사 표시)

## Step 2: 실험-코멘트 매핑

프로젝트의 실험 파일(A1~A10 등)과 결과를 스캔:
```
Comment 1.1 → A3_reactivity_analysis.py → results/A3_*.json
Comment 1.2 → A10_raw_robustness.py → results/A10_*.json
Comment 2.1 → A1_model_comparison.py → results/A1_*.json
```

## Step 3: Authors' Response 작성 패턴 (실제 example 기반)

### 구조 (4단계)
```
감사 표현 → 핵심 대응 요약 → 구체적 수정 내용 → 결론/추가 언급
```

### 대응 유형별 템플릿

**실험 추가형:**
```
We sincerely appreciate this insightful comment regarding [주제].
In response, we have conducted [실험명] to address this concern.
Specifically, [구체적 결과 1-2줄, 수치 포함].
The results, now presented in [Section X] and [Table/Figure Y],
demonstrate that [핵심 발견].
```

**텍스트 수정형:**
```
We appreciate the helpful comment regarding [주제].
In response, we have revised [Section X] to [수정 내용].
Specifically, we now [구체적 변경사항].
These additions help [목적/효과].
```

**해석/방어형:**
```
We are grateful to the reviewer for highlighting [이슈].
While [인정할 부분], [방어 논리, 수치/레퍼런스 포함].
To clarify, [추가 설명].
We have revised [Section] to reflect this interpretation.
```

**Future Work 유도형:**
```
We thank the reviewer for this valuable suggestion regarding [주제].
We agree that [제안 내용] is essential for [목적].
In the revised manuscript, we have updated [Limitation/Future Work (Section X.X)]
to explicitly include plans for [구체적 계획].
```

### 시작 문구 패턴 (톤별)
- 강한 동의: "We sincerely appreciate this insightful comment and fully agree that..."
- 일반 동의: "We appreciate the reviewer for raising this important point regarding..."
- 감사+설명: "Thank you for the valuable suggestion regarding..."
- 결과 보고: "In response, we have conducted/revised/updated..."
- cross-ref (⚠️ 같은 리뷰어 내에서만): "As also discussed in our response to [R1-2]..." — 응답은 리뷰어별로 개별 전달되므로 **다른 리뷰어의 코멘트 ID를 언급 금지**(예: Reviewer #2 응답에서 "response to R4-4d" 쓰면 안 됨). 반드시 언급이 필요하면 코멘트 ID 대신 섹션/표로 참조.

### 금지 사항
- "We disagree" → "While we understand the concern, our analysis suggests..."
- 방어적 톤 → 감사 + 추가 분석/설명
- 장황한 설명 → 핵심 3-5문장
- reviewer 코멘트 반복 → 바로 대응으로

## Step 4: Edited Section 작성 패턴

```
∙ Section X.X
- Line XXX-XXX

∙ Section Y
- Line YYY-YYY
- Figure Z / Table Z

∙ References added: Author1 et al. (YYYY); Author2 et al. (YYYY)
```

규칙:
- 수정 없음: "-"
- 여러 섹션: 점(∙)으로 구분
- Line 번호는 placeholder("- Line")로 두고 저자가 채우거나, 확정되면 정확히 명시
- 새 Figure/Table 추가 시 명시
- 새 Reference 추가 시: 저자명 + 연도를 명시 (전체 인용 정보는 manuscript References list에)
- **부연 설명·메타정보 금지**: "(highlighted in green)", "(pending)", "Brief paragraph added..." 같은 설명은 빼고 Section / Line / References / Figure / Table만 깔끔히
- **Run 서식 (IUI 확정 컨벤션 — 반드시 일치)**: 각 항목은 **별도 단락**. `∙ Section X.Y` = **bold**(검정); `- Line A-B` · `- Equation (n)` · 기타 항목 = *italic*(검정); `- Table N` · `- Figure N` = 서식 없음(일반); `∙ N References` = **bold**, 그 아래 `- Citation` = 일반. 섹션 블록 사이에는 **빈 단락 1줄**. 새 단락은 셀 기본 단락의 pPr(줄간격·spacing)을 복제해 동일하게.

## Step 5: Manuscript와 References list 동기화 (필수)

새 reference를 본문에 인용하면 반드시 manuscript 끝의 References list에도 항목 추가. 본문 citation만 추가하고 list를 빼먹는 누락이 매우 흔하므로 체크리스트로 확인:

| 항목 | 확인 |
|------|------|
| 본문 인용 `(Author et al., YYYY)` 형식 일관 | ✓ |
| References list에 해당 항목 존재 | ✓ |
| 정렬 규칙 (저널 가이드 확인) | Harvard/APA 계열(ESWA 등)은 first author lastname 알파벳 순, IEEE 계열은 citation order |
| 같은 first author 여러 paper | 연도 오름차순(같은 lastname 내 정렬) |
| 출판 연도 정확 | issue year vs print year 혼동 주의 (예: PRESENCE 27(1) 2018 issue는 (2018)로 인용) |
| DOI 포함 (있는 경우) | ✓ |
| Track-changes 시각화 | 새 항목은 초록색. 기존 list를 재정렬했다면 list 전체를 초록색으로 표시 |

리스트 정렬 방식이 저널 표준과 다르면(예: citation order로 작성됐는데 ESWA 표준은 alphabetical) 저자에게 알리고 재정렬 결정.

## Step 6: Response letter 표 포맷 (필수)

`Authors' Responses` 셀:
- 양쪽 정렬 (justify)
- 줄간격 1.5
- **가독성 위해 논리적 문단으로 분리** (여는 감사 / 본문 / 닫는 감사, 또는 코멘트 파트별). **문단 사이에 빈 단락 1줄**을 넣어 구분 — 하나의 큰 덩어리(dense block) 금지. **문단 수는 고정 아님 · 내용에 따라 유동적**: 짧은 응답(예: Editor)은 1문단으로, 긴 본문은 소주제별로 더 분할. 각 문단 줄간격 1.5·justify. 문단 재구성 시 **아래첨자/위첨자 서식(예: M_c의 c) 반드시 보존**.
- 색상: 본문은 검정. **단, 수정 위치를 가리키는 구절은 빨강 이탤릭(font color = C00000, italic)** — `<기술적 섹션명> (Section X.Y)` 형태로 표기. 예: *Evaluation metrics (Section 4.5)*, *Limitations of single-channel monitoring (Section 5.3.1)*, *Table 11*. 이 빨강 이탤릭으로 "어디를 고쳤는지"가 한눈에 보이게 함.
- 초록색은 manuscript 변경 표시 전용 (response 본문에는 사용하지 않음)

`Edited Section` 셀:
- 짧은 list 형태, **줄간격 1.5** (Authors' Responses 셀과 동일)
- Section / Line / References / Figure / Table만 포함 (위치 라벨만)
- **내용 서술 금지**: "- Definition of M_c and displayed equation", "- Worked example (50th percentile)" 같은 *무엇을 했는지* 설명은 넣지 말 것. `∙ Section 5.3.1` + `- Table 11`처럼 **위치만**. Table은 부연 없이 `- Table 11`로만.
- 부연 설명·메타정보·placeholder 안내 금지

## Step 7: 변경 표시 (manuscript)

| 변경 유형 | 시각화 |
|----------|--------|
| 새 텍스트 추가 | 초록색 (RGB 00B050) |
| 기존 텍스트 삭제·교체 | strikethrough + 초록색 (track-changes 시각화) |
| References list 재정렬 | list 전체 초록색 |
| Response letter 본문 | 색상 없음 (검정) — 초록색은 manuscript 전용 |

## Step 8: 핵심 원칙

1. **모든 코멘트에 구체적 수정 위치(Section, Line) 명시**
2. **실험 결과는 수치 직접 인용** (r=0.32, p=0.001 등)
3. **수정하지 않은 경우에도 이유 설명**
4. **관련 코멘트끼리 cross-reference — 단, 같은 리뷰어 내에서만** (응답은 리뷰어별 개별 전달 → 다른 리뷰어 코멘트 ID 언급 금지; 필요 시 섹션/표로 참조)
5. **톤은 항상 감사 + 건설적** (적극 수용 자세)
6. **revised manuscript에서 변경 부분은 초록색으로 하이라이트**
7. **새 reference 인용 시 manuscript References list에도 알파벳 순 위치에 항목 추가** (citation-list 동기화)
8. **기존 텍스트 대체 시 strikethrough + 초록색으로 삭제 표시, 새 텍스트는 초록색**
9. **Response letter 본문은 검정·양쪽정렬·줄간격 1.5. 단, 수정 위치 구절은 빨강 이탤릭(C00000)으로 표기** (`<섹션명> (Section X.Y)`, `Table N`)
10. **Edited Section은 Section / Line / References / Figure / Table만 — 메타 설명 금지. Run 서식: `∙ Section`=bold, `- Line/Equation`=italic, `- Table/Figure`=일반 (IUI 컨벤션)**
