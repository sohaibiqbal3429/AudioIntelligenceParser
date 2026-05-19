"use client";

import { FormEvent, useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string>("No result yet.");
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setResult("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("audio", file);
    setIsLoading(true);
    setResult("Processing...");

    try {
      const response = await fetch(`${API_BASE_URL}/upload-audio`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setResult(`Error: ${data.detail || "Unknown error"}`);
        return;
      }

      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      setResult(`Request failed: ${String(error)}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>Audio Intelligence Parser</h1>
      <p className="muted">
        Upload an audio file from this Next.js frontend. Backend will transcribe it with local Whisper and
        extract name, email, age, gender, and phone using OpenAI.
      </p>

      <div className="card">
        <form onSubmit={onSubmit}>
          <div className="row">
            <input
              type="file"
              accept=".mp3,.wav,.m4a"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              required
            />
          </div>
          <button type="submit" disabled={isLoading}>
            {isLoading ? "Processing..." : "Upload & Process"}
          </button>
        </form>
      </div>

      <h2>Result</h2>
      <pre>{result}</pre>
    </main>
  );
}
