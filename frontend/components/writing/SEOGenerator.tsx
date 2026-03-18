"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { readSSE } from "@/lib/stream";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { OutputEditor } from "@/components/writing/OutputEditor";
import { OutputActions } from "@/components/writing/OutputActions";
import { PromptVariables } from "@/components/writing/PromptVariables";
import type { SEOArticleRequest } from "@/types/writing";

export function SEOGenerator() {
  const [form, setForm] = useState<SEOArticleRequest>({
    keyword: "",
    secondary_keywords: [],
    word_count: 1500,
    target_audience: "general",
    include_faq: true,
    language: "zh",
  });
  const [output, setOutput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const handleGenerate = async () => {
    setIsStreaming(true);
    setOutput("");
    const response = await api.streamPost("/generate/stream/seo", form);
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
            SEO Article Generator
          </h2>
          <p className="text-sm text-slate-500">
            Generate SEO content with keyword focus.
          </p>
        </div>
        <Input
          placeholder="Primary keyword"
          value={form.keyword}
          onChange={(event) => setForm({ ...form, keyword: event.target.value })}
        />
        <PromptVariables
          label="Secondary Keywords"
          values={form.secondary_keywords}
          onChange={(values) => setForm({ ...form, secondary_keywords: values })}
        />
        <Input
          type="number"
          placeholder="Word count"
          value={form.word_count}
          onChange={(event) =>
            setForm({ ...form, word_count: Number(event.target.value) })
          }
        />
        <Textarea
          placeholder="Target audience"
          value={form.target_audience}
          onChange={(event) => setForm({ ...form, target_audience: event.target.value })}
        />
        <Input
          placeholder="Language"
          value={form.language}
          onChange={(event) => setForm({ ...form, language: event.target.value })}
        />
        <label className="flex items-center gap-2 text-sm text-slate-600">
          <input
            type="checkbox"
            checked={form.include_faq}
            onChange={(event) =>
              setForm({ ...form, include_faq: event.target.checked })
            }
          />
          Include FAQ section
        </label>
        <Button onClick={handleGenerate} disabled={!form.keyword || isStreaming}>
          {isStreaming ? "Generating..." : "Generate SEO Article"}
        </Button>
      </div>
      <div className="space-y-5">
        <OutputEditor value={output} onChange={setOutput} />
        <OutputActions content={output} filename="seo.md" />
      </div>
    </div>
  );
}
