---
id: "skill-m5h7k2-f7g8"
name: academic-paper-basics
description: "Fundamental rules for academic paper writing that must ALWAYS be enforced - abbreviations, flow, terminology, references, tone, capitalization, vague pronouns, number consistency. These are non-negotiable basics."
source: "extracted"
createdAt: "2026-04-03T20:00:00Z"
triggers:
  - "paper writing"
  - "academic writing"
  - "논문 작성"
  - "논문 기본"
  - "paper basics"
  - "writing rules"
  - "약어"
  - "abbreviation"
tags:
  - "academic-writing"
  - "fundamental"
  - "always-apply"
quality: 98
usageCount: 2
---

# Problem

Academic papers repeatedly fail basic quality checks. These rules must be enforced on EVERY paper, EVERY time, without exception. The same mistakes keep recurring: vague pronouns, inconsistent number style, informal expressions, unnecessary colons, redundant phrasing.

# Solution

## RULE 1: Abbreviations (CRITICAL)
- EVERY abbreviation (2+ capital letters) must be spelled out on first use
- Abstract: define key abbreviation, spell out everything else
- Introduction body: re-define all abbreviations at first use (Abstract and body are independent)
- After definition: use ONLY the abbreviation
- If abbreviation used only once: do NOT define, just spell out
- Variable names in equations: define at first use
- Organizations as citations (IEEE, ISO, SAE, NHTSA): no definition needed

## RULE 2: Terminology Consistency (CRITICAL)
- Pick ONE term per concept, use EVERYWHERE
- "driver readiness" not just "readiness" (avoids system readiness confusion)
- "Take-Over Request (TOR)" hyphenation — pick one and stick with it
- Method names: lowercase in body, abbreviated in tables
- SAE levels (Level 3): uppercase per standard
- Distraction levels (level 1, level 2): lowercase
- Domain-appropriate terms for general audience: say "vehicle data" not "CAN-bus signals"

## RULE 3: Sentence Flow (CRITICAL)
- Every consecutive sentence pair must have logical connection
- No abrupt subject changes between sentences
- Transition words varied: Nevertheless, Nonetheless, Accordingly, In contrast, In turn, Building on
- "However" ONLY for genuine contrasts (max 3 per paper)
- NEVER start sentence with: "Yet", "But", "So", "And"
- NEVER use "hereafter" — use "denoted" or "referred to as"
- Sentence length max ~35 words
- Paragraph transitions: first sentence must connect to previous paragraph's conclusion

## RULE 4: Vague Pronouns (CRITICAL — THIS IS THE #1 RECURRING MISTAKE)
- NEVER leave "This", "That", "These", "Those", "They", "It" without an explicit referent noun
- BAD: "This suggests..." → GOOD: "This finding suggests..."
- BAD: "These observations motivate..." → GOOD: "The two observations motivate..." or "Our findings motivate..."
- BAD: "This assumption needs..." → GOOD: "The homogeneity assumption needs..."
- BAD: "This study identifies..." → acceptable as fixed academic phrase, but prefer "The present study identifies..." or "Our study identifies..."
- BAD: "This high readiness..." → GOOD: "The observed high readiness..."
- BAD: "This is the first...", "That is because...", "These are..." (a demonstrative directly followed by a verb = no referent noun) → GOOD: "The present study is the first...", "This occurs because...", "These findings are..."
- Every pronoun at sentence start MUST be followed by or paired with a specific noun; a demonstrative (this/that/these/those) must be immediately followed by a noun, never by a verb (write "this result is", not "this is")

## RULE 5: Colons (CRITICAL)
- AVOID colons (":") for list introductions or explanations
- BAD: "Three types were identified: Focused, Exploratory, and Disengaged"
- GOOD: "Three types were identified, namely Focused, Exploratory, and Disengaged"
- GOOD: "Three types emerged. The Focused type..."
- BAD: "We found two observations: first..., second..."
- GOOD: "We found two observations. First..., second..."
- Colons are acceptable ONLY in table captions, figure captions, and section headings

## RULE 5B: Parentheses (minimize)
- Minimize parenthetical asides in body text; prefer a comma, a relative/subordinate clause, or splitting into a separate sentence
- BAD: "a purely additive (linear) model" → GOOD: "a purely additive model" (drop the redundant gloss), or "a purely additive, linear model"
- BAD: "the prediction error (N: number of samples)" → GOOD: "the prediction error for N samples", or "..., where N is the number of samples"
- BAD: "41.5 % (about 27 drivers)" → GOOD: "41.5 %, about 27 drivers" (trailing appositive with a comma)
- KEEP parentheses ONLY for: acronym definition on first use ("Random Forest (RF)"), in-text citations ("(Grabisch, 1997)"), and mathematical grouping or equation numbers ("(1/N)", "(7)")

## RULE 6: Number Consistency (CRITICAL — RECURRING MISTAKE)
- Pick ONE convention and use throughout
- Convention A: spell out <10, numerals ≥10 ("five types", "18 features")
- Convention B: numerals everywhere ("5 types", "18 features")
- NEVER mix: "Ninety-five drivers participated, and 93 were used" is WRONG
- FIX: "A total of 95 drivers participated, and 93 were used" (both numerals)
- FIX: rewrite to avoid starting sentence with number: "The study recruited 95 drivers..."
- Same dataset/variable referenced multiple times must use same style throughout

## RULE 7: Capitalization (CRITICAL)
- Section headings: SENTENCE CASE consistently (not Title Case)
  - GOOD: "Forward gaze paradox"
  - BAD: "Forward Gaze Paradox"
