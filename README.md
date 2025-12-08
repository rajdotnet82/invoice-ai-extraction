# Invoice AI Extraction (Excel-Only + LLM)

A lightweight, case-study-style app that extracts structured invoice data from **uploaded invoice images** using an LLM, then saves it into an **Excel-only datastore** (`SalesOrderHeader` + `SalesOrderDetail`).  
Designed to be fast, simple, and easy to demo.

---

## What this does

✅ Upload an invoice image (`.jpg/.jpeg/.png`)  
✅ LLM extracts invoice fields into JSON  
✅ Preview extracted JSON in the UI  
✅ Save results into Excel (no database)  
✅ Works with multiple invoice templates (extendable)

This project intentionally uses Excel as the only “database” to match the original case study constraints.

---

## Architecture (high level)

**Frontend (Next.js)**
- Upload-only UI
- Two actions:
  - **Extract Only (File)**
  - **Extract & Save (File)**
- Displays extracted JSON and save result

**Backend (Flask)**
- Accepts file uploads
- Calls LLM to extract invoice JSON
- Normalizes basic totals/rates
- Persists into Excel sheets:
  - `SalesOrderHeader`
  - `SalesOrderDetail`

**Storage**
- `backend/data/Case Study Data_tiny.xlsx` is the source of truth  
- `backend/uploads/` stores temporary files during processing

---

## Tech stack

- **Frontend:** Next.js (App Router), TypeScript
- **Backend:** Flask, Flask-CORS
- **Data:** Excel via `pandas` + `openpyxl`
- **AI:** OpenAI API
- **Local env:** `python-dotenv`

---

## How to run (Backend)

### Prerequisites
- Python 3.11+ recommended

### Install dependencies

```bash
cd backend
python -m pip install -r requirements.txt
```

### Update your OpenAI API key

Create or edit:

`backend/.env`

```env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
```

> This step is required. The backend will not extract invoices without a valid key.

### Start the backend

```bash
python app.py
```

Backend runs on:
- `http://127.0.0.1:5000`

---

## How to run (Frontend)

### Prerequisites
- Node 18+ recommended

### Install dependencies

```bash
cd frontend
npm install
```

### Configure API base URL

Create or edit:

`frontend/.env.local`

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5000
```

### Start the frontend

```bash
npm run dev
```

Frontend runs on:
- `http://localhost:3000`

---

## API endpoints

### Health

```http
GET /api/health
```

### Extract Only (File)

```http
POST /api/extract-file
Content-Type: multipart/form-data
file: <invoice.jpg>
```

### Extract & Save (File)

```http
POST /api/extract-and-save-file
Content-Type: multipart/form-data
file: <invoice.jpg>
```

Response includes:
- `filename`
- `extracted` JSON
- `salesOrderId` (on save)

---

## Quick demo steps

1. Start the backend
2. Start the frontend
3. Open `http://localhost:3000`
4. Upload `backend/test-invoices/invoice.jpg`
5. Click:
   - **Extract Only (File)**
   - **Extract & Save (File)**
6. Open:
   - `backend/data/Case Study Data_tiny.xlsx`
7. Verify new rows in:
   - `SalesOrderHeader`
   - `SalesOrderDetail`

---

## Notes on Excel-only persistence

This app simulates a relational structure inside Excel:
- A header row is appended to `SalesOrderHeader`
- Line items are appended to `SalesOrderDetail`
- IDs increment to mimic database identity behavior

---

## Security

- Do not commit `.env` or API keys.
- Keep keys server-side only.

Recommended backend `.gitignore`:

```gitignore
.env
__pycache__/
uploads/*
*.pyc
```

---

## Roadmap

- [ ] Editable form UI before saving
- [ ] PDF upload support
- [ ] Confidence scoring + validation warnings
- [ ] Multi-template test suite

---

## License

MIT (or your preferred license)
