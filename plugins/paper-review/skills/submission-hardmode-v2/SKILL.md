---
name: submission-hardmode-v2
description: Verification-centric paper hardening pipeline for journal submission. Multi-agent orchestration system that transforms experimental results into high-acceptance-probability manuscripts through hostile review simulation, fatal risk mitigation, and evidence-based claim validation. Use when users need to: (1) maximize acceptance probability for a specific journal, (2) align paper with journal norms and expectations, (3) identify and fix fatal methodological gaps before submission, (4) validate novelty against related work, or (5) ensure all claims have statistical backing. Triggered by phrases like 'harden paper for submission,' 'prepare for [journal name],' 'maximize acceptance probability,' or 'run submission hardmode.' Requires target journal, example papers, and experimental results as input; outputs submission-ready manuscript with acceptance probability estimate.
---

# SUBMISSION HARDMODE v2

## Overview

**NOT a writing tool. A verification system.**

This skill orchestrates specialized agents to structurally increase journal acceptance probability through:
- **Hostile reviewer simulation** (detect fatal flaws before submission)
- **Evidence-based claim validation** (block overclaiming)
- **Scope alignment verification** (prevent desk rejection)
- **Novelty differentiation analysis** (avoid incremental contribution trap)
- **Statistical rigor enforcement** (match journal standards)

**Input**: Target journal + Example papers + Experimental results

**Output**: Hardened manuscript + Acceptance probability estimate + Required revisions

---

## When to Use This Skill

Use **submission-hardmode-v2** when you need to:

**Pre-Submission Hardening**:
- Maximize acceptance probability for a specific journal
- Identify and fix fatal methodological gaps
- Align paper framing with journal norms
- Validate all claims have statistical backing

**Risk Assessment**:
- Simulate hostile reviewer feedback
- Evaluate novelty against related work
- Calculate desk rejection probability
- Identify incremental contribution risks

**Evidence Validation**:
- Map claims to experimental evidence
- Ensure statistical transparency
- Quantify effect sizes and power
- Check multiple comparison corrections

**Triggers**:
- "Harden this paper for [Journal Name]"
- "Maximize acceptance probability"
- "Run submission hardmode"
- "Prepare for hostile reviewers"
- "Validate claims against evidence"

---

## Required Inputs

### 1. Target Journal
```yaml
target_journal: "ACM TOCHI"
```

### 2. Experimental Results (structured data)
```yaml
experimental_results:
  study_1:
    participants: 48
    design: "2x2 within-subjects"
    dependent_vars: ["task_time", "error_rate", "satisfaction"]
    results:
      task_time: {effect: "F(1,47)=12.3, p<0.001, ηp²=0.21"}
      error_rate: {effect: "F(1,47)=5.6, p=0.022, ηp²=0.11"}
      satisfaction: {effect: "F(1,47)=18.9, p<0.001, ηp²=0.29"}
```

### 3. Optional Parameters
```yaml
journal_examples_folder: "./papers/tochi_2023_examples/"  # If not provided, auto-search
field: "Human-Computer Interaction"  # default: "HCI"
mode: "Conservative"                 # Conservative | Aggressive
statistical_strictness: "High"       # Low | Medium | High
```

**Note**: If `journal_examples_folder` not provided, the skill will automatically search for and download 3-5 recent papers from the target journal to `references/journal_papers/`.

---

## Global Rules (Hard Constraints)

| Rule | Enforcement |
|------|-------------|
| NO_OVERCLAIMING | All claims must map to explicit evidence |
| CLAIM_CLASSIFICATION | Label as [Supported \| Speculative] |
| METHODOLOGY_GATING | Block drafting if fatal flaws detected |
| JOURNAL_ALIGNMENT | Auto-correct framing mismatches |
| CLARITY_ENFORCEMENT | Clear, concise sentences only |
| INCREMENTAL_RISK_ASSESSMENT | Mandatory before drafting |
| STATISTICAL_TRANSPARENCY | Report effect sizes + p-values |
| LOGIC_FIRST | Design argument structure before writing |
| SCOPE_VERIFICATION | Validate Aim & Scope alignment |
| EVIDENCE_REQUIREMENTS | Claim without evidence = invalid |
| ABBREVIATION_CONSISTENCY | First use: full form + abbreviation, then abbreviation only (from Introduction) |
| TERMINOLOGY_CONSISTENCY | Once defined, always use the same term throughout |

