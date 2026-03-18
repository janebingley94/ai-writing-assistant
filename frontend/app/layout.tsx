import type { Metadata } from "next";
import { DM_Sans, Space_Grotesk } from "next/font/google";
import "./globals.css";

const displayFont = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-display",
});

const bodyFont = DM_Sans({
  subsets: ["latin"],
  variable: "--font-body",
});

export const metadata: Metadata = {
  title: "AI Writing Assistant",
  description: "Prompt-driven writing studio with streaming generation.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${displayFont.variable} ${bodyFont.variable}`}>
      <body className="font-body">
        <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#ffffff,_#f7f3ee_60%,_#efe7da)]">
          {children}
        </div>
      </body>
    </html>
  );
}
