#!/usr/bin/env python3
"""
invoice-ai — photo/PDF of any invoice → structured JSON
Handles: vendor, line items, totals, VAT, due date, PO number, multi-currency, multi-language
"""
import anthropic
import base64
import json
import sys
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


SYSTEM = """You are an expert accounts payable specialist and document parser.
Extract ALL information from this invoice into a structured JSON object.

Return ONLY valid JSON — no markdown, no explanation, no backticks.

Required format:
{
  "invoice_number": "string or null",
  "invoice_date": "YYYY-MM-DD or null",
  "due_date": "YYYY-MM-DD or null",
  "po_number": "string or null",
  "vendor": {
    "name": "string",
    "address": "string or null",
    "email": "string or null",
    "phone": "string or null",
    "tax_id": "string or null",
    "vat_number": "string or null"
  },
  "bill_to": {
    "name": "string or null",
    "address": "string or null",
    "email": "string or null"
  },
  "line_items": [
    {
      "description": "string",
      "quantity": number,
      "unit_price": number,
      "total": number,
      "tax_rate": number or null,
      "tax_amount": number or null,
      "sku": "string or null"
    }
  ],
  "subtotal": number,
  "discount": number or null,
  "discount_type": "percentage|fixed|null",
  "tax_total": number or null,
  "shipping": number or null,
  "total": number,
  "amount_paid": number or null,
  "amount_due": number,
  "currency": "USD|EUR|GBP|EGP|AED|...",
  "payment_terms": "string or null",
  "payment_method": "string or null",
  "bank_details": {
    "bank_name": "string or null",
    "account_number": "string or null",
    "iban": "string or null",
    "swift": "string or null"
  },
  "notes": "string or null",
  "detected_language": "en|ar|fr|de|es|...",
  "confidence": 0.0
}"""


def encode_file(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    types = {".pdf": "application/pdf", ".png": "image/png",
             ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".webp": "image/webp", ".tiff": "image/tiff"}
    media_type = types.get(suffix, "application/pdf")
    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return media_type, data


def parse_invoice(file_path: str) -> dict:
    client = anthropic.Anthropic()
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    media_type, data = encode_file(path)
    is_pdf = "pdf" in media_type

    content_block = {
        "type": "document" if is_pdf else "image",
        "source": {"type": "base64", "media_type": media_type, "data": data}
    }

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                content_block,
                {"type": "text", "text": "Extract all invoice data from this document."}
            ]
        }]
    )

    text = response.content[0].text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text)


def parse_from_bytes(content: bytes, filename: str, media_type: str) -> dict:
    """Parse invoice from raw bytes — useful in web APIs."""
    client = anthropic.Anthropic()
    data = base64.standard_b64encode(content).decode("ascii")
    is_pdf = "pdf" in media_type

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document" if is_pdf else "image",
                    "source": {"type": "base64", "media_type": media_type, "data": data}
                },
                {"type": "text", "text": "Extract all invoice data from this document."}
            ]
        }]
    )

    text = response.content[0].text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text)


def format_output(result: dict) -> str:
    """Format parsed invoice as readable text."""
    lines = []
    vendor = result.get("vendor", {})
    lines.append(f"\n{'─'*50}")
    lines.append(f"  INVOICE PARSED")
    lines.append(f"{'─'*50}")
    lines.append(f"  Invoice #:    {result.get('invoice_number', 'N/A')}")
    lines.append(f"  Date:         {result.get('invoice_date', 'N/A')}")
    lines.append(f"  Due:          {result.get('due_date', 'N/A')}")
    lines.append(f"  Vendor:       {vendor.get('name', 'N/A')}")
    if vendor.get("vat_number"):
        lines.append(f"  VAT Number:   {vendor['vat_number']}")
    lines.append(f"\n  Line items:")
    for item in result.get("line_items", []):
        lines.append(f"    • {item.get('description', '?')}")
        lines.append(f"      {item.get('quantity', 0)} × {result.get('currency','')}{item.get('unit_price', 0):.2f} = {result.get('currency','')}{item.get('total', 0):.2f}")
    lines.append(f"\n  Subtotal:     {result.get('currency', '')}{result.get('subtotal', 0):.2f}")
    if result.get("tax_total"):
        lines.append(f"  Tax:          {result.get('currency', '')}{result.get('tax_total', 0):.2f}")
    lines.append(f"  TOTAL DUE:    {result.get('currency', '')}{result.get('amount_due', 0):.2f}")
    lines.append(f"\n  Confidence:   {int(result.get('confidence', 0) * 100)}%")
    lines.append(f"  Language:     {result.get('detected_language', 'en').upper()}")
    lines.append(f"{'─'*50}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m invoice_ai <invoice.pdf|.png|.jpg> [--json]")
        sys.exit(0)

    result = parse_invoice(sys.argv[1])

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))