---

## Pipeline Structure

```
PHASE -1: Reference Paper Collection (librarian, conditional)
    ↓
PHASE 0: Journal Profiling (librarian, parallel)
    ↓
PHASE 0.5: Scope Alignment Check (architect, GATE)
    ↓
PHASE 1: Contribution Lock (prometheus)
    ↓
PHASE 1.5: Novelty Differentiation (librarian, parallel)
    ↓
PHASE 2: Hostile Review Simulation (metis, BLOCKING)
    ↓
PHASE 3: Fatal Risk Mitigation (sisyphus + ulw, BLOCKING)
    ↓
PHASE 3.5: Narrative Architecture (architect)
    ↓
PHASE 4: Manuscript Drafting (hephaestus)
    ↓
PHASE 5: Final Stress Test (momus)
```

**CONDITIONAL**: Phase -1 (runs only if journal_examples_folder not provided)
**GATES**: Phase 0.5 (scope check), Phase 2 (fatal risks)
**BLOCKING**: Phase 3 (must fix before proceeding)

---

## Execution Protocol

### PHASE -1: Reference Paper Collection

**Agent**: `librarian` (blocking, conditional)

**Objective**: Collect 3-5 recent papers from target journal for analysis

**Trigger**: Only runs if `journal_examples_folder` NOT provided

**Delegation**:
```markdown
task(
  subagent_type="librarian",
  load_skills=[],
  run_in_background=false,
  prompt="""
  CONTEXT: User did not provide example papers from {target_journal}. Need to collect 3-5 recent accepted papers for profiling.
  
  GOAL: Find and collect 3-5 high-quality, recent papers from {target_journal} in {field}.
  
  DOWNSTREAM: These papers will be analyzed in PHASE 0 to extract journal norms.
  
  REQUEST:
  1. Search for recent papers (2022-2024) from {target_journal} in {field}
  2. Prioritize:
     - High citation count (quality indicator)
     - Methodologically diverse (different study designs)
     - Recent publication date (current norms)
     - Full text accessible (PDF or HTML)
  
  3. For each paper, collect:
     - Title
     - Authors
     - Year
     - DOI or URL
     - Abstract (for quick relevance check)
     - PDF link (if available)
  
  4. Save to: .claude/skills/submission-hardmode-v2/references/journal_papers/
     - Create folder if doesn't exist
     - Save as: {journal_abbrev}_{year}_{first_author}.pdf or .md (metadata)
  
  5. Return JSON:
     {
       "papers": [
         {
           "title": "...",
           "authors": "...",
           "year": 2023,
           "doi": "...",
           "pdf_link": "...",
           "saved_as": "tochi_2023_smith.pdf"
         }
       ],
       "total_found": 5,
       "search_query": "...",
       "notes": "..."
     }
  
  SKIP: Older than 2020, non-empirical papers (unless {field} is theoretical)
  
  If unable to download PDFs, save metadata only and note as limitation.
  """
)
```

**Fallback**: If librarian cannot find papers, ask user to:
1. Provide journal_examples_folder, OR
2. Manually add 3-5 papers to references/journal_papers/, OR
3. Proceed with limited profiling (RISKY - warn user)

**Outputs**: 
- Store papers in `references/journal_papers/`
- Create `references/paper_inventory.json` with metadata

---

### PHASE 0: Journal Profiling

**Agent**: `librarian` (background, parallel)

**Objective**: Extract acceptance patterns from example papers

**Input Source**:
- If `journal_examples_folder` provided → use that path
- Otherwise → use `references/journal_papers/` (from PHASE -1)

**Delegation**:
```markdown
task(
  subagent_type="librarian",
  load_skills=[],
  run_in_background=true,
  prompt="""
  CONTEXT: Preparing submission for {target_journal}. Need to understand journal norms for contribution framing, methodological rigor, and structural expectations.
  
  GOAL: Extract actionable patterns from example papers that will guide our paper's structure and claims.
  
  DOWNSTREAM: Results will determine:
  - How we frame contributions
  - What methodological rigor is expected
  - What structural norms to follow
  
  REQUEST:
  1. Analyze all papers in {paper_source}
     (paper_source = journal_examples_folder OR references/journal_papers/)
  2. Extract:
     - Contribution framing patterns (novelty vs utility emphasis)
     - Methodological rigor threshold (sample sizes, controls, statistical reporting)
     - Recurring rejection reasons (from author responses if available)
     - Structural characteristics (section organization, figure density)
     - Aim & Scope summary (verbatim + interpretation)
  
  3. Return structured JSON:
     {
       "contribution_framing": ["pattern1", "pattern2"],
       "rigor_threshold": "High|Medium|Low",
       "rejection_reasons": ["reason1", "reason2"],
       "structural_norms": {...},
       "aim_scope": "..."
     }
  
  SKIP: Individual paper summaries. Focus on aggregate patterns.
  """
)
```

