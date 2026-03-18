"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { readSSE } from "@/lib/stream";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { OutputEditor } from "@/components/writing/OutputEditor";
import { OutputActions } from "@/components/writing/OutputActions";
import type { SummaryRequest } from "@/types/writing";

const summaryOptions = [
  { value: "bullet_points", label: "Bullet Points" },
  { value: "paragraph", label: "Paragraph" },
  { value: "tldr", label: "TL;DR" },
  { value: "executive", label: "Executive" },
];

export function SummaryTool() {
  const [form, setForm] = useState<SummaryRequest>({
    content: "",
    summary_type: "paragraph",
    max_length: 300,
    language: "zh",
  });
  const [output, setOutput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const handleGenerate = async () => {
    setIsStreaming(true);
    setOutput("");
    const response = await api.streamPost("/generate/stream/summary", form);
    await readSSE(response, (token) => {
      setOutput((prev) => prev + token);
    });
    setIsStreaming(false);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
      <div className="space-y-5 rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-glass">
        <div>
          <h2 className="font-display text-xl font-semibold text-slate-900">
            Summary Tool
          </h2>
          <p className="text-sm text-slate-500">
            Summarize long-form content with streaming output.
          </p>
        </div>
        <Select
          value={form.summary_type}
          onChange={(event) =>
            setForm({ ...form, summary_type: event.target.value as SummaryRequest["summary_type"] })
          }
        >
          {summaryOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
        <Textarea
          placeholder="Paste content to summarize..."
          value={form.content}
          onChange={(event) => setForm({ ...form, content: event.target.value })}
          rows={8}
        />
        <div className="grid gap-3 md:grid-cols-2">
          <Input
            type="number"
            value={form.max_length}
            onChange={(event) =>
              setForm({ ...form, max_length: Number(event.target.value) })
            }
            placeholder="Max length"
          />
          <Input
            value={form.language}
            onChange={(event) => setForm({ ...form, language: event.target.value })}
            placeholder="Language"
          />
        </div>
        <Button onClick={handleGenerate} disabled={!form.content || isStreaming}>
          {isStreaming ? "Summarizing..." : "Generate Summary"}
        </Button>
      </div>
      <div className="space-y-5">
        <OutputEditor value={output} onChange={setOutput} />
        <OutputActions content={output} filename="summary.md" />
      </div>
    </div>
  );
}
