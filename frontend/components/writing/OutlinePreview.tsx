"use client";

interface OutlinePreviewProps {
  outline: unknown;
}

export function OutlinePreview({ outline }: OutlinePreviewProps) {
  if (!outline) return null;
  return (
    <div className="rounded-3xl border border-slate-200 bg-white/90 p-4 shadow-glass">
      <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
        Outline Preview
      </div>
      <pre className="mt-3 whitespace-pre-wrap text-xs text-slate-700">
        {JSON.stringify(outline, null, 2)}
      </pre>
    </div>
  );
}
