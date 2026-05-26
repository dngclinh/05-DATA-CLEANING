# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mục tiêu
Chuẩn hóa danh sách công ty B2B (ngành xây dựng Đức) theo template cố định, gán tags `type, service`, phục vụ pipeline leads end-to-end.

Module này là **bước 5/7** trong pipeline: Nhận file thô → Keywords → Tìm nguồn → Scrape → **[Làm sạch]** → Contact person → Báo cáo.

## Commands

**Setup**
```
pip install -r requirements.txt
```
Dependencies: `pandas`, `openpyxl`, `phonenumbers`

**Run cleaning pipeline**
```
python src/main.py leads.xlsx
python src/main.py leads.xlsx --output leads_cleaned.xlsx
```

**Slash commands**
| Command | Mô tả | Trạng thái |
|---------|-------|-----------|
| `/clean` | Normalize + backup + highlight file .xlsx | ✅ Tested |
| `/classify` | Enrich missing contact fields + gán tag type/service từ website | ✅ Tested (31 sites) |
| `/contact` | Tìm contact persons (tên, chức vụ tiếng Anh, email, SĐT) — mỗi người 1 dòng | ✅ Tested (31 công ty, 43 contacts) |
| `/report` | Báo cáo thống kê kết quả | ⚠️ Cần cập nhật cho 4 cột contact |
| `/researcher` | Nghiên cứu và tóm tắt thông tin theo yêu cầu | ✅ Mới thêm |

## Output template

```
Company Name | Street | City | Zip | Website | Phone | E-Mail | Contact Person | Position | Contact Email | Contact Phone | Note / Category
```

Xem chi tiết schema, n.a rules, và yellow highlight tại `.claude/rules/output-schema.md`.

## Architecture

Four modules, each with a single responsibility:

| Module | Role |
|--------|------|
| `src/tags.py` | Single source of truth: `COLUMNS` order, `TYPES`, `SERVICES`, `HIGHLIGHT_COLUMNS`, `NA_VALUE`, `is_valid_note()` |
| `src/normalizer.py` | Pure transformation: fills empty→`n.a`, lowercases + de-obfuscates emails, formats phones to international, builds change log and yellow-cell list |
| `src/excel_handler.py` | Excel I/O only: `backup()`, `load()` (reads all cells as strings), `save()` writes two sheets with yellow highlights |
| `src/main.py` | Orchestrator: wires `backup→load→normalize→save`, exposes `argparse` CLI |

**Data flow**
```
input.xlsx
  └─ backup copy (<stem>_backup_YYYYMMDD_HHMMSS.xlsx)
  └─ load() → DataFrame
  └─ normalize() → (cleaned_df, changes, yellow_cells)
  └─ save() → output_cleaned.xlsx
       ├─ Sheet "Data"         — 12 columns, n.a filled, yellow on missing Website/E-Mail
       └─ Sheet "Deleted Data" — only logs cells where real content was erased (safety net, usually empty)
```

**Normalization applied to**: E-Mail, Contact Email, Phone, Contact Phone (all 4 contact-related columns).

**Extending:**
- New normalization rules → edit `normalizer.normalize()` only
- New columns → update `tags.COLUMNS` and `tags.HIGHLIGHT_COLUMNS` if applicable

## Known gaps (as of 2026-05-12)

- **ZIP-from-City extraction**: session-2026-05-08b applied this logic manually but it is **not yet in `normalizer.py`**. Next time raw data has "12345 Berlin" in City, normalizer will not auto-split. Add `_extract_zip_from_city()` helper to normalizer before processing new raw files.
- **`/report`**: currently does not report contact column coverage. Update `skills/report.md` to include Contact Person found/missing stats.

## Rules

| File | `alwaysApply` | Khi nào load |
|------|:---:|---------|
| `.claude/rules/output-schema.md` | ✅ | Luôn luôn — schema 12 cột, n.a, yellow, email/phone format |
| `.claude/rules/data-cleaning.md` | — | Khi mở `src/normalizer.py`, `excel_handler.py`, `tags.py` |
| `.claude/rules/classification.md` | — | Khi mở `agents/tagger.md` hoặc `src/tags.py` |
| `.claude/rules/web-enrichment.md` | — | Khi mở `agents/tagger.md` — visit priority, field extraction |
| `.claude/rules/contact-person.md` | — | Khi mở `agents/contact-finder.md` — senior titles, 1 row/person |

## Skills

Skills là **interface layer** — chứa trigger phrases, xử lý `$ARGUMENTS`, và file selection logic. Mỗi skill gọi agent tương ứng để thực thi:

| Skill | Agent | Nội dung skill |
|-------|-------|---------------|
| `.claude/skills/clean.md` | `agents/cleaner.md` | Trigger + Glob *.xlsx + usage |
| `.claude/skills/classify.md` | `agents/tagger.md` | Trigger + Glob *_cleaned.xlsx + usage |
| `.claude/skills/contact.md` | `agents/contact-finder.md` | Trigger + Glob *_cleaned.xlsx + usage |
| `.claude/skills/report.md` | *(đọc file trực tiếp)* | Trigger + báo cáo spec |
| `.claude/skills/researcher.md` | `agents/researcher.md` | Trigger + usage examples |

## Agents

Agents là **execution layer** — chứa logic thực thi theo format 9 thành phần. Mỗi agent có `tools:` khai báo rõ trong frontmatter:

| File | `tools:` | Vai trò |
|------|---------|---------|
| `.claude/agents/cleaner.md` | `[Glob, Read, Bash, Write]` | Chạy Python pipeline, backup, báo cáo |
| `.claude/agents/tagger.md` | `[Glob, Read, Write, WebFetch, WebSearch]` | Enrich contact + classify type/service từ website |
| `.claude/agents/contact-finder.md` | `[Glob, Read, Write, WebFetch, WebSearch]` | Tìm contact person cấp cao — ghi Position bằng tiếng Anh |
| `.claude/agents/researcher.md` | `[WebFetch, WebSearch, Read, Glob, Grep]` | Nghiên cứu và tóm tắt thông tin theo yêu cầu |

**Format 9 thành phần** (áp dụng cho mọi agent): Mục tiêu và vai trò → Bộ não suy luận → Prompt hệ thống/Policy → Bộ nhớ → Khả năng lập kế hoạch → Tool use → Feedback loop → Tự đánh giá → Guardrails và an toàn.

## Session handoff
Ghi chú làm việc theo session lưu tại `.claude/handoff/`. Đọc file mới nhất để nắm trạng thái hiện tại, việc chưa làm xong, và quyết định đã chốt trước khi bắt đầu session mới.
