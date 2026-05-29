---
name: paper-workflow
description: "논문 작성 워크플로우 통합 규칙: docx 기준 작업, 변환 전 백업, figure 스크립트 자동 실행, md/docx 변환 안전 절차"
allowed-tools: Read Write Edit Bash
---

# 논문 작성 워크플로우

이 프로젝트에서 논문 관련 작업 시 반드시 따라야 하는 규칙들이다.

## 작성 파이프라인

```
paper-finder:outline 또는 직접 작성
       ↓ (optimized_outline.md)
/paper-workflow:paper-compose  ← academic-paper-composer 호출
       ↓ (chapter-by-chapter + quality check)
manuscript.md/docx
       ↓
/paper-workflow:paper-translate (필요 시 한→영)
/paper-workflow:paper-figure   (figure 생성·갱신)
       ↓
paper-review:verify  (제출 전 검증)
```

본문 작성 자체는 `academic-paper-composer` 스킬(이 플러그인 내)이 담당한다 — `/paper-workflow:paper-compose <outline.md>` 명령으로 호출. 모든 chapter마다 7-dimension quality check, 완료 후 10-dimension final evaluation.

---

## 규칙 1: docx가 최종 기준

Word docx 파일이 기준으로 주어지면, **이전 버전 md 파일을 절대 참조하지 않는다.**

- 해당 docx에서만 내용을 추출할 것
- OMML 수식은 XML에서 직접 파싱할 것
- 테이블, figure 번호, keywords 등 모든 요소를 docx 기준으로 할 것

**Why:** 유저가 docx에서 직접 수정한 내용(수식, 테이블, figure 번호 등)이 이전 md의 내용으로 덮어써져서 반영 누락이 반복되었다.

---

## 규칙 2: md→docx 변환 전 반드시 백업

`convert_to_docx.py` 등으로 md→docx 변환 시, 기존 docx 파일을 반드시 백업한다.

- 변환 전: `cp original.docx original_backup.docx`
- 또는 다른 파일명으로 생성
- 유저에게 "기존 docx를 덮어씁니다. 백업할까요?" 확인

**Why:** 유저가 Word에서 직접 추가한 figure, 수식 등이 md에는 포함되지 않으므로 변환 시 소실된다. 실제로 figure가 전부 날아간 사고가 발생했다.

---

## 규칙 3: figure 스크립트 수정 후 반드시 실행

그림 생성 스크립트(`.py`)를 수정한 후에는 **반드시 실행하여 이미지를 재생성**한다.

- `python <script>.py` 실행
- 생성된 이미지를 Read로 보여줌

**Why:** 코드만 수정하고 실행하지 않으면 불완전한 작업이다. 유저는 수정 결과를 바로 확인하고 싶어한다.

---

## 체크리스트 (작업 전 확인)

- [ ] docx 기준 작업인가? → 이전 md 참조 금지
- [ ] md→docx 변환하는가? → 기존 docx 백업 완료?
- [ ] figure 스크립트 수정했는가? → 실행하여 이미지 재생성
