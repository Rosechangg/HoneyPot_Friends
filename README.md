# HoneyPot_Friends

> Claude Code 플러그인 마켓플레이스 — **학술 연구 워크플로우**: 논문 탐색·표 레포트화·작성·번역·리뷰어 응답까지 한 묶음

**Version**: 1.0.0 &nbsp;|&nbsp; **Author**: [Rosechang](https://github.com/Rosechangg) &nbsp;|&nbsp; **License**: MIT

> 영감: [orientpine/honeypot](https://github.com/orientpine/honeypot) marketplace 구조

---

## 빠른 시작

**Step 1.** 마켓플레이스 등록

```bash
/plugin marketplace add https://github.com/Rosechangg/HoneyPot_Friends
```

또는 로컬 클론 후:

```bash
git clone https://github.com/Rosechangg/HoneyPot_Friends.git
/plugin marketplace add /path/to/HoneyPot_Friends
```

**Step 2.** 플러그인 호출

```bash
# 키워드로 논문 찾고 표 레포트 + Word + 연구 방향까지
/paper-finder:find-papers "human-AI interaction" --required="CHI,IUI" --years=2023-2026

# 새 논문 프로젝트 골격 생성
/paper-workflow:paper-init

# 한→영 논문 번역 (학술 규칙 자동 적용)
/paper-workflow:paper-translate
```

---

## 플러그인 한눈에 보기

| 카테고리 | 플러그인 | 설명 |
|:--------:|----------|------|
| 탐색 | [**paper-finder**](#paper-finder) | 키워드 → arXiv + Semantic Scholar 병렬 검색 → 표 레포트(.md/.docx) → 연구 방향 제안 |
| 작성 | [**paper-workflow**](#paper-workflow) | 논문 작성 통합 워크플로우 — 기본 규칙·번역·figure·docx 관리·reviewer response |

---

<br>

# 탐색

---

## paper-finder

> 키워드와 (선택적) 필수 학회/저널을 받아 관련 논문을 자동으로 수집·랭킹·레포트화하는 5단계 파이프라인 플러그인.

### 사용법

```bash
/paper-finder:find-papers <키워드> [--required=CVPR,SIGGRAPH] [--years=2022-2026] [--top=30]
```

### 5단계 파이프라인

1. **Venue Recommendation** — 키워드 분석 → 분야 분류 → top venue 자동 추천 (사용자가 준 필수 venue는 강제 포함)
2. **Parallel Search** — arXiv API + Semantic Scholar API 병렬 호출 (rate-limit retry 자동)
3. **Merge & Rank** — DOI/arXiv-id/제목으로 dedup, venue 별칭 매칭 + citation log boost + recency 점수
4. **Report Build** — Markdown 표 + Word(.docx) 레포트 (클릭 가능한 하이퍼링크 포함)
5. **Research Direction Brainstorming** — `brainstorming-research-ideas` 스킬을 호출해 gap 3개 + 방향 5개 + 실현가능성 평가, 레포트 끝에 append

### 주요 특징

- **arXiv + Semantic Scholar 병렬 검색**: 한쪽이 rate-limit이어도 다른 쪽으로 진행
- **자동 retry/backoff**: arXiv 최대 8회 (15~180초 백오프), S2 최대 6회 + jitter
- **venue 별칭 사전**: CVPR ↔ "IEEE/CVF Conference on Computer Vision and Pattern Recognition" 등 9개 분야 매핑
- **idempotent re-run**: 같은 키워드로 다시 돌리면 캐시된 중간 산출물 재사용
- **Word docx 출력**: 클릭 가능한 하이퍼링크 + `Light Grid Accent 1` 표 스타일

### 의존성

- Python ≥ 3.9 (표준 라이브러리만)
- `python-docx` (docx 출력 시; 없으면 .md만 생성하고 안내)
- 선택: `S2_API_KEY` 환경변수 (Semantic Scholar rate limit 완화)

<details>
<summary>구성 요소 (4 Skills · 1 Command · 4 Python Scripts)</summary>

| 유형 | 항목 |
|------|------|
| Skills | `paper-finder` (오케스트레이터), `venue-recommender` (Phase 1), `paper-report-builder` (Phase 4), `research-direction-brainstormer` (Phase 5) |
| Command | `/paper-finder:find-papers` |
| Scripts | `search_arxiv.py`, `search_semantic_scholar.py`, `merge_and_rank.py`, `build_report.py` |
| References | `venues.md` (9개 분야 × top venue 카탈로그), `workflow.md` (전체 흐름) |

</details>

### 활용하는 기존 시스템 스킬

| 스킬 | Phase | 어떻게 |
|------|-------|--------|
| `academic-paper-strategist` (system) | Phase 1 | 키워드 확장 (primary/secondary/method) |
| `brainstorming-research-ideas` (system) | Phase 5 | gap 분석 + 방향 5개 + 실현가능성 |
| `creative-thinking-for-research` (system, fallback) | Phase 5 | 시스템 스킬 로드 실패 시 대체 |

---

<br>

# 작성

---

## paper-workflow

> 영문 학술 논문 작성 통합 워크플로우. 여러 번의 실제 논문 작업에서 축적된 규칙을 10개 스킬 + 4개 슬래시 커맨드로 패키징.

### 사용법

```bash
# 새 논문 프로젝트 골격 (디렉토리·.gitignore·draft·convert 스크립트)
/paper-workflow:paper-init

# 한→영 번역 (학술 규칙 자동 적용)
/paper-workflow:paper-translate

# Authors' Response 생성 (point-by-point)
/paper-workflow:paper-review-response

# figure 스크립트 수정→실행→stale 감지→docx 백업
/paper-workflow:paper-figure
```

### 설계 원칙

- **항상 적용되는 기본 규칙**: `academic-paper-basics` 스킬이 모든 작성 작업에서 자동 트리거
- **docx가 source-of-truth**: 사용자가 Word에서 직접 수정한 내용을 md로 되돌리지 않음 (figure 소실 사고 방지)
- **변환 전 백업 필수**: md→docx 변환 시 기존 docx에 박힌 figure·수식이 소실되지 않도록 자동 백업
- **em-dash 금지**: 본문·응답 모두 `—` 대신 콜론·괄호·쉼표 사용
- **figure 스크립트 수정 후 즉시 실행**: 코드 변경 후 이미지 재생성 누락 방지

<details>
<summary>구성 요소 (10 Skills · 4 Commands)</summary>

| 카테고리 | 스킬 | 역할 |
|---------|------|------|
| 기본 규칙 | `academic-paper-basics` | 약어·흐름·용어·톤·숫자 표기 (always-apply) |
| 기본 규칙 | `eswa-paper-review-checklist` | ESWA 제출용 10가지 검토 항목 |
| 번역 | `korean-to-english-paper-translation` | 한→영 논문 번역 규칙 |
| 번역 | `word-equation-rendering` | LaTeX → Word 수식 변환 문제 해결 |
| 워크플로우 | `paper-workflow` | docx-as-source, 변환 전 백업, figure 자동 실행 |
| 워크플로우 | `paper-docx-manager` | docx 버전 관리, 백업, source-of-truth 원칙 |
| 도구 | `figure-pipeline` | `gen_fig*.py` 수정 → 실행 → stale 감지 → docx 백업 |
| 도구 | `experiment-to-table` | JSON 실험 결과 → 학술 테이블 (bold best, ±std, p-value) |
| 도구 | `reviewer-response` | 리뷰어 코멘트 → point-by-point response letter |
| 구조 | `research-project-scaffold` | 연구 프로젝트 표준 구조 + git 버전 관리 |

| 슬래시 커맨드 | 역할 |
|--------------|------|
| `/paper-workflow:paper-init` | 새 논문 프로젝트 골격 생성 |
| `/paper-workflow:paper-translate` | 한→영 번역 |
| `/paper-workflow:paper-review-response` | Authors' Response 생성 |
| `/paper-workflow:paper-figure` | figure 파이프라인 실행 |

</details>

---

## 두 플러그인의 워크플로우 연계

```
                          ┌─────────────────┐
   키워드 입력 ────────▶  │  paper-finder   │ ─────▶  report.md + report.docx + directions.md
                          │  (탐색·레포트화)  │
                          └─────────────────┘
                                                              │
                                                              │ 후속: 관심 논문 선정
                                                              ▼
                          ┌─────────────────┐
   새 논문 시작 ────────▶  │  paper-workflow │ ─────▶  paper draft (md + docx) + figures + response
                          │  (작성·번역·리뷰)  │
                          └─────────────────┘
```

paper-finder가 외부 문헌 탐색·시드 잡기를 담당하고, paper-workflow가 본인 논문 작성·관리를 담당합니다.

---

## 기여 및 라이선스

- License: MIT
- Issues / PRs: <https://github.com/Rosechangg/HoneyPot_Friends/issues>
- 마켓플레이스 구조 영감: [orientpine/honeypot](https://github.com/orientpine/honeypot)
