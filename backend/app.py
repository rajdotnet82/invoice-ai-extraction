from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from excel_store_fast import save_order_from_json
from llm_extractor import extract_invoice_image

app = Flask(__name__)

CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]}}
)

UPLOAD_DIR = "uploads"
ALLOWED_EXT = {".png", ".jpg", ".jpeg"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


def normalize_extracted(extracted: dict):
    subtotal = float(extracted.get("subtotal", 0) or 0)
    tax = float(extracted.get("tax", 0) or 0)
    freight = float(extracted.get("freight", 0) or 0)

    # Fix taxRate if clearly wrong
    if subtotal > 0:
        inferred_rate = tax / subtotal
        if 0 <= inferred_rate <= 0.2:
            extracted["taxRate"] = round(inferred_rate, 4)

    # Recompute totalDue if missing
    computed_total = subtotal + tax + freight
    if not extracted.get("totalDue"):
        extracted["totalDue"] = round(computed_total, 2)

    return extracted


def validate_and_save_upload():
    if "file" not in request.files:
        return None, None, (jsonify({"error": "Missing file field"}), 400)

    f = request.files["file"]
    if not f or not f.filename:
        return None, None, (jsonify({"error": "Empty file"}), 400)

    filename = secure_filename(f.filename)
    ext = os.path.splitext(filename.lower())[1]

    if ext not in ALLOWED_EXT:
        return None, None, (jsonify({"error": f"Unsupported file type: {ext}. Use png/jpg/jpeg"}), 400)

    saved_path = os.path.join(UPLOAD_DIR, filename)
    f.save(saved_path)

    return filename, saved_path, None


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/extract-file")
def extract_file():
    filename, saved_path, error_resp = validate_and_save_upload()
    if error_resp:
        return error_resp

    try:
        extracted = extract_invoice_image(saved_path)
        extracted = normalize_extracted(extracted)

        return jsonify({
            "filename": filename,
            "extracted": extracted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/extract-and-save-file")
def extract_and_save_file():
    filename, saved_path, error_resp = validate_and_save_upload()
    if error_resp:
        return error_resp

    try:
        extracted = extract_invoice_image(saved_path)
        extracted = normalize_extracted(extracted)

        new_id = save_order_from_json(extracted)
        if not new_id:
            raise Exception("Excel save returned no SalesOrderID. Check save_order_from_json return.")

        return jsonify({
            "message": "Extracted (file) and saved",
            "filename": filename,
            "salesOrderId": new_id,
            "extracted": extracted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
