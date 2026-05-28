---
id: "skill-m5h7k2-d5e6"
name: korean-to-english-paper-translation
description: "Rules and pitfalls for translating Korean academic papers to English for SCIE journal submission — covers framing, tone, terminology, and common mistakes"
source: "extracted"
createdAt: "2026-04-03T18:00:00Z"
triggers:
  - "paper translation"
  - "Korean to English"
  - "논문 영어 번역"
  - "영어 변환"
  - "SCIE submission"
tags:
  - "academic-writing"
  - "translation"
  - "paper"
quality: 90
usageCount: 0
---

# Problem

When translating Korean academic papers to English for journal submission, multiple issues arise: unnatural sentence structure, inconsistent terminology, overclaiming, and formatting errors that compound across the entire document.

# Solution

## Translation Rules

### 1. Sentence-Level
- Korean sentences are inherently longer — SPLIT when translating (one idea per English sentence)
- Korean SOV → English SVO; restructure, don't just reorder
- "~하였다" passive → vary English passive/active (not always "was performed")
- "본 연구는" → "This study" (never "we")
- "~것으로 판단된다" → avoid hedging in Results; use "indicates" or "demonstrates"

### 2. Terminology Mapping (freeze early, use everywhere)
- 준비도 → "driver readiness" (not just "readiness")
- 행동 지표 → "behavioral indicator" (not "metric", "measure")
- 합성 → "synthesis" (not "composition" except for metric name)
- 산만 유형 → "distraction type" (general) / "distraction channel" (framework-specific)
- 산출 → "computed" (for direct calculation)
- 예측 → "predicted" (for model output)
- 점수 → "value" (NOT "score" — implies judgmental quantification)

### 3. Abbreviation Protocol
- Abstract: define key abbreviation (TOR), spell out everything else (Random Forest, not RF)
- Introduction: define ALL abbreviations at first use
- Body: use abbreviation only after definition
- Tables: can use short forms
- Never define abbreviation that won't be reused

### 4. Framing Pitfalls
- Don't say "real-world" from simulator data
- Don't say "decision-support system" without implementing one
- Don't say "score" — implies scoring/grading
- Don't say "foundation for intelligent system" — too grandiose
- Don't treat supervised mapping metrics as "discovered properties"
- Subjective correlations = "supplementary evidence", not "validation"

### 5. Common Translation Mistakes
- "~을 수행하였다" → don't always use "was performed" — vary: "was conducted", "was applied", "was carried out"
- "+/-" → "±" (must convert before Word generation)
- "--" (em dash) → comma or semicolon in body (keep in reference titles only)
- "However" → use sparingly, vary with "Yet", "Nonetheless", "In contrast"
- "hereafter" → "denoted" or "referred to as"
- "This suggests" → "This finding suggests" (specify referent)

### 6. Abstract Structure (ESWA)
- 150-280 words, 8-10 sentences
- Flow: Background → Yet (gap) → To address (proposal) → To validate (method) → Results → Accordingly (conclusion)
- Every sentence connects to the next via transition word or subject chain
- No Cohen's d in abstract if value seems extreme (may raise reviewer suspicion)
- Last sentence: connect to journal scope without overclaiming

### 7. Word File Generation
- Equations: ensure multi-letter variables (DR) parsed as single token
- LaTeX `\neq` must have spaces around it: `j \neq i` not `j\neq i`
- "for all" in equations → use `\forall` symbol
- Tables: 3-line format, 100% page width, multi-row header detection
- Title: no blue underline (remove default Word Title style border)
- Page break before Introduction (Abstract on page 1)
