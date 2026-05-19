import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Audio Intelligence Parser",
  description: "Upload audio, transcribe with Whisper, extract details with OpenAI",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
