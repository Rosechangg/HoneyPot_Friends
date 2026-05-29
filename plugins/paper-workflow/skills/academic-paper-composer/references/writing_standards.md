# Writing Quality Standards for Academic Papers

This document defines quality evaluation criteria for systematic academic paper writing.

## Overview

Quality evaluation occurs at two levels:
1. **Chapter-level quality checks** (after each chapter is written)
2. **Final quality assessment** (before submission)

---

## Core Writing Principles (MUST FOLLOW)

These are non-negotiable principles that apply to every section of every paper. Violating any of these is a quality failure regardless of other scores.

### 1. Paragraph Flow and Representativeness

**The single most important writing principle.**

- The **first or last sentence** of every paragraph must represent (summarize or introduce) that paragraph's core message.
- Consecutive paragraphs must be **logically connected**: the reader should understand why paragraph N+1 follows paragraph N without guessing.
- When starting a new paragraph, explicitly establish its relationship to the preceding paragraph through transitional logic — not just transitional words.
- **Test**: Read only the first sentence of each paragraph in sequence. If the argument's flow is clear from these sentences alone, the writing passes.

### 2. No Bullet Points in Body Text

- Academic paper body text must be written in **prose (산문체)**, not bullet points.
- Bullet points are acceptable ONLY in:
  - Contribution lists in the Introduction (if the journal convention supports it, though prose is always preferred)
  - Enumerated items that are truly lists (e.g., sensor specifications)
- When tempted to use bullets, convert to "첫째, ... 둘째, ... 셋째, ..." prose instead.

### 3. No Internal Labels or Codes

- Never use internal project labels (e.g., C1, C2, C3, P1, P2) in the paper text. These are meaningful only to the authors and confuse readers.
- Replace with descriptive text: "The first contribution is..." rather than "C1:..."

### 4. Introduction Structure: Problem → Objective → Method → Contributions

The Introduction must follow this logical sequence:
1. **Problem definition** (research gaps, not methodology complaints)
2. **Research objective** — one clear sentence stating what this paper aims to achieve
3. **Research method** — brief description of how the objective is pursued
4. **Contributions** — what the paper delivers (in prose, without excessive numerical detail)

### 5. No Detailed Numbers in Contribution Statements

- Introduction contributions should convey **what** is achieved and **why it matters**, not enumerate specific numerical results.
- Save precise numbers (R², p-values, percentages) for the Results section.
- **Bad**: "...achieving R² improvement of +0.013 in Visual, +0.037 in Psychomotor..."
- **Good**: "...outperforming all baselines across every channel..."

### 6. Terminology Consistency

- Once a term is chosen for a concept, use that **exact same term** throughout the entire paper.
- Do NOT alternate between synonyms (e.g., switching between "driver availability" and "driver readiness" for the same concept).
- Create a terminology table during outlining and enforce it during writing.

### 7. Reference Style Must Match Target Journal

- **Before writing**, check the target journal's reference format by examining example papers.
- Common formats: numbered [1, 2] vs. author-year (Gold et al., 2013).
- Apply the correct format from the first draft — retrofitting is error-prone.

### 8. Define Concepts Before Giving Examples

- When introducing a concept (e.g., "visual distraction"), first provide a **definitional sentence** explaining what it is, then provide examples.
- **Bad**: "Visual distraction includes looking at a smartphone or adjusting the navigation system."
- **Good**: "Visual distraction refers to situations where the driver's gaze departs from the forward roadway, such as when interacting with a smartphone or navigation system."

### 9. Natural, Careful Word Choice

- Every sentence should read naturally — as if a domain expert is explaining to a peer, not as if a machine generated it.
- Avoid:
  - Unnecessarily formal or stilted phrasing
  - Redundant qualifiers ("it is important to note that...")
  - Awkward passive constructions when active voice is clearer
- When writing in Korean (for drafts), aim for the register of a well-written Korean academic paper, not translated English.

### 10. No Arrows (→) in Body Text

- Arrows and other informal symbols have no place in academic paper body text.
- Replace with prose: "이는 ... 을 의미한다" or "this leads to..." or "consequently,..."

### 11. Never Reference Non-Existent Figures or Tables

