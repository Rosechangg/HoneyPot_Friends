---
id: "skill-paper-docx-manager-001"
name: paper-docx-manager
description: "논문 docx 버전 관리: 자동 백업, md→docx 변환 안전장치, docx source-of-truth 원칙"
source: "extracted"
createdAt: "2026-04-09T10:00:00Z"
triggers:
  - "docx"
  - "manuscript"
  - "draft"
  - "논문 변환"
  - "convert"
  - "convert_to_docx"
  - "python-docx"
  - "워드"
  - "Word"
tags:
  - "research"
  - "paper-writing"
  - "document-management"
  - "version-control"
quality: 92
usageCount: 0
---

# Problem

논문 작성 시 docx 파일 관리에서 반복되는 사고:
1. md→docx 변환 스크립트가 기존 docx를 덮어써서 사용자가 직접 넣은 figure, 수식이 소실
2. docx가 최종본인데 이전 버전 md를 참조하여 사용자 수정사항이 누락
3. `draft_v1.docx` ~ `draft_v9.docx` 수동 버전 관리로 혼란

# Solution

## 철칙 1: docx가 Source of Truth일 때 이전 md 절대 참조 금지

사용자가 docx를 기준으로 작업을 요청하면:
1. **해당 docx에서만** 내용 추출 (python-docx 또는 XML 파싱)
2. 이전 버전 md 파일을 **절대** 열거나 참조하지 않음
3. OMML 수식은 docx XML에서 직접 파싱
4. 테이블, figure 번호, keywords 등 **모든 요소**를 docx 기준으로

## 철칙 2: 덮어쓰기 전 자동 백업

`convert_to_docx.py` 등 docx 생성/변환 스크립트 실행 전:
1. 대상 경로에 기존 docx가 있는지 확인
2. 있으면 → `{원본명}_backup_{YYYYMMDD_HHMM}.docx`로 복사
3. 사용자에게 알림: "기존 파일을 백업했습니다: {경로}"
4. **없으면** → 그대로 진행

```python
import shutil
from datetime import datetime

def backup_if_exists(docx_path):
    if os.path.exists(docx_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        backup = docx_path.replace(".docx", f"_backup_{timestamp}.docx")
        shutil.copy2(docx_path, backup)
        print(f"Backed up: {backup}")
```

## 철칙 3: 버전 추적

논문 docx 파일 작업 시:
1. 현재 디렉토리에서 `*_v*.docx` 패턴의 파일 목록 파악
2. 가장 최신 버전 번호 확인
3. 새 파일 생성 시 → `{이름}_v{N+1}.docx`로 자동 네이밍 제안
4. 이전 버전과의 차이를 요약할 수 있으면 한 줄로 기록

## 철칙 4: 변환 스크립트 안전 가이드

새로운 md→docx 변환 스크립트 작성 시 반드시 포함:
- 출력 파일명을 입력과 다르게 설정 (덮어쓰기 방지)
- figure 임베드 시 이미지 경로 존재 여부 체크
- 3-line 테이블 스타일 기본 적용
- UTF-8 한글 지원 확인
