---
description: 한국어 논문 초안을 영문 학술 논문 톤으로 번역한다 (academic-paper-basics + korean-to-english-paper-translation 스킬 결합)
---

# /paper-translate

한국어 논문 초안 또는 섹션을 영문 학술 논문 톤으로 번역한다.

## 동작

1. `korean-to-english-paper-translation` 스킬의 번역 규칙을 적용한다.
2. `academic-paper-basics` 스킬의 기본 규칙을 항상 함께 적용한다 (약어, 흐름, 톤, 숫자 표기).
3. 수식·표·인용·figure 번호는 그대로 보존하고 본문만 번역한다.
4. em-dash(`—`) 사용 금지 — 콜론·괄호·쉼표로 대체 (사용자 글로벌 규칙).

## 인자

- `$1`: 번역할 파일 경로 또는 섹션 이름. 미지정 시 사용자에게 묻는다.

## 출력

- 동일 디렉토리에 `_en.md` 접미사를 붙인 새 파일을 만든다 (원본 보존).
- 변경 후 차이를 요약해 보여준다.

## 주의

- docx가 source-of-truth인 경우 `paper-workflow` 스킬의 규칙을 따른다 (md를 따로 만들지 않고 docx에서 직접 추출).
