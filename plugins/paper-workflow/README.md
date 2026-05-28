# paper-workflow

영문 학술 논문 작성 통합 워크플로우 플러그인. 여러 번의 실제 논문 작업에서 축적된 규칙과 워크플로우를 10개 스킬 + 4개 슬래시 커맨드로 패키징.

## 구성

### 스킬 10개

| 카테고리 | 스킬 | 역할 |
|---------|------|------|
| 기본 규칙 | `academic-paper-basics` | 약어·흐름·용어·톤·숫자 표기 (always-apply) |
| 기본 규칙 | `eswa-paper-review-checklist` | ESWA 제출용 10가지 검토 항목 |
| 번역 | `korean-to-english-paper-translation` | 한→영 논문 번역 규칙 |
| 번역 | `word-equation-rendering` | LaTeX→Word 수식 변환 문제 해결 |
| 워크플로우 | `paper-workflow` | docx-as-source, 변환 전 백업, figure 자동실행 |
| 워크플로우 | `paper-docx-manager` | docx 버전 관리, 백업, source-of-truth 원칙 |
| 도구 | `figure-pipeline` | `gen_fig*.py` 수정→실행→stale 감지→docx 백업 |
| 도구 | `experiment-to-table` | JSON 실험 결과 → 학술 테이블 (bold best, ±std, p-value) |
| 도구 | `reviewer-response` | 리뷰어 코멘트 → point-by-point response letter |
| 구조 | `research-project-scaffold` | 연구 프로젝트 표준 구조 + git 버전 관리 |

### 슬래시 커맨드 4개

| 커맨드 | 역할 |
|--------|------|
| `/paper-workflow:paper-init` | 새 논문 프로젝트 골격 생성 |
| `/paper-workflow:paper-translate` | 한→영 번역 (기본 규칙 자동 적용) |
| `/paper-workflow:paper-review-response` | Authors' Response 생성 |
| `/paper-workflow:paper-figure` | figure 파이프라인 실행 + stale 감지 |

## 설계 원칙

- **항상 적용되는 기본 규칙:** `academic-paper-basics`는 모든 작성 작업에서 자동 트리거.
- **docx가 source-of-truth:** 유저가 Word에서 직접 수정한 내용을 md로 되돌리지 않는다.
- **변환 전 백업 필수:** md→docx 변환 시 기존 docx에 박힌 figure·수식이 소실되지 않도록 백업.
- **em-dash 금지:** 본문·응답 모두 `—` 대신 콜론·괄호·쉼표 사용.
- **figure 스크립트 수정 후 즉시 실행:** 스크립트 변경 후 이미지 재생성 누락 방지.

## 연관 플러그인

- **`siggraph-paper-skills`** — SIGGRAPH Poster + Technical Paper 전용 (본 플러그인의 규칙을 상속).
- **`paper-style-generator`** — 새 학회·저널 스타일을 PDF로부터 자동 추출.

## 유래

학습 스킬(`~/.claude/skills/omc-learned/`)의 원본은 유지되며, 본 플러그인은 marketplace 배포용 패키징 사본이다. 둘은 동일 콘텐츠를 가지지만 omc-learned는 auto-extract 시스템이 계속 관리한다.
