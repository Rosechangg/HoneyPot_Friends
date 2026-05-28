---
id: "skill-figure-pipeline-001"
name: figure-pipeline
description: "gen_fig*.py 그림 스크립트 관리: 수정 후 자동 실행, stale 감지, docx 임베드 시 백업"
source: "extracted"
createdAt: "2026-04-09T10:00:00Z"
triggers:
  - "figure"
  - "gen_fig"
  - "그림"
  - "plot"
  - "chart"
  - "figure 생성"
  - "그림 스크립트"
  - "PNG"
  - "이미지 생성"
tags:
  - "research"
  - "visualization"
  - "paper-writing"
  - "automation"
quality: 90
usageCount: 0
---

# Problem

연구 프로젝트에서 `gen_fig*.py` 패턴으로 논문 그림을 생성하는데, 반복되는 문제가 있다:
1. 스크립트 수정 후 실행을 빠뜨려서 이미지가 갱신 안 됨
2. docx에 figure 임베드할 때 기존 figure가 날아감
3. 어떤 그림이 최신인지 추적이 안 됨

# Solution

## 규칙 1: 스크립트 수정 → 반드시 실행

`gen_fig*.py` 또는 figure 생성 스크립트를 수정했으면:
1. 즉시 `python <script>.py` 실행
2. 생성된 PNG/PDF를 Read 도구로 열어서 사용자에게 보여줌
3. "스크립트만 수정하고 끝"은 불완전한 작업 — 항상 실행까지가 한 세트

## 규칙 2: Stale 감지

figure 관련 작업 시작 전:
1. `gen_fig*.py` 파일들의 수정 시각 확인
2. 대응하는 출력 이미지(PNG/PDF)의 수정 시각 비교
3. 스크립트가 이미지보다 최신이면 → "stale figure 감지: {파일명}" 알림
4. 사용자에게 재생성 여부 확인 후 실행

## 규칙 3: docx 임베드 시 백업

python-docx로 figure를 docx에 넣거나 docx를 덮어쓸 때:
1. **반드시** 기존 docx를 `{원본명}_backup_{YYYYMMDD_HHMM}.docx`로 복사
2. 새 파일명으로 생성하거나, 백업 확인 후 덮어쓰기
3. 사용자에게 "기존 docx를 백업했습니다: {백업 경로}" 알림

## 규칙 4: Figure 목록 관리

프로젝트의 `paper/figures/` 디렉토리에서:
```
gen_fig1_xxx.py → fig1_xxx.png
gen_fig2_xxx.py → fig2_xxx.png
...
```
이 매핑을 파악하고, 전체 figure 상태를 요약할 수 있어야 함.

## 적용 프로젝트 패턴
- `D:\Research\PJT_DFS\ESWA\paper\figures\gen_fig*.py`
- `D:\Research\PJT_IUI\...\figures\`
- `D:\Research\PJT_SOTIF\...\figures\`