**Outputs**: Store as `journal_profile.json`

---

### PHASE 0.5: Scope Alignment Check

**Agent**: `architect`

**Objective**: Prevent desk rejection via scope mismatch detection

**GATE CONDITION**: `alignment_score >= 0.7` OR user override

**Delegation**:
```markdown
task(
  subagent_type="architect",
  load_skills=[],
  run_in_background=false,
  prompt="""
  CONTEXT: Validating scope alignment before investing in full pipeline.
  
  GOAL: Calculate probability of desk rejection due to scope mismatch.
  
  DOWNSTREAM: If score < 0.7, HALT pipeline and present mismatch report to user.
  
  REQUEST:
  Compare:
  - Our experimental results: {experimental_results}
  - Journal Aim & Scope: {journal_profile.aim_scope}
  
  Calculate:
  1. alignment_score (0-1): How well our work fits journal scope
  2. mismatch_risks: List specific misalignment points
  3. desk_reject_probability (0-1): Estimated probability of immediate rejection
  
  Return JSON:
  {
    "alignment_score": 0.85,
    "mismatch_risks": ["minor point"],
    "desk_reject_probability": 0.15,
    "recommendation": "PROCEED|HALT"
  }
  """
)
```

**If alignment_score < 0.7**: Ask user "Scope mismatch detected. Desk rejection risk: {probability}. Override and proceed anyway?"

---

### PHASE 1: Contribution Lock

**Agent**: `prometheus` (not a built-in agent; map to high-tier executor or architect)

**Objective**: Lock 3-4 core contributions with evidence mapping

**Delegation**:
```markdown
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=false,
  prompt="""
  CONTEXT: Defining core contributions that will structure entire paper.
  
  GOAL: Create claim-evidence table where EVERY claim maps to experimental support.
  
  DOWNSTREAM: This table will be used by:
  - Hostile reviewer simulation (to find weak claims)
  - Narrative architecture (to structure arguments)
  - Manuscript drafting (to write results section)
  
  REQUEST:
  Given:
  - Experimental results: {experimental_results}
  - Journal framing norms: {journal_profile.contribution_framing}
  
  Generate:
  1. 3-4 core contributions (bullet points matching journal style)
  2. Theoretical positioning (1 paragraph)
  3. Claim-evidence table:
  
     | Claim | Supporting Result | Statistical Strength | Limitation |
     |-------|-------------------|---------------------|------------|
     | Our system reduces task time | study_1.task_time | F(1,47)=12.3, p<0.001, ηp²=0.21 (large effect) | Limited to expert users |
  
  VALIDATION:
  - Each contribution must reference ≥1 experimental result
  - Statistical strength must include effect size + significance
  - Limitations must be explicit per claim
  
  FLAG: Any claim without p<0.05 or effect size data as [UNSUPPORTED]
  """
)
```

**Outputs**: Store as `contributions.json`

---

### PHASE 1.5: Novelty Differentiation

**Agent**: `librarian` (background, parallel)

**Objective**: Differentiate from top-5 related works

**Delegation**:
```markdown
task(
  subagent_type="librarian",
  load_skills=[],
  run_in_background=true,
  prompt="""
  CONTEXT: Validating novelty claim before drafting. Need to avoid incremental contribution trap.
  
  GOAL: Quantify our novelty against closest related work.
  
  DOWNSTREAM: If incremental_risk > 0.7, HALT and warn user of high rejection risk.
  
  REQUEST:
  1. Search {field} for top-5 papers most similar to {contributions.core_contributions}
  2. Create differentiation matrix:
  
     | Paper | Their Contribution | Our Difference | Novelty Type |
     |-------|-------------------|----------------|--------------|
     | Smith 2023 | UI for single-user | Multi-user coordination | Domain |
  
     Novelty Types: [Methodological, Theoretical, Domain, Scale, Generalization]
  
  3. Calculate:
     - incremental_risk (0-1): 0=transformative, 1=marginal extension
     - novelty_strength (0-1): 0=weak differentiation, 1=clear gap filled
  
  4. If incremental_risk > 0.7, FLAG as HIGH RISK
  
  Return JSON with matrix + scores.
  """
)
```

