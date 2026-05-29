# SUBMISSION HARDMODE v2

## 📁 Folder Structure

```
submission-hardmode-v2/
├── SKILL.md              # Executable skill definition (main file)
├── DESIGN_SPEC.yaml      # Technical specification document
├── README.md             # This file
├── references/           # Reference materials (example papers, etc.)
└── outputs/              # Generated during execution (auto-created)
```

## 🎯 Quick Start

### Prerequisites

1. **Required**: Target journal name (e.g., "ACM TOCHI")
2. **Required**: Your experimental results (structured format)
3. **Optional**: Folder with 3-5 accepted papers from that journal
   - If not provided, skill will auto-search and download to `references/journal_papers/`

### Basic Usage (with examples)

```markdown
RUN SUBMISSION_HARDMODE

TARGET_JOURNAL: ACM TOCHI
JOURNAL_EXAMPLES: ./papers/tochi_examples/
EXPERIMENTAL_RESULTS: {
  study_1: {
    participants: 48,
    design: "2x2 within-subjects",
    results: {
      task_time: {effect: "F(1,47)=12.3, p<0.001, ηp²=0.21"}
    }
  }
}
```

### Basic Usage (auto-search)

```markdown
RUN SUBMISSION_HARDMODE

TARGET_JOURNAL: ACM CHI
# No JOURNAL_EXAMPLES - will auto-search and download
EXPERIMENTAL_RESULTS: {
  study_1: {
    participants: 48,
    design: "2x2 within-subjects",
    results: {
      task_time: {effect: "F(1,47)=12.3, p<0.001, ηp²=0.21"}
    }
  }
}
```

## 📋 What This Skill Does

**NOT a writing assistant. A verification system.**

This skill orchestrates multiple agents to:

1. **Collect reference papers** (auto-search if not provided)
2. **Profile your target journal** (acceptance patterns, rigor expectations)
3. **Check scope alignment** (prevent desk rejection)
4. **Lock contributions with evidence** (map claims to data)
5. **Validate novelty** (avoid incremental contribution trap)
6. **Simulate hostile reviewers** (find fatal flaws BEFORE submission)
7. **Mitigate risks** (fix only critical issues)
8. **Design narrative architecture** (logical argument flow)
9. **Draft manuscript** (with validated claims)
10. **Final stress test** (acceptance probability estimate)

## 🚨 Key Features

### Automatic Halting (Failsafes)

The skill will STOP if:
- Scope mismatch detected (alignment < 0.7)
- Fatal methodological gap cannot be fixed
- Claims lack statistical backing
- Novelty risk too high (incremental > 0.7)

**This prevents wasted work on unsubmittable papers.**

### Evidence-Based Writing

Every claim must:
- Map to experimental data
- Have statistical backing (effect size + p-value)
- Include explicit limitations
- Be labeled as [Supported] or [Speculative]

### Hostile Review Simulation

Simulates 3 harsh reviewers who:
- Find the strongest rejection arguments
- Rate severity (Fatal / Major / Minor)
- Provide remediation requirements

## 📊 Expected Outputs

After completion, you'll get:

```
.claude/skills/submission-hardmode-v2/
├── references/
│   ├── journal_papers/            # Auto-collected papers (if applicable)
│   │   ├── chi_2023_smith.pdf
│   │   └── ...
│   └── paper_inventory.json       # Metadata
├── outputs/
│   ├── journal_profile.json       # Journal acceptance patterns
│   ├── scope_alignment.json       # Desk rejection risk
│   ├── contributions.json         # Claim-evidence table
│   ├── novelty_differentiation.json # Comparison with related work
│   ├── hostile_review.json        # Simulated reviewer feedback
│   ├── updated_contributions.json # After risk mitigation
│   ├── narrative_architecture.json # Argument flow design
│   ├── manuscript_draft.md        # Actual paper
│   ├── final_assessment.json      # Acceptance probability
│   └── SUBMISSION_REPORT.md       # Executive summary
```

## 🎛️ Configuration Options

### Mode
- `Conservative` (default): Strict validation, higher bar
- `Aggressive`: Faster, accepts moderate risks

### Statistical Strictness
- `High` (default): Requires effect sizes, power analysis, corrections
- `Medium`: Effect sizes + significance required
- `Low`: P-values sufficient

### Field
- `HCI` (default): Human-Computer Interaction
- `AI`: Artificial Intelligence
- `Cognitive Science`, etc.

## 📖 Documentation

- **SKILL.md**: Executable skill with detailed phase protocols
- **DESIGN_SPEC.yaml**: Technical specification (YAML format)
- **README.md**: This overview document

## 🔄 Typical Workflow

### First Run (Finding Gaps)
```
RUN SUBMISSION_HARDMODE
→ HALT at PHASE 2: "Fatal risk: No power analysis"
→ Fix: Conduct power analysis
→ Update experimental_results
```

### Second Run (Hardened Paper)
```
RUN SUBMISSION_HARDMODE
→ All phases pass
→ Acceptance probability: 0.72
→ 3 minor revisions required
→ READY FOR SUBMISSION: YES
```

## ⚠️ Important Notes

1. **Expect halts on first run**. The skill is designed to catch gaps EARLY.
2. **Provide structured data**. Experimental results must include effect sizes and p-values.
3. **Journal examples matter**. Quality of profiling depends on example papers.
4. **Evidence is mandatory**. Claims without backing will be blocked.
5. **Outputs are reusable**. JSON files can be used for revision cycles.

## 🛠️ Troubleshooting

### "Scope mismatch detected"
→ Your work may not fit the journal. Review Aim & Scope carefully.

### "Fatal risk: [X]"
→ Critical methodological gap. Must fix before proceeding.

### "Incremental risk > 0.7"
→ Your novelty may be too weak. Consider different framing or stronger contribution.

### "Claim lacks statistical backing"
→ Add effect sizes and p-values to experimental_results.

## 📦 Integration with Other Skills

This skill can leverage:
- `academic-paper-composer`: For manuscript drafting (PHASE 4)
- `notion-rag`: For literature review (PHASE 1.5)
- `academic-paper-strategist`: For pre-planning (optional)

## 📝 Example: Complete Invocation

```markdown
RUN SUBMISSION_HARDMODE

TARGET_JOURNAL: ACM TOCHI
JOURNAL_EXAMPLES: ./papers/tochi_2023_examples/
FIELD: Human-Computer Interaction
MODE: Conservative
STATISTICAL_STRICTNESS: High

EXPERIMENTAL_RESULTS:
  study_1:
    participants: 48
    design: "2x2 within-subjects"
    dependent_vars: ["task_time", "error_rate", "satisfaction"]
    results:
      task_time:
        effect: "F(1,47)=12.3, p<0.001, ηp²=0.21"
        mean_control: 45.2
        mean_treatment: 38.6
      error_rate:
        effect: "F(1,47)=5.6, p=0.022, ηp²=0.11"
        mean_control: 12.3
        mean_treatment: 9.8
      satisfaction:
        effect: "F(1,47)=18.9, p<0.001, ηp²=0.29"
        likert_control: 4.2
        likert_treatment: 5.8
```

## 🔮 Future Enhancements

Potential v3.0 features:
- Multi-journal optimization (target 2-3 journals simultaneously)
- Automatic figure generation from results
- Citation network analysis
- Reviewer persona customization

---

**Version**: 2.0  
**Created**: 2026-02-11  
**Status**: Ready for use  
**Dependencies**: librarian, architect, academic-paper-composer (optional)
