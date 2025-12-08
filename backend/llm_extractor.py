import os
import json
import base64
import mimetypes
from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

client = OpenAI(api_key=api_key)

SYSTEM = """
You are an invoice extraction engine.

Return ONLY valid JSON with this structure:
{
  "invoiceNumber": string,
  "orderDate": "YYYY-MM-DD",
  "dueDate": "YYYY-MM-DD",
  "shipDate": "YYYY-MM-DD or null",
  "purchaseOrderNumber": "string or null",
  "customer": { "customerId": 0, "accountNumber": null, "name": string },
  "terms": "string or null",
  "shipVia": "string or null",
  "subtotal": number,
  "taxRate": number,
  "tax": number,
  "freight": number,
  "totalDue": number,
  "lineItems": [
    {
      "itemNumber": "string or null",
      "description": string,
      "qty": number,
      "unitPrice": number,
      "unitPriceDiscount": number,
      "lineTotal": number
    }
  ]
}

Rules:
- If unknown, use null (where allowed) and customerId=0.
- Dates must be YYYY-MM-DD when you can infer them.
- Ensure lineTotal is consistent with qty and unitPrice where possible.
- If taxRate is not shown, estimate it as tax/subtotal when possible, else 0.
- If totals are missing, infer them from line items and tax/freight.
"""

def _parse_json(content: str, context: str):
    content = (content or "").strip()
    if not content:
        raise ValueError(f"Model returned empty content for {context}")

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        preview = content[:200].replace("\n", " ")
        raise ValueError(f"Invalid JSON for {context}. Preview: {preview}") from e


def extract_invoice_text(text: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    if not text or not text.strip():
        raise ValueError("Empty invoice text")

    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM.strip()},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    return _parse_json(resp.choices[0].message.content, "text extraction")


def extract_invoice_image(file_path: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    mime, _ = mimetypes.guess_type(file_path)
    if not mime:
        mime = "image/jpeg"

    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    data_url = f"data:{mime};base64,{b64}"

    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM.strip()},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract invoice fields from this image."},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    return _parse_json(resp.choices[0].message.content, "image extraction")


__all__ = ["extract_invoice_text", "extract_invoice_image"]
