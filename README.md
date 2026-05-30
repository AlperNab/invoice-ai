# Invoice Ai

This folder has been upgraded into a **standalone real GUI project**.

Run the project GUI:

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default local URL: `http://127.0.0.1:9128`

This project includes its own FastAPI backend, browser GUI, provider settings, local/cloud LLM routing, encrypted API-key storage, file uploads, job history, exports, and a project-specific plugin configuration.

See `PROJECT_IMPLEMENTATION.md` and `project_config.json` for the applied project-specific features and customization controls.

---

## Original README

# invoice-ai

> **Photo or PDF of any invoice → structured JSON.** Vendor, line items, totals, VAT, due date, PO number, multi-currency, multi-language. Powered by Claude vision.

[![PyPI](https://img.shields.io/pypi/v/invoice-ai?style=flat)](https://pypi.org/project/invoice-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude](https://img.shields.io/badge/Powered_by-Claude-D97757?style=flat)](https://anthropic.com)

## Quickstart

```bash
pip install invoice-ai
python -m invoice_ai receipt.pdf
python -m invoice_ai invoice.jpg --json
```

## Output

```json
{
  "invoice_number": "INV-2025-0042",
  "invoice_date": "2025-05-22",
  "due_date": "2025-06-22",
  "vendor": { "name": "Acme Corp", "vat_number": "GB123456789" },
  "line_items": [
    { "description": "Web development", "quantity": 40, "unit_price": 120.00, "total": 4800.00 }
  ],
  "subtotal": 4800.00,
  "tax_total": 960.00,
  "total": 5760.00,
  "amount_due": 5760.00,
  "currency": "GBP",
  "confidence": 0.97
}
```

## Supported formats

PDF, PNG, JPEG, WEBP, TIFF — any invoice from any country in any language.

## Python API

```python
from invoice_ai import parse_invoice, parse_from_bytes

result = parse_invoice("invoice.pdf")
print(f"Total due: {result['currency']}{result['amount_due']}")

# From bytes (for web APIs)
result = parse_from_bytes(file_bytes, "invoice.pdf", "application/pdf")
```

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
