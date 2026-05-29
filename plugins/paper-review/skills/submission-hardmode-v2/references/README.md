# References Folder

## Purpose

This folder stores reference materials used by the SUBMISSION_HARDMODE_v2 skill.

## Structure

```
references/
├── journal_papers/         # Target journal example papers (3-5 recent papers)
│   ├── {journal}_{year}_{author}.pdf
│   └── ...
├── paper_inventory.json    # Metadata of collected papers (auto-generated)
└── README.md              # This file
```

## Journal Papers Folder

### Auto-Collection (PHASE -1)

If you don't provide `journal_examples_folder`, the skill will automatically:
1. Search for 3-5 recent papers from your target journal
2. Download PDFs (if available) or save metadata
3. Store them in `journal_papers/` folder
4. Create `paper_inventory.json` with metadata

### Manual Addition

You can also manually add papers before running the skill:

```bash
.claude/skills/submission-hardmode-v2/references/journal_papers/
├── tochi_2023_smith.pdf
├── tochi_2023_jones.pdf
├── tochi_2024_brown.pdf
└── ...
```

**Naming convention**: `{journal_abbrev}_{year}_{first_author}.pdf`

### Requirements

For best profiling results, papers should:
- ✅ Be from the **target journal** (same venue)
- ✅ Be **recent** (2022-2024 preferred)
- ✅ Represent **diverse methodologies** (quantitative, qualitative, mixed)
- ✅ Be **high quality** (high citations, well-structured)
- ✅ Match your **field** (HCI, AI, etc.)

### What Gets Analyzed

PHASE 0 (Journal Profiling) extracts from these papers:
- Contribution framing patterns
- Methodological rigor expectations
- Structural norms (section organization)
- Statistical reporting standards
- Writing style conventions
- Aim & Scope alignment

## Paper Inventory

`paper_inventory.json` contains metadata:

```json
{
  "papers": [
    {
      "title": "Example Paper Title",
      "authors": "Smith, J., Jones, A.",
      "year": 2023,
      "doi": "10.1145/1234567",
      "pdf_link": "https://...",
      "saved_as": "tochi_2023_smith.pdf",
      "collected_date": "2026-02-11",
      "collection_method": "auto|manual"
    }
  ],
  "total_count": 5,
  "target_journal": "ACM TOCHI",
  "field": "Human-Computer Interaction"
}
```

## Troubleshooting

### No papers collected automatically
- Librarian may not have access to PDFs behind paywall
- Check `paper_inventory.json` for metadata
- Manually download PDFs from DOI links

### Papers don't match my field
- Set `field` parameter correctly in skill invocation
- Manually curate papers in this folder before running skill

### Papers are outdated
- Auto-collection prioritizes 2022-2024
- If auto-search finds older papers, manually replace with newer ones

## Notes

- Papers stored here are for **analysis only** (not redistributed)
- PDFs are NOT included in skill distribution
- This folder is gitignored by default
- Clear this folder between different journal targets
