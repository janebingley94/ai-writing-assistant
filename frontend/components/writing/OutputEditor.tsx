"use client";

import dynamic from "next/dynamic";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

interface OutputEditorProps {
  value: string;
  onChange?: (value: string) => void;
  height?: number;
  language?: string;
}

export function OutputEditor({
  value,
  onChange,
  height = 420,
  language = "markdown",
}: OutputEditorProps) {
  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white/90 shadow-glass">
      <MonacoEditor
        height={height}
        language={language}
        value={value}
        onChange={(val) => onChange?.(val ?? "")}
        options={{
          minimap: { enabled: false },
          wordWrap: "on",
          fontSize: 14,
          fontFamily: "var(--font-body)",
          padding: { top: 16, bottom: 16 },
        }}
      />
    </div>
  );
}
