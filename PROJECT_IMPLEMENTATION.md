# Invoice Ai — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9128`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/invoice-ai.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `Finance / Accounts Payable`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Invoice file → extracted fields and validation
- Suite: `Finance Document Suite`

## Deep features applied

- OCR/vision extraction
- vendor matching
- PO matching
- tax/VAT validation
- duplicate detection
- approval workflow
- ERP export

## Customization controls

- `execution_mode` — Execution mode (select)
- `country` — country (select)
- `currency` — currency (select)
- `tax_rules` — tax rules (textarea)
- `vendor_list` — vendor list (text)
- `po_tolerance` — PO tolerance (slider)
- `approval_levels` — approval levels (select)
- `export_schema` — export schema (select)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `invoice_file` — Invoice file (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Finance Ops Console** pattern.

**UX workflow:** Document intake → extraction → validation → approval/export

**Domain components:**
- Invoice header card
- Line-item extraction table
- VAT/tax validator
- PO matching panel
- Approval queue

**Quick actions:**
- Extract invoice fields
- Validate totals/VAT
- Detect duplicate invoice
- Prepare ERP export

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
