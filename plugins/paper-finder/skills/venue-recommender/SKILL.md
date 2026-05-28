---
name: venue-recommender
description: "키워드를 입력받아 그 분야의 top 학회/저널을 추천하고, 사용자가 지정한 필수 venue와 합쳐 required/preferred 리스트를 만든다. paper-finder Phase 1에서 사용"
allowed-tools: Read Glob Grep
---

# Venue Recommender

키워드 → 분야 → top venue 추천.

## 입력
- `keyword` (string): 검색 키워드
- `must_include` (list, optional): 사용자가 강제로 포함하고 싶은 venue들

## 출력
```json
{
  "domain": "computer vision",
  "required_venues": ["CVPR", "SIGGRAPH"],
  "preferred_venues": ["ICCV", "ECCV", "NeurIPS", "ICML"],
  "search_categories": ["cs.CV", "cs.LG"],
  "reasoning": "키워드 'graph attention temporal' → CV+ML 교집합..."
}
```

## 절차

### 1. 키워드 → 분야 분류
LLM이 키워드의 도메인 토큰을 분석한다:

| 단서 | 분야 |
|------|------|
| vision, image, segmentation, detection, 3D | CV |
| nlp, language, llm, transformer | NLP |
| graph, gnn, attention | ML/Graph |
| ui, hci, user, interaction | HCI |
| rendering, shader, mesh, animation | Graphics |
| medical, ehr, clinical | Medical AI |
| time series, forecasting, anomaly | TimeSeries/IoT |
| robotics, control, slam | Robotics |
| explainable, fairness, bias | Trust ML |

### 2. 분야 → top venue (references/venues.md 참조)
- 분야별 top conference 2~5개 + top journal 1~3개
- 키워드가 여러 분야에 걸치면 (예: "vision transformer") 양쪽 분야의 top을 합친다

### 3. 필수 venue 통합
- `must_include`가 있으면 모두 `required_venues`로 강제 포함
- 추천 venue는 `preferred_venues`로 분리

### 4. arXiv category 매핑
- CV → `cs.CV`
- ML → `cs.LG, stat.ML`
- NLP → `cs.CL`
- Graphics → `cs.GR`
- HCI → `cs.HC`
- 등 (references/venues.md 매핑표 참조)

## 사용 예시

```
Input: keyword="graph attention temporal", must_include=["SIGGRAPH"]

Output:
  domain: "graph learning + temporal modeling (ML)"
  required: ["SIGGRAPH"]
  preferred: ["NeurIPS", "ICML", "ICLR", "KDD", "AAAI"]
  search_categories: ["cs.LG", "cs.AI"]
```

## 주의

- 사용자가 `must_include`를 비워두면 `required_venues`도 빈 리스트로 두고, `--require-strict` 없이 진행한다 (전체 풀에서 랭킹만).
- 최대 venue 수는 required+preferred 합쳐 8~10개 권장 (S2 API venue 파라미터 길이 제한).
