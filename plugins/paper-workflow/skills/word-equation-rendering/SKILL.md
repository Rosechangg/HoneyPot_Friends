---
id: "skill-m5h7k2-b3c4"
name: word-equation-rendering
description: "Fixes for LaTeX-to-OMML equation rendering in python-docx Word files — multi-letter variables, special symbols, fraction handling"
source: "extracted"
createdAt: "2026-04-03T18:00:00Z"
triggers:
  - "equation rendering"
  - "OMML"
  - "Word equation"
  - "수식 변환"
  - "수식 깨짐"
  - "latex to word"
tags:
  - "python-docx"
  - "OMML"
  - "equation"
  - "Word"
quality: 95
usageCount: 0
---

# Problem

When converting LaTeX equations to OMML (Office MathML) for Word documents using python-docx, several rendering issues occur:
1. Multi-letter variables (DR, HM, ch) split into individual letters (D R, H M)
2. LaTeX commands like `\neq` not converted when adjacent to other characters
3. English words in equations (e.g., "for all") render as individual letters
4. `+/-` not converted to `±`
5. `--` (em dash) appearing instead of proper formatting

# Solution

## 1. Token Parser Fix for Multi-Letter Variables

The default LaTeX token regex only matches single characters. Add multi-letter pattern:

```python
_TOKEN_RE = re.compile(
    r'(\\[A-Za-z]+|\\[^A-Za-z]'   # \command or \symbol
    r'|_\{[^}]*\}|\^\{[^}]*\}'     # _{...} or ^{...}
    r'|_[^{]|\^[^{]'               # _x or ^x
    r'|\{[^}]*\}'                   # {group}
    r'|[A-Za-z]{2,}'               # multi-letter variable names (DR, HM, ch)
    r'|[^\\_{^}\s])'               # any other single char
)
```

The key addition is `[A-Za-z]{2,}` which matches consecutive letters as one token.

## 2. LaTeX Command Spacing

Commands like `\neq` must be separated from adjacent characters by spaces:
- WRONG: `j\neq i` → parser sees "j\neq" as one token
- RIGHT: `j \neq i` → parser correctly separates j, ≠, i

## 3. English Words in Equations

Replace English words with LaTeX symbols:
- `for all` → `\forall` (∀)
- `for` in equations splits into `f o r`

## 4. Text Replacements Before OMML Conversion

Apply these replacements globally in the markdown BEFORE converting:
```python
# In the markdown file
sed -i 's/+\/-/±/g'  # plus-minus
sed -i 's/ -- /, /g'  # em dash to comma (except in reference titles)
```

## 5. Style Detection for Multi-Letter Tokens

In the OMML builder, multi-letter tokens should use plain style ('p'), not italic ('i'):
```python
sty = 'p' if (len(resolved) > 1 or (resolved and ord(resolved[0]) > 127)) else 'i'
```

This ensures "DR" renders as upright "DR" not italic "𝐷𝑅".

## 6. Table Formatting in Word

### 3-line academic table borders:
- Top line, header-bottom line, table-bottom line only
- No vertical lines, no insideH (except header bottom)

### Multi-row header detection:
```python
def detect_header_rows(rows):
    if len(rows) < 2: return 1
    row0_empty = sum(1 for c in rows[0] if c.strip() == '')
    row1_empty = sum(1 for c in rows[1] if c.strip() == '')
    if row0_empty >= 2 and row1_empty < row0_empty: return 2
    return 1
```

### Table width: use percentage width to prevent cell wrapping
```python
tblW.set(qn('w:type'), 'pct')
tblW.set(qn('w:w'), '5000')  # 100% page width
```

## 7. Table Cell Markdown Parsing

Tables with statistical markers (`*p < .05`, `**p < .01`, `.153*`) must NOT have `*` parsed as bold/italic markdown. In `add_table_to_doc`, use `parse_md=False` for table cells but still handle inline `$math$`:

```python
# In table cells: parse $math$ but NOT *bold*/*italic*
math_parts = re.split(r'(\$[^$]+?\$)', cell_text)
for mp in math_parts:
    if mp.startswith('$') and mp.endswith('$'):
        _insert_inline_math(p, mp[1:-1])
    elif mp:
        run = p.add_run(mp)
```

## 8. Common Pitfalls Checklist
- [ ] All `+/-` replaced with `±`
- [ ] All `--` in body text replaced (keep in reference titles)
- [ ] Multi-letter variables render as single unit in Word
- [ ] `\neq`, `\leq`, `\geq` have spaces around them in LaTeX source
- [ ] No "for all" text in equations — use `\forall`
- [ ] Variable names consistent between equations (e.g., DR_V not R_V in equation 6 if DR_V used in equation 1)
- [ ] Table cells: `*` statistical markers preserved (not parsed as markdown)
- [ ] Table cells: `$DR_{self,2}$` inline math still renders correctly
- [ ] Verify by extracting OMML text from generated docx