- Only reference tables and figures that actually exist in the manuscript.
- During drafting, if a figure/table is planned but not yet created, write "(Fig. X, to be added)" rather than referencing it as if it exists.

### 12. Concise Titles

- Paper titles should be concise and informative.
- Remove qualifiers that are obvious from context or that unnecessarily narrow scope (e.g., "Level 3" if the entire paper context makes this clear).
- Every word in the title should earn its place.

### 13. Frame Problems as Research Gaps, Not Method Complaints

- The "Problem" section of the Introduction should describe **what is unknown or unaddressed** in the literature (research gaps), not merely criticize a specific method's shortcomings.
- **Bad**: "Weighted sum has a limitation because it assumes independence."
- **Good**: "Existing approaches lack the ability to capture nonlinear interactions among behavioral indicators, leaving synergy and redundancy effects unmodeled."

### 14. Short, Clear Sentences — One Idea Per Sentence

- **Every sentence should convey exactly one idea.** Long compound sentences with multiple clauses and nested subclauses are the single most common readability failure in academic drafts.
- If a sentence has more than one comma-separated clause with different subjects, split it.
- **Bad**: "시각적 산만은 운전자의 시선이 전방 도로에서 이탈하여 도로 상황 파악이 지연되는 현상이며, 운동적 산만은 손이나 신체가 비운전 행위에 점유되어 물리적 제어 반응이 방해받는 상태이고, 인지적 산만은 정신적 주의가 운전 과제로부터 이탈하여 판단과 의사결정이 지연되는 상황이다."
- **Good**: "시각적 산만은 운전자의 시선이 전방 도로에서 이탈하여 도로 상황 파악이 지연되는 현상이다. 운동적 산만은 손이나 신체가 비운전 행위에 점유되어 물리적 제어 반응이 방해받는 상태이다. 인지적 산만은 정신적 주의가 운전 과제로부터 이탈하여 판단과 의사결정이 지연되는 상황이다."
- **Self-check**: Read the sentence aloud. If you need to take a breath in the middle, the sentence is too long.

### 15. No Content Repetition Between Sections

- **Introduction and Related Work must cover different content.** This is a common structural failure.
- Introduction: presents the broad problem, identifies research gaps at a high level, and states what this paper contributes.
- Related Work: provides detailed review of specific prior approaches, methods, indicators, and findings — information that was NOT in the Introduction.
- **Test**: If a reviewer could swap the Introduction's literature paragraph with a Related Work subsection and notice no difference, the sections overlap too much.
- Same principle applies between Framework and Results — Framework explains the method; Results presents findings.

### 16. Results Belong in the Results Section

- **Framework/Method sections should explain HOW things are computed, NOT report WHAT the results are.**
- Statistical test results (p-values, effect sizes), model performance numbers (R², MAE), and comparative findings all belong in the Results section.
- The Framework section should describe the methodology clearly enough that a reader could replicate the study, but should not reveal the outcome.
- **Bad** (in Framework section): "Kruskal–Wallis 검정 결과, 9개 지표 모두 유의한 차이를 보였다 (p < 0.05)."
- **Good** (in Framework section): "지표 선정의 통계적 정당화를 위해 Kruskal–Wallis 검정을 수행한다. 결과는 Section 5.1에서 보고한다."

### 17. Don't Over-Emphasize Supporting Theories

- When a theory is used as a **basis or framework** but is not the paper's main contribution, mention it briefly and move on.
- Over-emphasizing a supporting theory signals to reviewers that the paper may be padding its contribution, or that the actual contribution is weaker than claimed.
- **Guideline**: If a theory is mentioned more than 3–4 times in the Introduction, it's probably over-emphasized. Use it where it's directly relevant, then let the data speak.
- **Bad**: Repeating "MRT에 의하면..." in every paragraph of the Introduction.
- **Good**: Introduce the theory once where it justifies the channel taxonomy, then refer to it only when directly interpreting results.

### 18. Spell Out Uncommon Abbreviations

- Do NOT introduce abbreviations that are not widely recognized in the target journal's field.
- If an abbreviation would need re-explanation every time a new reader encounters it, spell out the full term instead.
- Standard abbreviations (e.g., TOR, NDRT, DMS, ADS) are fine if common in the field.
- Custom abbreviations created for the paper (e.g., "VPC" for "Visual-Psychomotor-Cognitive") should generally be avoided — they add cognitive load without saving significant space.
- **Rule of thumb**: If the abbreviation isn't used at least 5 times AND isn't a standard term, don't abbreviate.

