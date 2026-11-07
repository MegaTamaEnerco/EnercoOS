"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Search, FileText } from "lucide-react";
import type { DocMeta } from "@/lib/content";

export function DocsSidebar({
  docs,
  activeSlug,
}: {
  docs: DocMeta[];
  activeSlug: string;
}) {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return docs;
    return docs.filter(
      (d) =>
        d.title.toLowerCase().includes(q) ||
        d.description.toLowerCase().includes(q) ||
        d.category.toLowerCase().includes(q)
    );
  }, [docs, query]);

  const grouped = useMemo(() => {
    const map = new Map<string, DocMeta[]>();
    for (const d of filtered) {
      const list = map.get(d.category) ?? [];
      list.push(d);
      map.set(d.category, list);
    }
    return Array.from(map.entries());
  }, [filtered]);

  return (
    <aside className="w-full lg:w-64 lg:shrink-0">
      <div className="sticky top-22 space-y-6">
        {/* Search Input */}
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-[#7f8aa3]" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Filter docs..."
            aria-label="Filter documentation"
            className="w-full rounded-xl border border-white/12 bg-white/[0.04] py-2 pl-9 pr-3 text-xs text-white placeholder-[#7f8aa3] outline-none transition focus:border-[#58a6ff]"
          />
        </div>

        {/* Grouped Navigation */}
        <nav aria-label="Documentation Sidebar" className="space-y-5">
          {grouped.length === 0 ? (
            <p className="px-2 text-xs text-[#7f8aa3]">No matching guides found.</p>
          ) : (
            grouped.map(([category, items]) => (
              <div key={category}>
                <div className="px-2.5 text-[11px] font-semibold uppercase tracking-wider text-[#8ea0c0]">
                  {category}
                </div>
                <ul className="mt-1.5 space-y-1">
                  {items.map((doc) => {
                    const isActive = doc.slug === activeSlug;
                    return (
                      <li key={doc.slug}>
                        <Link
                          href={`/docs/${doc.slug}`}
                          className={`flex items-center gap-2 rounded-lg px-2.5 py-2 text-xs font-medium transition ${
                            isActive
                              ? "bg-[#0071e3] text-white shadow-sm"
                              : "text-[#b4bcd0] hover:bg-white/[0.06] hover:text-white"
                          }`}
                        >
                          <FileText
                            className={`h-3.5 w-3.5 shrink-0 ${
                              isActive ? "text-white" : "text-[#58a6ff]"
                            }`}
                          />
                          <span className="truncate">{doc.title}</span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))
          )}
        </nav>
      </div>
    </aside>
  );
}
