---
description: figure 생성 스크립트 수정 후 자동 실행, stale 감지, docx 백업까지 처리한다 (figure-pipeline 스킬 활용)
---

# /paper-figure

논문용 figure 파이프라인을 안전하게 수행한다.

## 동작

1. `figure-pipeline` 스킬을 로드한다.
2. 대상 파일이 `gen_fig*.py` 패턴이면:
   - 스크립트 실행 후 생성된 이미지를 Read로 보여준다.
   - 출력 경로의 이미지 stale (스크립트 수정 시각 > 이미지 시각)을 검사한다.
3. 대상이 docx 변환을 동반하면 `paper-docx-manager` 스킬의 백업 규칙을 적용한다 (변환 전 `*_backup.docx` 생성).
4. 새 figure를 추가했다면 본문에서 figure 번호와 caption 정합성을 확인한다.

## 인자

- `$1`: 대상 figure 스크립트 (예: `figures/gen_fig3.py`) 또는 디렉토리
- `--all` (선택): 모든 `gen_fig*.py`를 일괄 재생성

## 주의

- 코드 수정 후 실행 누락은 가장 빈번한 사고 → 스크립트 수정 직후 자동 실행이 원칙.
- docx에 직접 박힌 figure가 있다면 md→docx 변환 시 figure가 소실될 수 있으므로 반드시 백업 후 변환.
