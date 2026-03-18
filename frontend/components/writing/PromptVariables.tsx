"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface PromptVariablesProps {
  label: string;
  values: string[];
  onChange: (values: string[]) => void;
}

export function PromptVariables({ label, values, onChange }: PromptVariablesProps) {
  const [draft, setDraft] = useState("");

  const addValue = () => {
    const next = draft.trim();
    if (!next) return;
    onChange([...values, next]);
    setDraft("");
  };

  return (
    <div className="space-y-2">
      <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
        {label}
      </div>
      <div className="flex gap-2">
        <Input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="输入后回车添加"
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              addValue();
            }
          }}
        />
        <Button type="button" onClick={addValue}>
          Add
        </Button>
      </div>
      {values.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {values.map((item, index) => (
            <button
              key={`${item}-${index}`}
              type="button"
              className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-600"
              onClick={() => {
                onChange(values.filter((_, idx) => idx !== index));
              }}
            >
              {item} ×
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