**If incremental_risk > 0.7**: Warn user and ask to proceed or abort

---

### PHASE 2: Hostile Review Simulation

**Agent**: `metis` (not built-in; map to `architect` with hostile persona)

**Objective**: Simulate 3 hostile reviewers, extract top-3 Fatal risks

**BLOCKING**: Must identify Fatal risks before proceeding

**Delegation**:
```markdown
task(
  subagent_type="architect",
  load_skills=[],
  run_in_background=false,
  prompt="""
  CONTEXT: Simulating peer review BEFORE submission to catch fatal flaws.
  
  GOAL: Generate 10 strongest rejection arguments from hostile reviewers.
  
  DOWNSTREAM: Top-3 Fatal risks will be mitigated in PHASE 3. Major/Minor risks will be noted for revisions.
  
  REQUEST:
  You are 3 reviewers for {target_journal} with {journal_profile.rigor_threshold} standards.
  Mode: {mode}
  
  Review:
  - Contributions: {contributions.core_contributions}
  - Evidence: {contributions.claim_evidence_table}
  
  Generate:
  1. 10 strongest rejection arguments (be brutally honest)
  2. Rate severity: [Fatal | Major | Minor]
     - Fatal = desk reject or require major new experiments
     - Major = accept with revisions likely
     - Minor = accept with minor revisions
  
  3. Return top-3 Fatal risks with remediation requirements:
  
     {
       "fatal_risks": [
         {
           "critique": "No power analysis reported",
           "severity": "Fatal",
           "remediation": "Conduct post-hoc power analysis"
         }
       ]
     }
  """
)
```

**If no Fatal risks**: Skip PHASE 3, proceed to PHASE 3.5

---

### PHASE 3: Fatal Risk Mitigation

**Agent**: `sisyphus` (self, with ulw mode enabled)

**Objective**: Fix ONLY Fatal risks via minimal additions

**BLOCKING**: Must complete before drafting manuscript

**Execution Mode**: ULW enabled (parallel agents for independent risks)

**Protocol**:
```markdown
For EACH fatal risk:
1. Design minimal experiment/analysis to address it
2. Execute (or simulate if data unavailable)
3. Generate statistical report:
   - Effect size (Cohen's d / η² / Cramér's V)
   - Power analysis (post-hoc)
   - Multiple comparison corrections (Bonferroni/Holm if applicable)
4. Update claim-evidence table

HALT if experiment cannot address Fatal risk (report to user).
```

**Delegation** (per risk):
```markdown
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=true,  # parallel for independent risks
  prompt="""
  CONTEXT: Addressing Fatal risk: {risk.critique}
  
  GOAL: Design and execute minimal fix. Update claim-evidence table.
  
  DOWNSTREAM: Updated evidence will be used in manuscript drafting.
  
  REQUEST:
  1. Design experiment/analysis:
     - What data is needed
     - What analysis addresses the critique
     - Minimal scope (don't add unnecessary work)
  
  2. Execute (simulate if needed)
  
  3. Generate statistical report:
     - Effect size with interpretation
     - Power analysis (post-hoc)
     - Multiple comparison corrections (if applicable)
  
  4. Update claim-evidence table with new supporting data
  
  Strictness: {statistical_strictness}
  
  HALT if fix is impossible with current data.
  """
)
```

**Outputs**: Store as `updated_contributions.json`

---

### PHASE 3.5: Narrative Architecture

**Agent**: `architect`

**Objective**: Design paper-level argument structure BEFORE writing