### 19. Explain Technical Procedures in Plain Language

- When describing methodological choices (counterbalancing, randomization, stratification, cross-validation), explain **what was done** and **why** in clear, accessible language.
- Don't just name the technique — the reader may not know it.
- **Bad**: "과제 순서는 참가자 간 역균형화하였다."
- **Good**: "시나리오 제시 순서는 참가자 간에 체계적으로 변경(counterbalancing)하여, 특정 시나리오가 항상 같은 순서에 위치함으로써 발생할 수 있는 순서 효과(피로, 학습)를 통제하였다."

### 20. Present All Baselines Fairly

- When comparing a proposed method against baselines, present the **full set** of baselines and explain why each was included.
- Don't frame the comparison as if there's only one baseline (e.g., "outperforms weighted sum") when multiple baselines exist.
- Each baseline should be briefly defined so the reader understands what it represents.
- **Bad**: "가중합의 한계를 넘어서기 위해 Choquet 적분을 제안한다."
- **Good**: "Equal WS, Manual WS, Optimal WS, OWA의 네 가지 baseline과 체계적으로 비교한다."

### 21. Balance Contribution Lengths in Introduction

- All contributions listed in the Introduction should receive approximately **equal treatment** in terms of length and detail.
- If one contribution gets a full paragraph while another gets one sentence, readers may perceive the shorter one as an afterthought.
- In the Results and Discussion sections, unequal treatment is fine (some contributions may have more complex results), but in the Introduction the framing should be balanced.

### 22. Frame Gaps Positively — "Necessity of X" Not "Limitation of Y"

- When identifying research gaps in the Introduction, frame them as the **importance or necessity** of what is needed, rather than dwelling on the **limitations** of prior work.
- This creates forward momentum and positions the paper's contribution as filling a genuine need rather than attacking predecessors.
- **Bad**: "기존 연구의 한계는 단일 지표만을 사용한다는 점이다."
- **Good**: "다중 지표의 통합적 활용은 운전자 준비도 평가의 신뢰성 향상에 필수적이다."

### 23. Results Section: Broad to Narrow Ordering

- Present results in order from the **broadest, most fundamental finding** to the **most specific or technical**.
- Start with findings that establish the overall landscape (e.g., why the problem matters, descriptive statistics), then narrow to method comparisons, and finally to theoretical implications.
- This mirrors how readers build understanding and prevents presenting technical results before the reader has context to interpret them.
- **Bad**: Starting Results with model comparison tables before showing that the problem actually exists in the data.
- **Good**: First showing cross-channel independence analysis (proving multi-channel assessment is necessary), then indicator validation, then method comparison.

### 24. Explain WHY Before Presenting Analysis

- Before presenting any statistical test, comparison, or analysis result, first explain **why this analysis is being performed** and **what question it answers**.
- The reader needs motivation before they can interpret numbers.
- **Bad**: "Table 5는 Choquet 적분과 baseline의 비교 결과를 보여준다. [table follows]"
- **Good**: "제안 프레임워크가 기존 합성 방법 대비 실질적 이점을 갖는지 검증하기 위해, Choquet 적분과 4가지 baseline의 예측 성능을 비교하였다."

### 25. Experiment Section: Standard Ordering

- The Experiment (or Experimental Setup) section should follow a consistent, reader-friendly order:
  1. **Equipment/Apparatus** (simulator, sensors, environment)
  2. **Tasks/Scenarios** (what participants were asked to do)
  3. **Participants** (demographics, recruitment, screening)
  4. **Procedure** (step-by-step flow of each session)
  5. **Data Collection & Processing** (what was recorded and how it was preprocessed)
- This order flows from the physical setup to the human element to the temporal flow to the data, which matches how a reader mentally reconstructs the experiment.

### 26. No Parenthetical Stage Labels in Framework Descriptions

