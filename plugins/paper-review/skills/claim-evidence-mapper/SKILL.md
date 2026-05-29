---
name: claim-evidence-mapper
description: "논문 본문의 모든 contribution/numerical claim을 추출해 그것을 뒷받침하는 실험 결과·표·figure와 매핑한 표를 생성. 증거 없는 클레임은 over-claiming 위험으로 표시. submission-hardmode-v2의 Phase 2가 활용할 입력. paper-review Phase 2에서 사용"
allowed-tools: Read Write Edit Glob Grep
---

# Claim ↔ Evidence Mapper

논문에서 *모든* 주장을 추출하고 그것을 뒷받침하는 증거를 1:N 매핑한 표를 생성. **증거 없는 주장**을 시각적으로 드러내서 over-claiming을 사전 차단.

## 사용 시점

- "이 논문의 클레임 정리해줘", "어떤 주장이 증거 부족하지?"
- paper-review-orchestrator Phase 2
- submission-hardmode-v2 호출 전 입력 정제

## 입력

| 항목 | 필수 | 형식 |
|------|------|------|
| Manuscript | ✅ | `.md`, `.docx`, `.tex` 중 하나 |
| Experiment results | ⬜ | JSON/YAML (있으면 자동 cross-ref). 없으면 paper의 Results 섹션만 사용 |

## 절차

### 1. Claim 추출
다음 단서로 claim 후보 식별:
- Abstract에서 "We propose…", "We show…", "Our method achieves…"
- Introduction의 contribution 리스트 (보통 bullet)
- Results/Discussion의 수치 주장: "X% improvement", "outperforms by Y", "statistically significant"
- Conclusion의 generalization 주장

각 claim은 다음 5개 필드로 정형화:
```yaml
- id: C1
  claim: "Our method outperforms baseline by 12.3% on Dataset A"
  location: "Abstract L3, Section 4.2 Table 3"
  type: "numerical"  # contribution | numerical | comparative | causal | generalization
  scope: "Dataset A only"
  strength: "strong"  # strong | moderate | weak | unverified
```

### 2. Evidence 매핑
각 claim마다 다음 evidence 후보 검색:
- 표 안 수치 (Table N의 row/column 매칭)
- Figure 캡션 / Figure 본문 주장
- Statistical test 결과 (`p<0.05`, `F(…)=…, η²=…`, CI)
- Section 본문 paragraph 인용 (location 포함)

### 3. Mapping table 작성
출력 형식:

| ID | Claim | Type | Supporting Evidence | Stat Strength | Limitation/Risk |
|----|-------|------|---------------------|---------------|-----------------|
| C1 | …+12.3% on Dataset A | numerical | Table 3 row "Ours"; t-test p<0.001 | strong (p<0.001, n=…) | dataset-specific |
| C2 | "Method generalizes" | generalization | — | **UNVERIFIED** | over-claim risk |

### 4. Risk 분류

각 claim을 다음 4개 category로:
- **GREEN**: 증거 강함, scope 일치, 통계 transparent
- **YELLOW**: 증거 있으나 scope보다 넓게 주장 (e.g., 한 데이터셋 결과로 "robust" 주장)
- **RED**: 증거 부족 또는 missing
- **FATAL**: 주된 contribution claim에 RED가 있으면 fatal

## 출력

- `phase2_claim_evidence_map.md` — 위 표 + risk summary
- `claims.yaml` — submission-hardmode-v2 Phase 2가 그대로 소비할 수 있는 구조화 데이터

## 다음 단계

`phase2_claim_evidence_map.md`에서 RED/FATAL을 발견하면:
1. orchestrator가 사용자에게 confirmation (그 claim을 빼거나 약화할지)
2. submission-hardmode-v2가 자동으로 해당 claim을 fatal risk로 escalate
3. 수정 위치(location 필드) 그대로 must_fix.md에 들어감

## 참고

submission-hardmode-v2의 `DESIGN_SPEC.yaml`에 정의된 Phase 2 (Fatal Risk Mitigation) 컬럼 구조와 동일 — 이 스킬이 그 입력을 *사전 가공*하는 역할.
