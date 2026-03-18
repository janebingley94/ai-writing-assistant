"use client";

import { Select } from "@/components/ui/select";

interface ToneSelectorProps {
  value: string;
  options: { value: string; label: string }[];
  onChange: (value: string) => void;
}

export function ToneSelector({ value, options, onChange }: ToneSelectorProps) {
  return (
    <Select value={value} onChange={(event) => onChange(event.target.value)}>
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </Select>
  );
}
