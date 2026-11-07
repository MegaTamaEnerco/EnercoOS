"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";

export function CopyButton({ text, label = "Copy" }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      // Fallback ignored
    }
  };

  return (
    <button
      type="button"
      onClick={handleCopy}
      className="inline-flex items-center gap-1.5 rounded-md border border-white/12 bg-white/[0.05] px-2.5 py-1 text-xs font-medium text-[#d5ddf0] transition hover:border-white/25 hover:bg-white/[0.1] hover:text-white cursor-pointer"
    >
      {copied ? (
        <>
          <Check className="h-3.5 w-3.5 text-emerald-400" />
          <span className="text-emerald-300">Copied</span>
        </>
      ) : (
        <>
          <Copy className="h-3.5 w-3.5 text-[#8ea0c0]" />
          <span>{label}</span>
        </>
      )}
    </button>
  );
}
