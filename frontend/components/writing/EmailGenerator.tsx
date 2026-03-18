"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { OutputEditor } from "@/components/writing/OutputEditor";
import { OutputActions } from "@/components/writing/OutputActions";
import type { EmailGenerateRequest, GenerationResponse } from "@/types/writing";

const emailTypeOptions = [
  { value: "business", label: "Business" },
  { value: "follow_up", label: "Follow Up" },
  { value: "introduction", label: "Introduction" },
  { value: "complaint", label: "Complaint" },
  { value: "thank_you", label: "Thank You" },
];

const toneOptions = [
  { value: "formal", label: "Formal" },
  { value: "friendly", label: "Friendly" },
  { value: "urgent", label: "Urgent" },
];

export function EmailGenerator() {
  const [form, setForm] = useState<EmailGenerateRequest>({
    email_type: "business",
    recipient_name: "",
    sender_name: "",
    context: "",
    tone: "formal",
    language: "zh",
  });
  const [output, setOutput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    setIsLoading(true);
    const response = await api.post<GenerationResponse>("/generate/email", form);
    setOutput(response.content);
    setIsLoading(false);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
      <div className="space-y-5 rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-glass">
        <div>
          <h2 className="font-display text-xl font-semibold text-slate-900">
            Email Generator
          </h2>
          <p className="text-sm text-slate-500">
            Generate structured email drafts with JSON output.
          </p>
        </div>
        <Select
          value={form.email_type}
          onChange={(event) =>
            setForm({ ...form, email_type: event.target.value as EmailGenerateRequest["email_type"] })
          }
        >
          {emailTypeOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
        <div className="grid gap-3 md:grid-cols-2">
          <Input
            placeholder="Recipient"
            value={form.recipient_name ?? ""}
            onChange={(event) =>
              setForm({ ...form, recipient_name: event.target.value })
            }
          />
          <Input
            placeholder="Sender"
            value={form.sender_name ?? ""}
            onChange={(event) => setForm({ ...form, sender_name: event.target.value })}
          />
        </div>
        <Select
          value={form.tone}
          onChange={(event) =>
            setForm({ ...form, tone: event.target.value as EmailGenerateRequest["tone"] })
          }
        >
          {toneOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
        <Textarea
          placeholder="Context"
          value={form.context}
          onChange={(event) => setForm({ ...form, context: event.target.value })}
          rows={5}
        />
        <Input
          placeholder="Language"
          value={form.language}
          onChange={(event) => setForm({ ...form, language: event.target.value })}
        />
        <Button onClick={handleGenerate} disabled={!form.context || isLoading}>
          {isLoading ? "Generating..." : "Generate Email"}
        </Button>
      </div>
      <div className="space-y-5">
        <OutputEditor value={output} onChange={setOutput} language="json" />
        <OutputActions content={output} filename="email.json" />
      </div>
    </div>
  );
}