**Delegation**:
```markdown
task(
  subagent_type="architect",
  load_skills=[],
  run_in_background=false,
  prompt="""
  CONTEXT: Designing logical flow before drafting to avoid incoherent narrative.
  
  GOAL: Create argument DAG and figure sequence.
  
  DOWNSTREAM: This structure will guide manuscript drafting in PHASE 4.
  
  REQUEST:
  Given:
  - Claims: {updated_contributions.claim_evidence_table}
  - Journal structure: {journal_profile.structural_norms}
  
  Design:
  1. Argument DAG:
     - Top-level claim (main contribution)
       ├─ Sub-claim 1 (from table)
       │  ├─ Evidence node (study_1.task_time)
       │  └─ Evidence node (study_1.error_rate)
       └─ Sub-claim 2
          └─ Evidence node
  
  2. Figure sequence:
     - Figure 1: System overview
     - Figure 2: Study design
     - Figure 3: Results (task_time)
     - Figure 4: Results (error_rate + satisfaction)
  
  3. Claim-figure mapping:
     - Sub-claim 1 → Figure 3, 4
     - Sub-claim 2 → Figure 5
  
  4. Section-level logic flow diagram
  
  ENSURE:
  - No orphan claims (all connected to evidence)
  - Figures appear before referenced in text
  - Logical progression: problem → solution → validation
  """
)
```

**Outputs**: Store as `narrative_architecture.json`

---

### PHASE 4: Manuscript Drafting

**Agent**: `hephaestus` (map to high-tier executor or writer with domain knowledge)

**Objective**: Draft manuscript sections following narrative architecture

**Delegation**:
```markdown
task(
  category="writing",
  load_skills=["academic-paper-composer"],  # leverage existing skill
  run_in_background=false,
  prompt="""
  CONTEXT: Drafting manuscript with validated claims and designed narrative structure.
  
  GOAL: Generate submission-ready sections matching journal norms.
  
  DOWNSTREAM: Manuscript will undergo final stress test (PHASE 5).
  
  REQUEST:
  Write complete manuscript sections:
  
  1. ABSTRACT (250 words max):
     - Problem statement (1 sentence)
     - Gap (1 sentence)
     - Approach (2 sentences)
     - Key results (2 sentences)
     - Contribution (1 sentence)
  
  2. INTRODUCTION:
     - Follow structure: Problem → Gap → Approach → Contribution
     - Cite related work in context (use {novelty.related_papers})
     - End with paper organization
  
  3. METHODS:
     - Rigor emphasis per {journal_profile.rigor_threshold}
     - Justify sample sizes
     - Detail statistical procedures
  
  4. RESULTS:
     - Organize by claim from {updated_contributions.claim_evidence_table}
     - Lead with strongest results
     - Report effect sizes + significance
     - Reference figures per {narrative_architecture.claim_figure_mapping}
  
  5. DISCUSSION:
     - Theoretical implications
     - Design implications
     - Limitations (explicit and upfront)
     - Future work (brief)
  
   WRITING RULES:
   - Active voice where possible
   - No hedging for [Supported] claims
   - Explicit hedging for [Speculative] claims
   - Clear topic sentences per paragraph
   - Max 25 words per sentence (average)
   
   ABBREVIATION RULES:
   - Abstract: Use full forms only (no abbreviations)
   - Introduction onwards: First mention = "Full Form (Abbreviation)", then "Abbreviation" only
   - Track all abbreviations in a glossary for consistency checking
   - Examples:
     * CORRECT: "Machine Learning (ML)" in Introduction first, then "ML" throughout
     * WRONG: "ML" in Abstract
     * WRONG: "ML" used before "Machine Learning (ML)" definition
   - Create abbreviation glossary as you write
   
   TERMINOLOGY CONSISTENCY:
   - Choose ONE term per concept and use it consistently throughout ALL sections
   - Examples:
     * CORRECT: Always use "haptic feedback" throughout paper
     * WRONG: Switching between "haptic feedback", "tactile response", "touch sensation" for same concept
     * CORRECT: Always use "participants" OR always use "users", not both
     * WRONG: "participants" in Methods, "users" in Results for same group
   - Create term registry: {concept → chosen_term}
   - If using multiple related but distinct concepts, explicitly differentiate them early
   - Maintain term registry as JSON:
     {
       "user_group": "participants",  // NOT "users", "subjects", "volunteers"
       "haptic_modality": "haptic feedback",  // NOT "tactile response", "touch sensation"
       "input_device": "controller"  // NOT "device", "input system"
     }
   
   Use all context: {journal_profile}, {updated_contributions}, {narrative_architecture}
  """
)
```

