---
description: 새 논문 프로젝트의 표준 디렉토리 구조와 git 초기 세팅을 만든다 (research-project-scaffold 스킬 활용)
---

# /paper-init

새 논문 프로젝트의 표준 골격을 만든다.

## 동작

1. `research-project-scaffold` 스킬을 로드해 표준 구조를 적용한다.
2. 기본 디렉토리 (`paper/`, `figures/`, `experiments/`, `data/`, `notes/`)를 생성한다.
3. `.gitignore`, `README.md`, `paper_draft.md`, `convert_to_docx.py` 골격을 추가한다.
4. `git init` 후 초기 커밋을 만든다.

## 인자

- `$1` (선택): 프로젝트 이름. 미지정 시 사용자에게 묻는다.

## 주의

- 이미 git repo가 초기화된 디렉토리에서는 기존 내용을 덮어쓰지 않고 누락된 항목만 추가한다.
- `paper-workflow` 스킬의 docx-as-source 규칙을 함께 적용한다 (이전 md 참조 금지).