- When describing a multi-stage framework or pipeline, do NOT use parenthetical labels like "(Stage 1)", "(Step A)" inline.
- Instead, describe each stage with a sentence-initial descriptor or use subsection headings.
- **Bad**: "본 프레임워크는 세 단계로 구성된다. (1단계) 행동 지표를 수집하고, (2단계) 정규화한 후, (3단계) Choquet 적분으로 합성한다."
- **Good**: "본 프레임워크는 세 단계로 구성된다. 첫째, TOR 이후 행동 데이터로부터 세 가지 지표를 추출한다. 둘째, 각 지표를 [0, 1] 구간으로 정규화한다. 셋째, 2-가법 Choquet 적분을 통해 단일 준비도 점수로 합성한다."

---

## Chapter-Level Quality Standards

### 5-Dimension Assessment (4 points each, 20 total)

After writing each chapter, evaluate against these 5 dimensions:

#### 1. Argument Quality (1-4 points)

**4 points - Excellent**:
- Thesis/claim crystal clear
- All supporting arguments logically connected
- Premises fully justified
- No logical gaps or unsupported assertions
- Counter-arguments addressed where appropriate

**3 points - Good**:
- Clear main argument
- Most support adequate
- Minor gaps that could be strengthened
- Some premises could use more justification

**2 points - Acceptable**:
- Argument identifiable but could be clearer
- Multiple gaps in reasoning
- Several premises need justification
- Logical flow interrupted

**1 point - Needs Major Revision**:
- Unclear argument
- Major logical gaps
- Many unsupported claims
- Disjointed reasoning

#### 2. Citation Quality (1-4 points)

**4 points - Excellent**:
- All claims properly cited
- Citations accurate and relevant
- Key literature well-integrated
- Citation density appropriate for section type
- Format consistent throughout

**3 points - Good**:
- Most claims cited
- Citations generally relevant
- Minor formatting inconsistencies
- Could integrate 1-2 more key sources

**2 points - Acceptable**:
- Some claims lack citations
- Several citations not optimally relevant
- Format inconsistencies present
- Missing some key literature

**1 point - Needs Major Revision**:
- Many uncited claims
- Citations poorly integrated
- Major format issues
- Key literature missing

#### 3. Clarity & Readability (1-4 points)

**4 points - Excellent**:
- Prose clear and precise
- Technical terms defined when introduced
- Sentence structure varied and effective
- Transitions smooth between ideas
- No ambiguity in meaning

**3 points - Good**:
- Generally clear prose
- Most terms adequately explained
- Occasional awkward phrasing
- Mostly good transitions

**2 points - Acceptable**:
- Some unclear passages
- Several terms need better explanation
- Multiple awkward sentences
- Transitions need improvement

**1 point - Needs Major Revision**:
- Frequently unclear
- Many unexplained terms
- Poor sentence structure
- Weak or missing transitions

#### 4. Structure & Flow (1-4 points)

**4 points - Excellent**:
- Perfect logical progression
- Each paragraph serves clear purpose
- Subsections well-organized
- Chapter fits outline specification exactly
- Word count within ±5% of target

**3 points - Good**:
- Good overall flow
- Most paragraphs purposeful
- Organization generally clear
- Minor deviations from outline
- Word count within ±10%

**2 points - Acceptable**:
- Flow interrupted in places
- Some paragraphs unfocused
- Organization could be improved
- Notable deviations from outline
- Word count off by 11-20%

**1 point - Needs Major Revision**:
- Poor flow
- Many unfocused paragraphs
- Disorganized
- Major deviations from outline
- Word count off by >20%

#### 5. Platform Style Conformity (1-4 points)

**4 points - Excellent**:
- Perfect match to platform writing style
- Voice consistent with sample papers
- Terminology appropriate
- Format conventions followed exactly
- Citation style matches platform

**3 points - Good**:
- Good style match
- Minor voice inconsistencies
- Terminology mostly appropriate
- Format mostly correct

**2 points - Acceptable**:
- Recognizable platform style but inconsistent
- Several voice/terminology issues
- Format needs adjustment in places

**1 point - Needs Major Revision**:
- Poor style match
- Wrong voice or terminology
- Format significantly different from platform norms

### Chapter Quality Gate

**Passing Threshold**: ≥16/20 (80%)

