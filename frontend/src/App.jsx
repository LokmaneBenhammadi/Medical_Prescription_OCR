import { useEffect, useMemo, useState } from "react";

const apiBaseUrl = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [backendStatus, setBackendStatus] = useState("Checking backend...");

  const previewUrl = useMemo(() => {
    if (!selectedFile) {
      return "";
    }
    return URL.createObjectURL(selectedFile);
  }, [selectedFile]);

  useEffect(() => {
    let isMounted = true;

    async function pingBackend() {
      try {
        const response = await fetch(`${apiBaseUrl}/health`);
        const data = await response.json();
        if (isMounted) {
          setBackendStatus(data.status === "ok" ? "Backend is ready." : "Backend is not ready.");
        }
      } catch {
        if (isMounted) {
          setBackendStatus("Backend is unreachable. Start FastAPI on port 8000.");
        }
      }
    }

    void pingBackend();

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!selectedFile) {
      setError("Choose an image first.");
      setResult(null);
      return;
    }

    setError("");
    setResult(null);
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch(`${apiBaseUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed.");
      }

      setResult(data);
    } catch (submitError) {
      setError(submitError.message || "Prediction failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="page">
      <section className="panel">
        <div className="panel__header">
          <div>
            <p className="eyebrow">Local Demo</p>
            <h1>Medical Prescription OCR</h1>
            <p className="subtle">
              Upload a prescription image, run the fine-tuned model locally, and inspect the extracted text.
            </p>
          </div>
          <span className="status">{backendStatus}</span>
        </div>

        <form className="upload-form" onSubmit={handleSubmit}>
          <label className="file-input">
            <span>Select image</span>
            <input
              type="file"
              accept="image/*"
              onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
            />
          </label>

          <button className="primary-button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Running OCR..." : "Run OCR"}
          </button>
        </form>

        {error ? <div className="message message--error">{error}</div> : null}

        <div className="content-grid">
          <section className="card">
            <h2>Image Preview</h2>
            {previewUrl ? (
              <img className="preview-image" src={previewUrl} alt="Prescription preview" />
            ) : (
              <p className="empty-state">No image selected yet.</p>
            )}
          </section>

          <section className="card">
            <h2>OCR Output</h2>
            {result ? (
              <>
                <div className="metrics">
                  <span>File: {result.image_id}</span>
                  <span>Lines: {result.line_count}</span>
                  <span>Time: {result.processing_ms} ms</span>
                </div>

                <label className="result-label" htmlFor="rawText">
                  Raw text
                </label>
                <textarea id="rawText" readOnly value={result.raw_text} />

                <h3>Line by line</h3>
                <ol className="line-list">
                  {result.lines.map((line, index) => (
                    <li key={`${index}-${line}`}>{line || <em>(empty line)</em>}</li>
                  ))}
                </ol>
              </>
            ) : (
              <p className="empty-state">Prediction results will appear here.</p>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}

export default App;