**Outputs**: 
- Store manuscript as `manuscript_draft.md`
- Store abbreviation glossary as `abbreviation_glossary.json`:
  ```json
  {
    "abbreviations": [
      {"full": "Machine Learning", "abbrev": "ML", "first_use_section": "Introduction", "first_use_location": "paragraph 2"}
    ]
  }
  ```
- Store term registry as `term_registry.json`:
  ```json
  {
    "concepts": {
      "user_group": "participants",
      "haptic_modality": "haptic feedback",
      "input_device": "controller"
    }
  }
  ```

---

### PHASE 5: Final Stress Test

**Agent**: `momus` (map to `architect` with harshest critic persona)

**Objective**: Final adversarial review + acceptance probability estimate

**Delegation**:
```markdown
task(
  subagent_type="architect",
  load_skills=[],
  run_in_background=false,
  prompt="""
  CONTEXT: Final verification before user submits to journal.
  
  GOAL: Provide acceptance probability estimate and must-fix items.
  
  DOWNSTREAM: User will decide whether to submit or revise further.
  
  REQUEST:
  Review complete manuscript as HARSHEST POSSIBLE REVIEWER:
  
  Provide:
  1. Single most convincing rejection argument
  2. Desk reject probability (0-1) with justification
  3. Acceptance probability (0-1) with justification:
     - Consider: scope alignment, novelty, rigor, clarity
     - Be brutally honest
  4. Required revisions (list with priority: [Fatal | Major | Minor])
  
   Be brutal. Identify:
   - Scope misalignment (even if passed PHASE 0.5)
   - Weak evidence chains
   - Overclaiming
   - Methodological gaps
   - Incremental contribution risk
   
   ABBREVIATION & TERMINOLOGY CHECKS:
   - Verify Abstract contains NO abbreviations
   - Verify all abbreviations introduced properly: "Full Form (Abbreviation)" on first use
   - Check no abbreviation used before definition
   - Identify terminology inconsistencies (same concept, different terms)
   - Flag synonym usage that breaks consistency
   - Examples of violations:
     * "ML" used in Abstract
     * "Machine Learning" appears after "ML" was already used
     * Switching between "user interface", "UI", and "interface" for same concept
   
   Return JSON:
   {
     "strongest_rejection": "...",
     "desk_reject_prob": 0.1,
     "acceptance_prob": 0.72,
     "confidence_rationale": "...",
     "required_revisions": [
       {"item": "...", "priority": "Minor"}
     ],
     "abbreviation_consistency": {
       "abstract_violations": ["ML used in abstract"],
       "definition_violations": ["ML used before definition"],
       "all_abbreviations": [
         {"term": "Machine Learning", "abbrev": "ML", "first_use": "Introduction, line 3"}
       ]
     },
     "terminology_consistency": {
       "inconsistencies": [
         {"concept": "user_interface", "terms_used": ["user interface", "UI", "interface"], "locations": ["Methods p.5", "Results p.8", "Discussion p.12"]}
       ],
       "recommendation": "Standardize to 'user interface' throughout"
     }
   }
  """
)
```

**Outputs**: Store as `final_assessment.json`

---

## Failsafe Rules (Automatic Halting)

| Trigger | Halt Behavior |
|---------|---------------|
| **Scope Mismatch** | If PHASE 0.5 `alignment_score < 0.7` AND user declines override → HALT, output scope report |
| **Fatal Methodology** | If PHASE 2 finds Fatal risk that PHASE 3 cannot fix → HALT before drafting, output gap description + required experiments |
| **Weak Novelty** | If PHASE 1.5 `incremental_risk > 0.7` → WARN user, require explicit proceed confirmation |
| **Missing Evidence** | If any claim lacks statistical backing (p-value or effect size) → BLOCK PHASE 4, request clarification |
| **Incomplete Statistical Report** | If PHASE 3 output missing effect sizes, power, or corrections → BLOCK PHASE 4 |

---

## Output Deliverables

Upon successful completion:

