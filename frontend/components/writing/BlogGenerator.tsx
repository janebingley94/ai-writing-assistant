"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { readSSE } from "@/lib/stream";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { OutputEditor } from "@/components/writing/OutputEditor";
import { OutputActions } from "@/components/writing/OutputActions";
import { OutlinePreview } from "@/components/writing/OutlinePreview";
import { PromptVariables } from "@/components/writing/PromptVariables";
import type { BlogGenerateRequest, GenerationResponse } from "@/types/writing";

const toneOptions = [
  { value: "professional", label: "Professional" },
  { value: "casual", label: "Casual" },
  { value: "academic", label: "Academic" },
  { value: "creative", label: "Creative" },
];

const lengthOptions = [
  { value: "short", label: "Short" },
  { value: "medium", label: "Medium" },
  { value: "long", label: "Long" },
];

export function BlogGenerator() {
  const [form, setForm] = useState<BlogGenerateRequest>({
    topic: "",
    keywords: [],
    tone: "professional",
    length: "medium",
    language: "zh",
    outline_first: true,
  });
  const [outline, setOutline] = useState<unknown>(null);
  const [output, setOutput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const handleGenerate = async () => {
    setIsStreaming(true);
    setOutput("");
    setOutline(null);

    if (form.outline_first) {
      const outlineResponse = await api.post<GenerationResponse>("/generate/blog", form);
      setOutline(outlineResponse.metadata?.outline ?? null);
    }

    const streamPayload = { ...form, outline_first: false };
    const response = await api.streamPost("/generate/stream/blog", streamPayload);
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
            Blog Generator
          </h2>
          <p className="text-sm text-slate-500">
            Generate long-form blog posts with outline preview.
          </p>
        </div>
        <Input
          placeholder="Topic"
          value={form.topic}
          onChange={(event) => setForm({ ...form, topic: event.target.value })}
        />
        <PromptVariables
          label="Keywords"
          values={form.keywords}
          onChange={(values) => setForm({ ...form, keywords: values })}
        />
        <div className="grid gap-3 md:grid-cols-2">
          <Select
            value={form.tone}
            onChange={(event) => setForm({ ...form, tone: event.target.value as BlogGenerateRequest["tone"] })}
          >
            {toneOptions.map((tone) => (
              <option key={tone.value} value={tone.value}>
                {tone.label}
              </option>
            ))}
          </Select>
          <Select
            value={form.length}
            onChange={(event) => setForm({ ...form, length: event.target.value as BlogGenerateRequest["length"] })}
          >
            {lengthOptions.map((length) => (
              <option key={length.value} value={length.value}>
                {length.label}
              </option>
            ))}
          </Select>
        </div>
        <Input
          placeholder="Language (default zh)"
          value={form.language}
          onChange={(event) => setForm({ ...form, language: event.target.value })}
        />
        <label className="flex items-center gap-2 text-sm text-slate-600">
          <input
            type="checkbox"
            checked={form.outline_first}
            onChange={(event) =>
              setForm({ ...form, outline_first: event.target.checked })
            }
          />
          Generate outline preview first
        </label>
        <Button onClick={handleGenerate} disabled={!form.topic || isStreaming}>
          {isStreaming ? "Generating..." : "Generate Blog"}
        </Button>
      </div>

      <div className="space-y-5">
        <OutlinePreview outline={outline} />
        <OutputEditor value={output} onChange={setOutput} />
        <OutputActions content={output} filename="blog.md" />
      </div>
    </div>
  );
}
