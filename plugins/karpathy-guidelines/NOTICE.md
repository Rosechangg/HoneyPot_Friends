# NOTICE

This plugin (`karpathy-guidelines`) contains content imported from a third-party open-source project.

---

## `skills/karpathy-guidelines/`

The four behavioral principles in this skill (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) are **imported verbatim** from:

- **Project**: [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- **Source file**: [`skills/karpathy-guidelines/SKILL.md`](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md)
- **Pinned commit**: `2c606141936f1eeef17fa3043a72095b4765b9c2` (`main` as of 2026-04-20)
- **Author**: forrestchang (org: [multica-ai](https://github.com/multica-ai))
- **License**: MIT (declared in the upstream `.claude-plugin/plugin.json` and in the skill's own frontmatter)
- **Original idea source**: [Andrej Karpathy's observations on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876)

> **License note:** The upstream repository declares MIT in its `plugin.json` and `SKILL.md`
> frontmatter, but does **not** ship a standalone `LICENSE` file or an explicit copyright line.
> The standard MIT License text reproduced below reflects those declared MIT terms. The
> conceptual content originates from Andrej Karpathy's public observations and is credited above.

### Changes in this import (각색 내역)

The behavioral content of the four principles is reproduced **verbatim** with no edits. The
following packaging-only changes were made to fit the `HoneyPot_Friends` marketplace:

1. Repackaged as a standalone plugin at `plugins/karpathy-guidelines/` and registered in the
   marketplace `.claude-plugin/marketplace.json`.
2. Added this `NOTICE.md` and a "Source / 출처" section at the end of `SKILL.md` pointing back to
   the upstream project, pinned commit, and original idea source.
3. Did **not** import the upstream's other files (`CLAUDE.md`, `CURSOR.md`, `EXAMPLES.md`,
   `.cursor/rules/`, READMEs) — only the `karpathy-guidelines` skill was brought over.

---

## MIT License (multica-ai/andrej-karpathy-skills)

```
MIT License

Copyright (c) forrestchang and the multica-ai/andrej-karpathy-skills contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