```
.claude/skills/submission-hardmode-v2/
├── references/
│   ├── journal_papers/               # PHASE -1 (if auto-collected)
│   │   ├── tochi_2023_smith.pdf
│   │   ├── tochi_2023_jones.pdf
│   │   └── ...
│   └── paper_inventory.json          # Metadata of collected papers
├── outputs/
│   ├── journal_profile.json          # PHASE 0
│   ├── scope_alignment.json          # PHASE 0.5
│   ├── contributions.json            # PHASE 1
│   ├── novelty_differentiation.json  # PHASE 1.5
│   ├── hostile_review.json           # PHASE 2
│   ├── updated_contributions.json    # PHASE 3
│   ├── narrative_architecture.json   # PHASE 3.5
│   ├── manuscript_draft.md           # PHASE 4
│   ├── abbreviation_glossary.json    # PHASE 4
│   ├── term_registry.json            # PHASE 4
│   ├── final_assessment.json         # PHASE 5
│   └── SUBMISSION_REPORT.md          # Summary
```

**SUBMISSION_REPORT.md** contains:
- Acceptance probability estimate
- Required revisions (prioritized)
- Scope alignment score
- Novelty risk assessment
- Statistical rigor validation
- Abbreviation consistency report
- Terminology consistency report
- Ready for submission: YES/NO

---

## Usage Example

### Invocation (with examples provided)
```
RUN SUBMISSION_HARDMODE

TARGET_JOURNAL: ACM TOCHI
JOURNAL_EXAMPLES: ./papers/tochi_2023_examples/
EXPERIMENTAL_RESULTS: <paste structured data>
FIELD: Human-Computer Interaction
MODE: Conservative
STATISTICAL_STRICTNESS: High
```

### Invocation (auto-search for examples)
```
RUN SUBMISSION_HARDMODE

TARGET_JOURNAL: ACM CHI
# JOURNAL_EXAMPLES not provided - will auto-search
EXPERIMENTAL_RESULTS: <paste structured data>
FIELD: Human-Computer Interaction
MODE: Conservative
STATISTICAL_STRICTNESS: High
```

### Expected Output (with auto-search)
```
✓ PHASE -1: Reference papers collected (5 papers from ACM CHI 2023-2024)
           → Saved to references/journal_papers/
✓ PHASE 0: Journal profiled (rigor_threshold: High)
✓ PHASE 0.5: Scope alignment: 0.85 (PASS)
✓ PHASE 1: 4 core contributions locked
✓ PHASE 1.5: Novelty risk: 0.3 (LOW)
✓ PHASE 2: 2 Fatal risks identified
✓ PHASE 3: Fatal risks mitigated (power analysis added)
✓ PHASE 3.5: Narrative architecture complete
✓ PHASE 4: Manuscript drafted (6,800 words)
✓ PHASE 5: Final assessment complete

ACCEPTANCE PROBABILITY: 0.72
REQUIRED REVISIONS: 3 Minor items

READY FOR SUBMISSION: YES
```

### Expected Output (with provided examples)
```
✓ PHASE 0: Journal profiled from ./papers/tochi_2023_examples/ (rigor_threshold: High)
✓ PHASE 0.5: Scope alignment: 0.85 (PASS)
✓ PHASE 1: 4 core contributions locked
✓ PHASE 1.5: Novelty risk: 0.3 (LOW)
✓ PHASE 2: 2 Fatal risks identified
✓ PHASE 3: Fatal risks mitigated (power analysis added)
✓ PHASE 3.5: Narrative architecture complete
✓ PHASE 4: Manuscript drafted (6,800 words)
✓ PHASE 5: Final assessment complete

ACCEPTANCE PROBABILITY: 0.72
REQUIRED REVISIONS: 3 Minor items

READY FOR SUBMISSION: YES
```

---

## Notes

- **This is NOT a drafting tool**. It's a verification system that drafts as a byproduct.
- **Expect halts**. Failsafes are intentional to prevent wasted work on unsubmittable papers.
- **Evidence is king**. Claims without statistical backing will be blocked.
- **Conservative by default**. Set `mode: Aggressive` only if you're confident in your novelty.
- **Reusable outputs**. All JSON outputs can be used for revision cycles.
- **Terminology matters**. Inconsistent terminology can signal lack of rigor. The system enforces:
  - Abbreviations properly introduced (full form first, then abbreviation)
  - Consistent term usage throughout (no synonym switching)
  - Abstract remains abbreviation-free for maximum clarity

---

## Maintenance

**Version**: 2.0  
**Last Updated**: 2026-02-11  
**Dependencies**: librarian, architect, academic-paper-composer (optional)

**Changelog**:
- v2.0: Initial release with 6-phase pipeline + failsafes
