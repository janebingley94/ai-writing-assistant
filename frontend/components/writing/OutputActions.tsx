"use client";

import { Button } from "@/components/ui/button";

interface OutputActionsProps {
  content: string;
  filename: string;
}

export function OutputActions({ content, filename }: OutputActionsProps) {
  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex items-center gap-2">
      <Button variant="outline" onClick={handleCopy}>
        Copy
      </Button>
      <Button variant="outline" onClick={handleDownload}>
        Download
      </Button>
    </div>
  );
}