- Head1 may be ALL CAPS per template style (INTRODUCTION, METHOD, RESULTS)
- Head2: sentence case (first word only capitalized)
- DO NOT capitalize instrument names unless they are formal proper nouns
  - "Situation Awareness Rating Technique (SART)" — formal name, capitalized
  - "Driver Readiness" — NOT a formal name, use "driver readiness" (lowercase)
- Proper nouns (Choquet, Pearson, Cohen, Transformer, LSTM, Random Forest): capitalize
- General methods (weighted sum, harmonic mean): lowercase

## RULE 8: References
- Every citation ↔ reference list entry (bidirectional match)
- Reference must ACTUALLY support the claim
- Harvard format: [Author et al. Year]
- Alphabetical order strictly enforced
- Single author: [Wickens 2008] (no "et al.")
- Two authors: [Kutuk and Sezgin 2025]
- 3+ authors: [Gold et al. 2013]

## RULE 9: Academic Tone (CRITICAL)
- NEVER use informal intensifiers: "very", "really", "quite", "pretty much", "a lot"
  - BAD: "The very small SDs..." → GOOD: "The small SDs..." or precise quantifier
  - BAD: "very large improvement" → GOOD: "substantial improvement"
- NEVER "vs." → use "versus" or rewrite
  - BAD: "11.19 vs. 9.10" → GOOD: "11.19 compared with 9.10"
- NEVER informal narrative framing: "some X, while others Y"
  - BAD: "some drivers keep their gaze tight, while others scan the periphery"
  - GOOD: "drivers vary in their monitoring strategies, ranging from concentrated forward fixation to active peripheral scanning"
- NO "we" as subject in highly formal journals; in HCI/SIGGRAPH, "we" is acceptable but use sparingly
- No informal verbs: "drops sharply" → "deteriorates substantially"
- No direct quotes
- No overclaiming: simulator ≠ "real-world"

## RULE 10: Formatting
- Units: "s" not "seconds", "%" with space, "Hz", "km/h"
- "±" not "+/-"
- Minimal em dash "—" — prefer commas or separate sentences
- "pre-TOR and post-TOR" not "pre-/post-TOR"
- Curly quotes ' not straight '
- Equations: number right-aligned, equation centered
- Tables: 3-line style, no vertical lines
- Table "Note:" line: italic

## RULE 11: Participant/Demographic Info (CRITICAL)
- Do NOT bury demographics in parentheses
- BAD: "95 drivers participated (mean age 37.0 years; 48% female; mean licensure 2.4 years)"
- GOOD: "The study recruited 95 licensed drivers with a mean age of 37.0 years, 48% of whom were female, and a mean licensure of 2.4 years."

## RULE 12: Limitation Wording (CRITICAL)
- In Conclusion/Limitations, do NOT re-cite specific numerical values that already appeared in Results
- BAD: "Limited by the small Disengaged sample (n=10)..."
- GOOD: "Limited by the small Disengaged sample size..."
- BAD: "Given the modest effect size (η²=.092)..."
- GOOD: "Given the modest effect size observed in this scenario..."

## RULE 13: Redundant Phrasing (CRITICAL)
- CHECK adjacent sentences for repeated phrases — remove or restructure
- BAD:
  > "In the cut-in scenario, TOR was triggered during a visual NDRT. In the pedestrian scenario, TOR was triggered during a visual NDRT."
- GOOD:
  > "Both the cut-in and pedestrian scenarios involved a visual NDRT; TOR was triggered by a lead vehicle cutting in and by a pedestrian entering the road, respectively."
- If you write the same 5+ word phrase twice within adjacent sentences, rewrite

## RULE 14: Abstract Structure (CRITICAL — SIGGRAPH/ACM style)
Required order:
1. **Background** (1 sentence): domain context
2. **Limitation** (1 sentence): what prior work missed, specifically and precisely
3. **Goal** (1 sentence): what THIS study aims to do (verb: "aims to", "seeks to")
4. **Method** (1-2 sentences): how we did it
5. **Contribution/Findings** (2-3 sentences): what we found
6. **Impact** (1 sentence): why it matters for the field

Do NOT skip steps. Do NOT bury the goal inside the method.

## RULE 15: "Homogeneous population" Misuse (CONCEPT-SPECIFIC)
- "Treated drivers as a homogeneous population" is IMPRECISE
- Prior work never CLAIMED homogeneity — they just didn't model individual differences systematically
- CORRECT: "Individual differences in [specific behavior] have not been systematically modeled"
- CORRECT: "Prior work has emphasized population-level effects over individual variability"
- CORRECT: "Prior work has not systematically characterized individual differences in [behavior]"

## RULE 16: Pre-Submission Checklist (EXPANDED)
- [ ] All abbreviations defined before first use
- [ ] "This/That/These/Those/They/It" always paired with explicit noun
- [ ] "However" count ≤ 3
- [ ] Zero "very", "really", "quite", "pretty" in body
- [ ] Zero "vs." in body
- [ ] Zero colons in body text (only in captions/headings)
- [ ] Zero "Yet"/"But"/"So" at sentence start
- [ ] Number style consistent throughout
- [ ] Demographics in main sentence, not parentheses
- [ ] Limitations section has no specific numerical values repeated from Results
- [ ] No back-to-back sentences with identical 5+ word phrases
- [ ] Abstract follows Background→Limitation→Goal→Method→Findings→Impact
- [ ] "Homogeneous population" replaced with "individual differences not modeled"
- [ ] All references bidirectionally matched
- [ ] Section heading capitalization: sentence case (except Head1 all-caps per template)
- [ ] Instrument names: formal names capitalized (SART), informal terms lowercase (driver readiness)
- [ ] Curly quotes not straight quotes
- [ ] No em dashes (or ≤1)
