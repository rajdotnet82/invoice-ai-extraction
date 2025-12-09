"use client";

import { useMemo, useState } from "react";

export default function Home() {
  const API_BASE = useMemo(
    () => process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:5000",
    []
  );

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // FILE FLOW (UPLOAD ONLY)
  const [file, setFile] = useState<File | null>(null);
  const [lastExtractedFile, setLastExtractedFile] = useState<any>(null);
  const [lastSavedResult, setLastSavedResult] = useState<any>(null);

  function resetErrors() {
    setError(null);
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setLastExtractedFile(null);
    // Optional: clear last save when selecting new file
    // setLastSavedResult(null);
  }

  // Extract Only (File)
  async function extractOnlyFile() {
    if (!file) return;

    setBusy(true);
    resetErrors();
    setLastExtractedFile(null);

    try {
      const form = new FormData();
      form.append("file", file);

      const res = await fetch(`${API_BASE}/api/extract-file`, {
        method: "POST",
        body: form,
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.error || `HTTP ${res.status}`);

      setLastExtractedFile(data); // { filename, extracted }
    } catch (e: any) {
      setError(e?.message || "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  // Extract & Save (File)
  async function extractAndSaveFile() {
    if (!file) return;

    setBusy(true);
    resetErrors();

    try {
      const form = new FormData();
      form.append("file", file);

      const res = await fetch(`${API_BASE}/api/extract-and-save-file`, {
        method: "POST",
        body: form,
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.error || `HTTP ${res.status}`);

      setLastSavedResult(data);
    } catch (e: any) {
      setError(e?.message || "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main
      style={{
        padding: 24,
        fontFamily: "system-ui, sans-serif",
        maxWidth: 1100,
      }}
    >
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 6 }}>
        Invoice AI Extraction (Upload → Excel)
      </h1>
      <p style={{ marginTop: 0, color: "#555" }}>
        Upload invoice image → LLM → JSON → Save to Excel
      </p>

      {/* FILE SECTION */}
      <section
        style={{
          marginTop: 18,
          padding: 12,
          border: "1px solid #ddd",
          borderRadius: 8,
        }}
      >
        <div style={{ fontWeight: 650, marginBottom: 8 }}>
          Upload invoice image (jpg/png)
        </div>

        <input
          type="file"
          accept=".png,.jpg,.jpeg"
          onChange={handleFileChange}
        />

        <div
          style={{ display: "flex", gap: 12, marginTop: 12, flexWrap: "wrap" }}
        >
          <button
            onClick={extractOnlyFile}
            disabled={busy || !file}
            style={btnStyle(busy || !file)}
          >
            Extract Only (File)
          </button>

          <button
            onClick={extractAndSaveFile}
            disabled={busy || !file}
            style={btnStyle(busy || !file)}
          >
            Extract & Save (File)
          </button>
        </div>

        {!!file && (
          <div style={{ marginTop: 10, color: "#666", fontSize: 12 }}>
            Selected: <strong>{file.name}</strong>
          </div>
        )}

        {lastExtractedFile?.extracted && (
          <div style={{ marginTop: 14 }}>
            <div style={{ fontWeight: 600, marginBottom: 6 }}>
              Extracted JSON (File)
            </div>
            <pre style={preStyle}>
              {JSON.stringify(lastExtractedFile.extracted, null, 2)}
            </pre>
          </div>
        )}
      </section>

      {/* ERROR */}
      {error && (
        <div
          style={{
            marginTop: 16,
            padding: 12,
            border: "1px solid #f2b8b5",
            background: "#fff5f5",
            borderRadius: 8,
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* SAVE RESULT PANEL */}
      {lastSavedResult && (
        <section style={{ marginTop: 22 }}>
          <h2 style={{ fontSize: 20, fontWeight: 650 }}>Last Save Result</h2>
          <div
            style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}
          >
            <div>
              <strong>SalesOrderId:</strong> {lastSavedResult.salesOrderId}
            </div>
            <div>
              <strong>Message:</strong> {lastSavedResult.message}
            </div>
            {lastSavedResult.filename && (
              <div>
                <strong>File:</strong> {lastSavedResult.filename}
              </div>
            )}

            <details style={{ marginTop: 12 }}>
              <summary style={{ cursor: "pointer" }}>
                View extracted JSON
              </summary>
              <pre style={{ ...preStyle, marginTop: 8 }}>
                {JSON.stringify(lastSavedResult.extracted, null, 2)}
              </pre>
            </details>
          </div>
        </section>
      )}
    </main>
  );
}

function btnStyle(disabled: boolean) {
  return {
    padding: "10px 14px",
    borderRadius: 8,
    border: "1px solid #ccc",
    background: disabled ? "#f5f5f5" : "white",
    cursor: disabled ? "not-allowed" : "pointer",
  } as const;
}

const preStyle = {
  whiteSpace: "pre-wrap",
  marginTop: 0,
  padding: 10,
  borderRadius: 8,
  border: "1px solid #eee",
  background: "#fafafa",
  fontSize: 12,
} as const;
