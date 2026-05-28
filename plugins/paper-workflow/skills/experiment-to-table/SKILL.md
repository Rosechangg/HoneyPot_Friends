---
id: "skill-experiment-to-table-001"
name: experiment-to-table
description: "실험 결과 JSON/CSV를 학술 논문 테이블로 자동 변환: bold best, ±std, p-value 마커"
source: "extracted"
createdAt: "2026-04-09T10:00:00Z"
triggers:
  - "results to table"
  - "결과 테이블"
  - "format results"
  - "paper table"
  - "results_summary"
  - "all_results"
  - "실험 결과"
  - "테이블 만들"
  - "논문 표"
tags:
  - "research"
  - "paper-writing"
  - "data-formatting"
  - "experiment"
quality: 88
usageCount: 0
---

# Problem

실험 결과가 JSON이나 CSV로 저장되어 있는데, 이를 논문에 넣을 수 있는 학술 테이블로 변환하는 작업이 매번 수동이다. bold 처리, ± 표기, 통계 마커, 소수점 자릿수 통일 등 포맷팅이 반복적이고 실수하기 쉽다.

# Solution

## Step 1: 결과 파일 로드 및 구조 파악

```python
import json, pandas as pd

# JSON인 경우
with open("all_results_summary.json") as f:
    data = json.load(f)

# CSV인 경우
df = pd.read_csv("results.csv")
```

결과 구조를 먼저 파악: 모델명, 메트릭(R², RMSE, MAE, Accuracy 등), fold별 결과 여부

## Step 2: 학술 테이블 포맷 규칙

| 규칙 | 적용 |
|------|------|
| **Best score bold** | 각 메트릭 열에서 최고 성능을 **bold** 처리 |
| **mean ± std** | `0.974 ± 0.012` 형식, 소수점 3자리 통일 |
| **방향 표시** | R², Accuracy: ↑ (높을수록 좋음) / RMSE, MAE: ↓ (낮을수록 좋음) |
| **p-value 마커** | `*` p<0.05, `**` p<0.01, `***` p<0.001 |
| **3-line 스타일** | 상단 굵은 선 — 헤더 — 중간 선 — 데이터 — 하단 굵은 선 |
| **모델 순서** | Baseline → 제안 모델 순, 또는 성능 오름차순 |

## Step 3: 출력 형식별 생성

### LaTeX 출력
```
\begin{table}[t]
\caption{Comparison of model performance}
\centering
\begin{tabular}{lcccc}
\toprule
Model & R² ↑ & RMSE ↓ & MAE ↓ \\
\midrule
LSTM & 0.205 ± 0.031 & 0.892 ± 0.045 & ... \\
\textbf{PIGNN} & \textbf{0.974 ± 0.012} & \textbf{0.161 ± 0.008} & ... \\
\bottomrule
\end{tabular}
\end{table}
```

### Markdown 출력 (docx 변환용)
```
| Model | R² ↑ | RMSE ↓ | MAE ↓ |
|-------|------|--------|-------|
| LSTM | 0.205 ± 0.031 | 0.892 ± 0.045 | ... |
| **PIGNN** | **0.974 ± 0.012** | **0.161 ± 0.008** | ... |
```

### python-docx 직접 생성
```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

def create_paper_table(doc, df, metrics_direction):
    table = doc.add_table(rows=len(df)+1, cols=len(df.columns))
    table.style = 'Table Grid'
    # 3-line style 적용
    # best score bold 처리
    for col_idx, (metric, direction) in enumerate(metrics_direction.items()):
        values = df[metric].values
        best_idx = values.argmax() if direction == "↑" else values.argmin()
        # bold 처리
```

## Step 4: 자동 요약 통계

테이블 생성 시 함께 제공:
- 제안 모델 vs 최고 baseline 대비 개선율 (%)
- 통계적 유의성 검정 결과 (paired t-test 또는 Wilcoxon)
- fold별 분산이 큰 메트릭 경고
