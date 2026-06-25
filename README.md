# HoneyPot_Friends

> Claude Code 플러그인 마켓플레이스 — **학술 연구 워크플로우**(논문 탐색·작성·제출 전 검증·리뷰어 응답) + **개발 가이드라인**

**Version**: 1.3.0 &nbsp;|&nbsp; **Author**: [Rosechang](https://github.com/Rosechangg) &nbsp;|&nbsp; **License**: MIT

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
# 1. 키워드로 논문 찾고 표 레포트 + Word + 연구 방향까지
/paper-finder:find-papers "human-AI interaction" --required="CHI,IUI" --years=2023-2026

# 2. 그 방향 중 하나 골라서 detailed outline까지 생성 (Phase 6)
/paper-finder:outline papers/<slug>/directions.md --platform=CHI --direction=1

# 3. outline → chapter-by-chapter 본문 작성 (academic-paper-composer)
/paper-workflow:paper-compose papers/<slug>/outline/optimized_outline.md

# 4. 한→영 번역 / figure 갱신
/paper-workflow:paper-translate
/paper-workflow:paper-figure

# 5. 제출 직전 종합 검증 (submission-hardmode-v2 메인 엔진)
/paper-review:verify paper.docx --journal=ESWA

# 6. 리뷰어 코멘트 받은 후 point-by-point response letter
/paper-review:respond reviews.md --manuscript=paper_revised.docx
```

---

## 플러그인 한눈에 보기

> 아래 표는 `scripts/sync_marketplace.py`가 `.claude-plugin/marketplace.json`에서 **자동 생성**합니다. 직접 수정하지 마세요 — 누군가 `plugins/`에 push하면 GitHub Actions가 갱신합니다. (각 플러그인의 자세한 설명은 아래 섹션 참고)

<!-- PLUGINS-TABLE:START -->
| 플러그인 | 버전 | 카테고리 | 설명 |
|----------|:----:|:--------:|------|
| [**paper-finder**](plugins/paper-finder) | `0.2.1` | research | 키워드 기반 학술 논문 자동 검색(arXiv + Semantic Scholar 병렬) → venue 필터링 → 표 레포트(.md/.docx) → 연구 방향 브레인스토밍 → (Phase 6) outline 자동 생성. 6-phase 파이프라인, 5 sub-skill + /find-papers + /paper-finder:outline 명령. |
| [**paper-workflow**](plugins/paper-workflow) | `1.2.0` | documentation | 영문 학술 논문 작성 통합 워크플로우. outline→chapter 본문 작성(composer), 기본 작성 규칙·한→영 번역·figure·docx 관리까지 9개 스킬 + 5개 슬래시 커맨드. (검증은 paper-review로 분리) |
| [**paper-review**](plugins/paper-review) | `0.1.0` | verification | 작성한 논문의 제출 전 최종 검증 플러그인. 본인 작성 submission-hardmode-v2를 메인 엔진으로 한 5-phase 파이프라인 (journal-fit → claim-evidence → surface checklist → hardmode → reviewer-response). 5개 스킬 + 2개 슬래시 커맨드. |
| [**karpathy-guidelines**](plugins/karpathy-guidelines) | `1.0.0` | workflow | LLM 코딩 실수를 줄이는 행동 가이드라인 4원칙(Think Before Coding · Simplicity First · Surgical Changes · Goal-Driven Execution). 원본: multica-ai/andrej-karpathy-skills (MIT). 출처·각색 내역은 plugins/karpathy-guidelines/NOTICE.md 참조. |
<!-- PLUGINS-TABLE:END -->

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

### 6단계 파이프라인

1. **Venue Recommendation** — 키워드 분석 → 분야 분류 → top venue 자동 추천 (사용자가 준 필수 venue는 강제 포함)
2. **Parallel Search** — arXiv API + Semantic Scholar API 병렬 호출 (rate-limit retry 자동)
3. **Merge & Rank** — DOI/arXiv-id/제목으로 dedup, venue 별칭 매칭 + citation log boost + recency 점수
4. **Report Build** — Markdown 표 + Word(.docx) 레포트 (클릭 가능한 하이퍼링크 포함)
5. **Research Direction Brainstorming** — `brainstorming-research-ideas` 스킬을 호출해 gap 3개 + 방향 5개 + 실현가능성 평가, 레포트 끝에 append
6. **(선택) Outline Generation** — `academic-paper-strategist` 스킬로 선택된 방향에서 detailed paper outline 생성 → 그대로 `/paper-workflow:paper-compose`에 전달 가능. `/paper-finder:outline` 명령으로 별도 호출

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
<summary>구성 요소 (5 Skills · 2 Commands · 4 Python Scripts)</summary>

| 유형 | 항목 |
|------|------|
| Skills | `paper-finder` (오케스트레이터), `venue-recommender` (Phase 1), `paper-report-builder` (Phase 4), `research-direction-brainstormer` (Phase 5), `academic-paper-strategist` (Phase 6) |
| Commands | `/paper-finder:find-papers`, `/paper-finder:outline` |
| Scripts | `search_arxiv.py`, `search_semantic_scholar.py`, `merge_and_rank.py`, `build_report.py` (+ strategist의 `evaluate_samples.py`, `gap_analysis.py`) |
| References | `venues.md` (9개 분야 × top venue), `workflow.md` (전체 흐름), strategist의 `quality_standards.md`, `search_strategy.md` |

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

# outline → chapter-by-chapter 본문 작성 (★ academic-paper-composer)
/paper-workflow:paper-compose <optimized_outline.md>

# 한→영 번역 (학술 규칙 자동 적용)
/paper-workflow:paper-translate

# Authors' Response 생성 (point-by-point) — paper-review:respond 권장
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
<summary>구성 요소 (9 Skills · 5 Commands)</summary>

| 카테고리 | 스킬 | 역할 |
|---------|------|------|
| 기본 규칙 | `academic-paper-basics` | 약어·흐름·용어·톤·숫자 표기 (always-apply) |
| 작성 ★ | `academic-paper-composer` | outline → chapter-by-chapter 본문 작성 + 7-dim quality check + 10-dim final eval |
| 번역 | `korean-to-english-paper-translation` | 한→영 논문 번역 규칙 |
| 번역 | `word-equation-rendering` | LaTeX → Word 수식 변환 문제 해결 |
| 워크플로우 | `paper-workflow` | docx-as-source, 변환 전 백업, figure 자동 실행 |
| 워크플로우 | `paper-docx-manager` | docx 버전 관리, 백업, source-of-truth 원칙 |
| 도구 | `figure-pipeline` | `gen_fig*.py` 수정 → 실행 → stale 감지 → docx 백업 |
| 도구 | `experiment-to-table` | JSON 실험 결과 → 학술 테이블 (bold best, ±std, p-value) |
| 구조 | `research-project-scaffold` | 연구 프로젝트 표준 구조 + git 버전 관리 |

| 슬래시 커맨드 | 역할 |
|--------------|------|
| `/paper-workflow:paper-init` | 새 논문 프로젝트 골격 생성 |
| `/paper-workflow:paper-compose` | ★ outline → chapter-by-chapter manuscript (composer) |
| `/paper-workflow:paper-translate` | 한→영 번역 |
| `/paper-workflow:paper-review-response` | Authors' Response 생성 (paper-review:respond 권장) |
| `/paper-workflow:paper-figure` | figure 파이프라인 실행 |

</details>

---

<br>

# 검증

---

## paper-review

> 작성한 논문의 **제출 직전 최종 검증** 플러그인. 본인 작성 `submission-hardmode-v2`를 메인 엔진으로, 그 앞단에 입력 정제·뒷단에 응답을 묶은 5-phase 파이프라인.

### 사용법

```bash
# 제출 직전 종합 검증 (5단계)
/paper-review:verify <manuscript> --journal=<저널명> [--examples=path/] [--mode=conservative]

# Revision 단계 — point-by-point response letter
/paper-review:respond <reviews> [--manuscript=path]
```

### 5-Phase 파이프라인

```
[Phase 1] journal-fit-checker              ─ scope/contribution/분량/통계 엄격성 매칭, desk reject 사전 차단
[Phase 2] claim-evidence-mapper            ─ 모든 claim → 증거 매핑 표, over-claim 표시
[Phase 3] eswa-paper-review-checklist      ─ 문장 흐름·용어·약어·reference·figure 번호 표면 품질
[Phase 4] ★ submission-hardmode-v2         ─ 본인 작성 메인 엔진 (적대적 리뷰어 3종 + fatal risk + novelty diff + stat rigor)
[Phase 5] reviewer-response                ─ (선택) 리뷰어 코멘트 받은 후 4단계 패턴 point-by-point 응답
```

### 주요 특징

- **★ submission-hardmode-v2 (본인 작성)가 핵심 엔진** — 다른 4개 스킬은 그 엔진의 입력 정제·출력 연결 역할
- **paper-finder의 related work pool** — `--related-work=path/ranked.json` 인자로 전달 시 Phase 4 novelty differentiation 강화
- **paper-workflow의 docx 규칙 상속** — manuscript가 docx면 자동 백업·source-of-truth 규칙 적용
- **acceptance probability 추정 + must_fix Top-N** — 5-phase 결과 종합

<details>
<summary>구성 요소 (5 Skills · 2 Commands)</summary>

| 스킬 | 역할 |
|------|------|
| `paper-review-orchestrator` | 5-phase 오케스트레이션 메인 |
| `journal-fit-checker` | Phase 1: 저널 scope/contribution 매칭 |
| `claim-evidence-mapper` | Phase 2: 클레임 → 증거 매핑 + risk 분류 |
| `eswa-paper-review-checklist` | Phase 3: 표면 품질 체크리스트 |
| `submission-hardmode-v2` | ★ Phase 4: 메인 검증 엔진 (본인 작성) |
| `reviewer-response` | Phase 5: 4단계 패턴 응답 letter |

| 슬래시 커맨드 | 역할 |
|--------------|------|
| `/paper-review:verify` | 5-phase 검증 |
| `/paper-review:respond` | reviewer-response 단독 호출 |

</details>

---

## 세 플러그인의 워크플로우 연계 (End-to-End)

```
                                ┌────────────────────────┐
   키워드 입력 ──────────────▶  │     paper-finder       │
                                │  Phase 1~5: 탐색·방향   │  ──▶  report.md/.docx + directions.md
                                │  Phase 6: outline 생성  │       (★ academic-paper-strategist)
                                │                        │  ──▶  optimized_outline.md
                                └───────────┬────────────┘
                                            │
                                            ▼
                                ┌────────────────────────┐
                                │    paper-workflow      │
                                │  /paper-compose        │  ──▶  manuscript.md/docx
                                │  (★ academic-paper-    │       (chapter-by-chapter
                                │     composer)          │        quality check + final eval)
                                │  + 번역·figure·docx    │
                                └───────────┬────────────┘
                                            │
                                            ▼ (paper-finder ranked.json을 --related-work으로)
                                ┌────────────────────────┐
                                │     paper-review       │
                                │  /verify (5-phase)     │  ──▶  hardmode report + must_fix.md
                                │  ★ submission-         │       + acceptance probability
                                │     hardmode-v2        │
                                │  /respond              │  ──▶  response_letter.md (revision)
                                └────────────────────────┘
```

- **paper-finder** — 외부 문헌 탐색·gap 파악·연구 방향 제안·**outline 자동 생성**
- **paper-workflow** — **outline → chapter-by-chapter 본문 작성**·번역·docx·figure 관리
- **paper-review** — 제출 직전 적대적 검증·acceptance probability 추정·리뷰어 응답

3개 플러그인의 **자작 메인 엔진 3종**:
- paper-finder: `academic-paper-strategist` (Phase 6 outline)
- paper-workflow: `academic-paper-composer` (chapter-by-chapter 본문)
- paper-review: `submission-hardmode-v2` (적대적 검증)

---

<br>

# 개발 가이드라인

---

## karpathy-guidelines

> LLM이 코딩할 때 자주 저지르는 실수(무단 가정, 과한 추상화, 요청과 무관한 리팩터링)를 줄이는 행동 가이드라인 4원칙. Andrej Karpathy의 LLM 코딩 관찰에서 유래.

> **🔗 출처(Attribution)** — 내용은 **원문 그대로(verbatim)** 가져왔습니다.
> - 원본 레포: [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (License: MIT, author: forrestchang)
> - 고정 커밋: [`2c60614`](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md) (`main`, 2026-04-20 기준)
> - 아이디어 출처: [Andrej Karpathy의 X 게시글](https://x.com/karpathy/status/2015883857489522876)
> - 전체 라이선스·각색 내역: [`plugins/karpathy-guidelines/NOTICE.md`](plugins/karpathy-guidelines/NOTICE.md)

### 4원칙

| 원칙 | 막아주는 실수 |
|------|---------------|
| **Think Before Coding** | 무단 가정, 숨겨진 혼란, 트레이드오프 누락 |
| **Simplicity First** | 과한 복잡도, 비대한 추상화 |
| **Surgical Changes** | 요청과 무관한 수정, 건드리면 안 되는 코드 변경 |
| **Goal-Driven Execution** | 모호한 성공 기준 → tests-first 검증으로 전환 |

### 사용법

별도 슬래시 커맨드 없이, 코드 작성·리뷰·리팩터링 시 스킬이 자동 트리거되거나 명시적으로 로드되어 가이드라인으로 동작합니다. 마켓플레이스를 등록한 친구들은 각자 환경에서 그대로 적용할 수 있습니다.

---

<br>

# 기여 방법 (자동 동기화)

> 친구들이 플러그인을 추가하거나 고칠 때 **마켓플레이스 등록·README 표를 직접 손댈 필요가 없습니다.** `plugins/` 폴더만 바꿔서 push하면 GitHub Actions가 나머지를 맞춰줍니다.

### 새 플러그인 추가하기

1. `plugins/<내-플러그인>/.claude-plugin/plugin.json` 작성 (필수: `name`, 권장: `version`, `description`, `author`, `license`)
2. `plugins/<내-플러그인>/skills/`, `commands/`, `agents/` 에 내용 추가
3. `main`에 push (또는 PR)

### push하면 자동으로 일어나는 일 ([`.github/workflows/sync-marketplace.yml`](.github/workflows/sync-marketplace.yml))

| 단계 | 내용 |
|------|------|
| 검증 | 모든 `plugin.json` / `marketplace.json` JSON 유효성 + `name` 존재 확인 (PR은 여기까지) |
| 등록 | `plugins/`에 있는데 `marketplace.json`에 없는 플러그인을 **자동 등록**, 사라진 폴더의 항목은 제거 |
| 동기화 | 각 플러그인의 `version`과 `skills`/`commands`/`agents` 파일 목록을 `marketplace.json`에 반영 + 마켓플레이스 버전 patch bump |
| 표 갱신 | 위 "플러그인 한눈에 보기" 표를 `marketplace.json` 기준으로 재생성 |
| 되커밋 | 변경분을 `chore: auto-sync ...` 커밋으로 자동 push (main 직접 push / 수동 실행 시) |

### 규칙 (단일 진실 공급원)

- **버전·파일 목록** = 각 플러그인의 `plugin.json` + 폴더 구조가 기준 → 자동 전파됨
- **설명·author·license** = `marketplace.json`에 큐레이션된 값을 유지 (신규 플러그인만 `plugin.json`에서 채움)
- `marketplace.json`의 플러그인 배열과 README 표는 **손으로 고치지 말 것** (다음 sync가 덮어씀)
- 로컬에서 미리 맞춰보고 싶으면: `python scripts/sync_marketplace.py` (검증만: `--check`)

---

## 기여 및 라이선스

- License: MIT (이 마켓플레이스 자체). 가져온 플러그인의 원본 라이선스·출처는 각 플러그인의 `NOTICE.md`에 별도 표기.
- Issues / PRs: <https://github.com/Rosechangg/HoneyPot_Friends/issues>
- 마켓플레이스 구조 영감: [orientpine/honeypot](https://github.com/orientpine/honeypot)
- 가져온 외부 콘텐츠:
  - `karpathy-guidelines` ← [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT) · idea by [Andrej Karpathy](https://x.com/karpathy/status/2015883857489522876)