**If chapter scores <16/20**:
- Identify specific dimension(s) scoring <3
- Implement targeted revisions
- Re-evaluate before proceeding to next chapter

**Why This Matters**: Each chapter builds on previous ones. Low-quality chapters create cascading problems that are harder to fix later.

---

## Section-Specific Quality Standards

### Abstract Quality (250-300 words)

**Required Elements**:
- ✓ Problem/puzzle statement (1-2 sentences)
- ✓ Existing approach limitations (1-2 sentences)
- ✓ This paper's contribution (2-3 sentences)
- ✓ Main argument/findings (2-3 sentences)
- ✓ Significance/implications (1-2 sentences)

**Quality Checklist**:
- [ ] Can be understood without reading paper
- [ ] No citations in abstract (platform-dependent)
- [ ] Avoids jargon or defines essential terms
- [ ] Accurately represents paper content
- [ ] Compelling to target audience

### Introduction Quality (typically 15-20% of paper)

**Required Elements**:
- ✓ Opening puzzle/problem (hooks reader)
- ✓ Background context (enough to understand problem)
- ✓ Literature review (what's been tried, what's missing)
- ✓ This paper's approach (clear statement)
- ✓ Contribution summary (what's new)
- ✓ Roadmap (chapter-by-chapter preview)

**Quality Checklist**:
- [ ] Problem significance clearly established
- [ ] Gap in literature explicitly identified
- [ ] Originality clearly articulated
- [ ] Roadmap matches actual chapter structure
- [ ] Appropriate citation density (15-25 citations typical for philosophy)

### Main Body Chapters (60-70% of paper)

**Quality Varies by Chapter Type**:

**Conceptual/Theoretical Chapters**:
- [ ] Key concepts clearly defined
- [ ] Distinctions drawn where needed
- [ ] Examples provided for abstract concepts
- [ ] Connections to literature explicit

**Argument Chapters**:
- [ ] Premises clearly stated
- [ ] Inference steps explicit
- [ ] Objections anticipated and addressed
- [ ] Conclusion follows logically

**Case Study/Analysis Chapters**:
- [ ] Case described in sufficient detail
- [ ] Analysis systematically applied
- [ ] Findings clearly presented
- [ ] Implications drawn

**Critical Review Chapters**:
- [ ] Target position accurately represented
- [ ] Criticism fair and well-supported
- [ ] Charitable interpretation maintained
- [ ] Alternative considered

### Conclusion Quality (10-15% of paper)

**Required Elements**:
- ✓ Thesis restatement (in light of arguments)
- ✓ Main findings summary
- ✓ Significance reiteration (why this matters)
- ✓ Limitations acknowledgment (honest assessment)
- ✓ Future work directions (2-3 concrete suggestions)

**Quality Checklist**:
- [ ] No new information introduced
- [ ] Addresses introduction promises
- [ ] Acknowledges limitations without undermining contribution
- [ ] Future work suggestions are specific and feasible
- [ ] Strong closing statement

---

## Final Quality Assessment

### 7-Dimension Evaluation (10 points each, 70 total)

Before submission, evaluate complete paper on 7 dimensions:

#### 1. Overall Argument Quality (1-10)

**9-10 - Excellent**:
- Thesis perfectly clear throughout
- All chapters contribute to central argument
- Premises fully justified
- No logical gaps
- Counter-arguments thoroughly addressed
- Conclusion strongly supported

**7-8 - Good**:
- Clear thesis
- Good chapter integration
- Minor logical gaps
- Most objections addressed

**5-6 - Acceptable**:
- Thesis identifiable but could be clearer
- Some chapter disconnects
- Several logical gaps
- Some objections unaddressed

**3-4 - Needs Revision**:
- Unclear thesis
- Poor chapter integration
- Major logical gaps

**1-2 - Major Revision Required**:
- No clear thesis
- Chapters poorly connected
- Pervasive logical problems

#### 2. Literature Integration (1-10)

**9-10 - Excellent**:
- 40-60 sources (typical for philosophy)
- All key literature covered
- Citations well-integrated
- Literature critically engaged
- Gap clearly positioned

**7-8 - Good**:
- 30-40 sources
- Most key works included
- Good integration
- Critical engagement present

**5-6 - Acceptable**:
- 20-30 sources
- Some key works missing
- Adequate integration
- Limited critical engagement

**3-4 - Needs Revision**:
- <20 sources
- Major gaps in literature
- Poor integration

**1-2 - Major Revision Required**:
- Insufficient sources
- Key literature ignored
- Citations merely decorative

#### 3. Clarity & Accessibility (1-10)

**9-10 - Excellent**:
- Consistently clear prose
- Complex ideas well-explained
- Appropriate for target audience
- No ambiguity
- Technical terms defined

**7-8 - Good**:
- Generally clear
- Most ideas accessible
- Minor unclear passages

**5-6 - Acceptable**:
- Clarity inconsistent
- Several unclear sections
- Some inaccessible passages

**3-4 - Needs Revision**:
- Frequently unclear
- Many inaccessible passages

**1-2 - Major Revision Required**:
- Pervasively unclear
- Inaccessible to target audience

#### 4. Originality & Contribution (1-10)

**9-10 - Excellent**:
- Major original contribution
- Clear advance over literature
- Significance well-established
- Multiple innovative elements

**7-8 - Good**:
- Clear original contribution
- Solid advance over literature
- Significance demonstrated

**5-6 - Acceptable**:
- Identifiable contribution
- Incremental advance
- Significance could be stronger

**3-4 - Needs Revision**:
- Unclear contribution
- Minimal advance

**1-2 - Major Revision Required**:
- No clear contribution
- Replicates existing work

#### 5. Methodological Rigor (1-10)

**9-10 - Excellent**:
- Method explicitly stated and justified
- Consistently applied
- Appropriate for research question
- Limitations acknowledged
- Alternative methods considered

**7-8 - Good**:
- Method clear and appropriate
- Generally consistent application
- Limitations noted

**5-6 - Acceptable**:
- Method identifiable
- Some inconsistency
- Limitations minimally addressed

**3-4 - Needs Revision**:
- Method unclear
- Inconsistent application

**1-2 - Major Revision Required**:
- No clear method
- Inappropriate approach

#### 6. Structure & Organization (1-10)

**9-10 - Excellent**:
- Perfect logical flow
- Optimal chapter organization
- Proportions balanced
- Transitions seamless
- Roadmap followed exactly

**7-8 - Good**:
- Good flow
- Sensible organization
- Proportions generally balanced
- Good transitions

**5-6 - Acceptable**:
- Flow adequate
- Organization acceptable
- Some proportion issues
- Transitions need work

**3-4 - Needs Revision**:
- Poor flow
- Questionable organization
- Imbalanced proportions

**1-2 - Major Revision Required**:
- No clear flow
- Disorganized
- Severely imbalanced

#### 7. Platform & Style Conformity (1-10)

**9-10 - Excellent**:
- Perfect platform style match
- Format exactly correct
- Voice consistent throughout
- Citation format perfect
- Length optimal

**7-8 - Good**:
- Good style match
- Format mostly correct
- Voice generally consistent
- Minor format issues

**5-6 - Acceptable**:
- Recognizable platform style
- Format needs adjustment
- Voice inconsistencies

**3-4 - Needs Revision**:
- Poor style match
- Format problems

**1-2 - Major Revision Required**:
- Wrong platform style
- Format significantly incorrect

### Final Quality Gate

**Passing Threshold**: ≥56/70 (80%)

**Score Interpretation**:
- 63-70 (90-100%): Excellent, ready for submission
- 56-62 (80-89%): Good, minor revisions recommended
- 49-55 (70-79%): Acceptable, moderate revisions needed
- <49 (<70%): Major revisions required

---

## Content Completeness Checklist

Before final submission, verify all required elements present:

### Structural Completeness
- [ ] Abstract (250-300 words)
- [ ] Introduction with all required elements
- [ ] All outlined main chapters present
- [ ] Conclusion with all required elements
- [ ] References section formatted correctly

### Content Completeness
- [ ] All promises from introduction fulfilled
- [ ] All claims supported by evidence or argument
- [ ] All technical terms defined
- [ ] All objections addressed
- [ ] All limitations acknowledged

### Citation Completeness
- [ ] Every citation in text has bibliography entry
- [ ] Every bibliography entry is cited in text
- [ ] Citation format consistent throughout
- [ ] All citations include necessary information (author, year, page if direct quote)

### Format Completeness
- [ ] Title page (if required by platform)
- [ ] Section numbering consistent
- [ ] Heading hierarchy logical
- [ ] Figure/table captions (if applicable)
- [ ] Appendices (if needed)

### Submission Checklist (Platform-Specific)

**PhilArchive/PhilPapers**:
- [ ] PDF format
- [ ] Abstract <500 words
- [ ] Proper metadata (title, keywords, AMS classification)
- [ ] Author information complete

**arXiv**:
- [ ] LaTeX or PDF format
- [ ] Abstract <1920 characters
- [ ] Proper category selection (cs.AI, q-bio.NC, etc.)
- [ ] No embedded fonts issues

**PhilSci-Archive**:
- [ ] PDF format
- [ ] Proper subject classification
- [ ] Keywords provided
- [ ] No copywritten material without permission

---

## Common Quality Issues and Fixes

### Issue 1: Argument Gaps

**Symptom**: Chapter scores low on "Argument Quality"
**Diagnosis**: Logical leaps, unsupported premises, or missing steps
**Fix**:
1. Identify specific gap (which premise or inference?)
2. Add explicit justification for that step
3. Consider if additional sub-argument needed
4. Re-evaluate argument flow

### Issue 2: Insufficient Citations

**Symptom**: Chapter scores low on "Citation Quality"
**Diagnosis**: Claims without support, missing key literature
**Fix**:
1. Review each paragraph - which claims need citations?
2. Search for supporting literature for uncited claims
3. Check if key works from literature review are actually cited
4. Aim for 10-15 citations per 1000 words (adjust by field)

### Issue 3: Unclear Prose

**Symptom**: Chapter scores low on "Clarity & Readability"
**Diagnosis**: Complex sentences, undefined terms, weak transitions
**Fix**:
1. Break complex sentences into simpler ones
2. Add definitions for technical terms at first use
3. Add transition sentences between paragraphs
4. Read aloud to identify awkward phrasing

### Issue 4: Structural Problems

**Symptom**: Chapter scores low on "Structure & Flow"
**Diagnosis**: Poor organization, wrong proportions, deviates from outline
**Fix**:
1. Create reverse outline (what does each paragraph actually do?)
2. Reorganize paragraphs for better flow
3. Cut or expand sections to match target proportions
4. Ensure chapter follows outline specification

### Issue 5: Style Mismatch

**Symptom**: Chapter scores low on "Platform Style Conformity"
**Diagnosis**: Wrong voice, inappropriate terminology, format issues
**Fix**:
1. Review platform writing standards guide
2. Check sample papers for voice and terminology
3. Adjust sentence structure to match platform norms
4. Verify citation format matches platform requirements

---

## Quality Improvement Strategies

### Strategy 1: Iterative Refinement

For chapters scoring 14-15/20:
- Identify the single lowest-scoring dimension
- Focus revision effort on that dimension only
- Re-evaluate
- If still <16/20, address next-lowest dimension

### Strategy 2: Peer Review Simulation

After writing each chapter:
1. Read as if you're a skeptical reviewer
2. List every question or objection that arises
3. Address each in revision
4. Re-evaluate

### Strategy 3: Cross-Chapter Coherence

After completing all main chapters:
1. Create concept map across chapters
2. Verify terminology consistent throughout
3. Check that chapter N builds on chapter N-1
4. Ensure conclusion addresses introduction promises

### Strategy 4: Platform Benchmarking

Before final evaluation:
1. Re-read 2-3 sample papers from target platform
2. Note their structural and stylistic patterns
3. Compare your paper to these patterns
4. Adjust to match where needed

---

## Summary

**Chapter-Level Quality**:
- 5 dimensions, 4 points each (20 total)
- Passing threshold: ≥16/20 (80%)
- Evaluate after each chapter before proceeding

**Final Quality**:
- 7 dimensions, 10 points each (70 total)
- Passing threshold: ≥56/70 (80%)
- Evaluate complete paper before submission

**Iterative Improvement**:
- Low-scoring chapters must be revised before proceeding
- Final paper must meet threshold before submission
- Use targeted revision strategies for specific issues

This ensures systematic quality control throughout the writing process.
