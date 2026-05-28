---
id: "skill-m5h7k2-a1b2"
name: eswa-paper-review-checklist
description: "Comprehensive review checklist for ESWA (Expert Systems with Applications) paper submission - covers flow, terminology, references, figures, tables, and common pitfalls"
source: "extracted"
createdAt: "2026-04-03T18:00:00Z"
triggers:
  - "ESWA review"
  - "paper review checklist"
  - "submission checklist"
  - "논문 검토"
  - "ESWA 제출"
tags:
  - "academic-writing"
  - "ESWA"
  - "paper-review"
quality: 90
usageCount: 0
---

# Problem

When preparing a paper for ESWA submission, multiple quality dimensions must be checked systematically. Missing any dimension can lead to desk rejection or harsh reviewer feedback.

# Solution

## Pre-Submission Checklist

### 1. Sentence & Paragraph Flow
- Every consecutive sentence pair must have logical connection
- Use varied transition words: Yet, Accordingly, To this end, In turn, Building on, Nonetheless (NOT just "However")
- "However" ONLY for genuine contrasts/limitations, used sparingly (max 3-4 in entire paper)
- Avoid "This/That" without a following noun — always specify: "This finding", "This pattern", "This result"
- Break long sentences (>30 words) into shorter single-idea sentences
- Paragraph transitions: first sentence of new paragraph should connect to previous paragraph's conclusion

### 2. Terminology Consistency
- Pick ONE term per concept and use it EVERYWHERE
- "driver readiness" not just "readiness" (avoid confusion with system readiness)
- "synthesis" for combining process, "Composition R²" only for the metric name
- "behavioral indicators" consistently (not "metrics", "measures", "indices" randomly)
- "distraction type" for general concept, "distraction channel" for framework-specific unit — define the transition explicitly

### 3. Variable Naming
- If using multi-letter variables (e.g., DR), ensure OMML/Word parser handles them as single tokens
- In display equations: use standard LaTeX notation
- In inline text: $DR_{ch}$, $DR_{final}$
- Equation (6) must match variable names in equations (1)-(5)

### 4. Abbreviation Rules
- Abstract: define on first use (TOR, but NOT RF — spell out "Random Forest")
- Body: re-define at first body appearance
- Tables: can use short form (RF, WS)
- Never use abbreviation before definition
- Remove abbreviations defined but never reused (e.g., VPC, DMS)

### 5. Reference Verification
- Every in-text citation must appear in reference list AND vice versa
- Reference must actually support the claim it's cited for (verify content match)
- ISO citations: standardize format throughout (e.g., "ISO 21959, 2020" consistently)
- Reference list: alphabetical order strictly enforced
- Remove references no longer cited after edits

### 6. Figure & Table Verification
- All numerical values cited in text must match their source Table
- Figure descriptions must match actual figure content (check updated figures)
- Table borders: 3-line style (top, below header, bottom) — no vertical lines
- Table captions: above table
- Figure captions: below figure, "Fig. N." format
- Multi-row headers (e.g., Table 6): header line below the LAST header row

### 7. Framing & Overclaiming Prevention
- Directly computed metrics (η², Cohen's d from optimization target) = "synthesis accuracy", NOT "discovered properties"
- Out-of-sample prediction results = "independent validation evidence"
- Readiness = "composite of takeover performance indicators", NOT "latent psychological construct"
- Subjective correlations = "supplementary convergent validity evidence", NOT "primary validation"
- Don't say "score" — use "value" instead (score implies judgmental quantification)
- Don't claim "real-world" applicability from simulator data

### 8. ESWA Scope Alignment
- Emphasize interpretability (Shapley values, fuzzy measures) — this is the ESWA differentiator
- Frame as "multi-criteria decision-making" methodology
- Avoid pure ML framing — position the Choquet integral layer as the core contribution
- Last sentence of abstract should connect to ESWA scope without overclaiming

### 9. Statistical Reporting
- "Pearson's correlation coefficient" on first use, then just "$r$"
- Cohen's d for effect sizes
- η² for discriminability
- Report p-values with significance markers in tables
- Units: "s" not "seconds", "%" with space before

### 10. Academic Tone
- No "we" as subject — use "This study", "The proposed framework", passive voice
- No informal expressions: "drops sharply" → "deteriorates substantially"
- No direct quotes as examples: "Please grip..." → "guidance directing the driver to..."
- No "hereafter" — use "denoted" or "referred to as"
- "Accordingly" not "So", "Yet" not "But"
