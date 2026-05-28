---
id: "skill-research-project-scaffold-001"
name: research-project-scaffold
description: "연구 프로젝트 표준 디렉토리 구조 생성, 실험→논문 파이프라인 boilerplate 제공"
source: "extracted"
createdAt: "2026-04-09T10:00:00Z"
triggers:
  - "new project"
  - "새 프로젝트"
  - "scaffold"
  - "init research"
  - "프로젝트 생성"
  - "프로젝트 구조"
  - "project setup"
  - "initialize"
tags:
  - "research"
  - "project-management"
  - "automation"
  - "scaffold"
quality: 82
usageCount: 0
---

# Problem

새 연구 프로젝트를 시작할 때마다 디렉토리 구조를 처음부터 만들고, 기존 프로젝트에서는 v1/v2/v3/v4 폴더 복사로 버전 관리를 해서 코드 중복이 심하다. 표준화된 구조와 boilerplate가 없어서 프로젝트마다 구조가 다르다.

# Solution

## 표준 프로젝트 구조

```
PJT_{ProjectName}/
├── data/
│   ├── raw/                  # 원본 데이터 (수정 금지)
│   ├── processed/            # 전처리된 데이터
│   └── features/             # .pt, .npy 등 피처 캐시
├── src/
│   ├── models/               # PyTorch nn.Module 정의
│   ├── data/                 # Dataset, DataLoader
│   ├── analysis/             # 통계 분석, SHAP 등
│   └── utils/                # 공통 유틸리티
├── scripts/
│   ├── preprocess.py         # 데이터 전처리
│   ├── train.py              # 모델 학습
│   ├── evaluate.py           # 평가
│   └── ablation.py           # Ablation study
├── configs/
│   └── default.yaml          # 실험 설정
├── outputs/
│   ├── models/               # 학습된 모델 (.pth)
│   └── results/              # 결과 JSON/CSV
├── paper/
│   ├── figures/              # gen_fig*.py → PNG
│   ├── tables/               # 결과 테이블
│   └── drafts/               # draft_v*.docx
├── PROGRESS.md               # 실험 진행 기록
├── README.md                 # 프로젝트 개요
└── requirements.txt          # 의존성
```

## PROGRESS.md 템플릿

```markdown
# {Project Name} Progress

## 연구 목표
- 

## 실험 기록

### YYYY-MM-DD: {실험명}
- **목적:** 
- **설정:** 
- **결과:** 
- **다음 단계:** 

## 주요 발견
1. 

## TODO
- [ ] 
```

## Git 기반 버전 관리 (폴더 복사 대체)

v1/, v2/ 폴더 복사 대신:
```bash
# 새 실험 브랜치
git checkout -b exp/ablation-temporal-edges

# 실험 완료 후 결과 커밋
git add outputs/results/ablation_temporal.json
git commit -m "exp: temporal edge ablation - R²=0.89"

# main에 merge 또는 태그
git tag v2.0-temporal-edges
```

## Boilerplate 코드

### 실험 config (configs/default.yaml)
```yaml
model:
  name: "CGAT"
  hidden_dim: 64
  num_heads: 4
  dropout: 0.1

training:
  epochs: 100
  lr: 0.001
  batch_size: 32
  k_folds: 5
  seed: 42

data:
  raw_path: "data/raw/"
  processed_path: "data/processed/"
  feature_path: "data/features/"
```

### 결과 저장 패턴
```python
import json
from datetime import datetime

def save_results(results, name, output_dir="outputs/results"):
    output = {
        "experiment": name,
        "timestamp": datetime.now().isoformat(),
        "metrics": results,
    }
    path = f"{output_dir}/{name}.json"
    with open(path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
```

## 프로젝트 생성 시 체크리스트
1. 표준 구조로 디렉토리 생성
2. git init + .gitignore (data/raw/, *.pth, __pycache__)
3. PROGRESS.md 초기화
4. requirements.txt 작성
5. configs/default.yaml 작성
