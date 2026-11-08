import { notFound } from "next/navigation";
import Link from "next/link";
import type { Metadata } from "next";
import { Calendar, FileCode, ArrowLeft, ArrowRight } from "lucide-react";
import { getAllDocsMeta, getDocBySlug } from "@/lib/content";
import { DocsSidebar } from "@/components/DocsSidebar";

export async function generateStaticParams() {
  const docs = getAllDocsMeta();
  return docs.map((d) => ({ slug: d.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const doc = await getDocBySlug(slug);
  if (!doc) return { title: "Documentation Not Found" };
  return {
    title: doc.title,
    description: doc.description,
  };
}

export default async function DocArticlePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const allDocs = getAllDocsMeta();
  const doc = await getDocBySlug(slug);

  if (!doc) {
    notFound();
  }

  const currentIndex = allDocs.findIndex((d) => d.slug === slug);
  const prevDoc = currentIndex > 0 ? allDocs[currentIndex - 1] : null;
  const nextDoc =
    currentIndex >= 0 && currentIndex < allDocs.length - 1
      ? allDocs[currentIndex + 1]
      : null;

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-10 lg:flex-row">
        {/* Left Sidebar */}
        <DocsSidebar docs={allDocs} activeSlug={doc.slug} />

        {/* Center Article */}
        <article className="min-w-0 flex-1">
          <div className="liquid-glass rounded-2xl p-6 sm:p-10">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-6">
              <div>
                <div className="flex items-center gap-2 text-xs font-medium text-[#58a6ff]">
                  <span>{doc.category}</span>
                  <span className="text-white/30">·</span>
                  <span className="inline-flex items-center gap-1 text-[#9aa5be] tabular-nums">
                    <Calendar className="h-3.5 w-3.5" />
                    Updated {doc.updatedAt}
                  </span>
                </div>
                <h1 className="mt-2 text-2xl font-bold tracking-tight text-white sm:text-3xl">
                  {doc.title}
                </h1>
                <p className="mt-2 text-sm leading-relaxed text-[#b4bcd0]">
                  {doc.description}
                </p>
              </div>
            </div>

            {/* Rendered Markdown HTML */}
            <div
              className="enerco-prose mt-6"
              dangerouslySetInnerHTML={{ __html: doc.html }}
            />

            {/* Source File Hint for Easy Editing */}
            <div className="mt-10 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-xs text-[#9aa5be]">
              <div className="flex items-center gap-2">
                <FileCode className="h-4 w-4 text-[#58a6ff]" />
                <span>
                  Source file:{" "}
                  <code className="rounded bg-white/10 px-1.5 py-0.5 font-mono text-white">
                    web/content/docs/{doc.slug}.md
                  </code>
                </span>
              </div>
              <span>Documentation guides are statically compiled at build time</span>
            </div>

            {/* Prev / Next Navigation */}
            <div className="mt-8 grid grid-cols-1 gap-4 border-t border-white/10 pt-6 sm:grid-cols-2">
              {prevDoc ? (
                <Link
                  href={`/docs/${prevDoc.slug}`}
                  className="group flex flex-col rounded-xl border border-white/10 bg-white/[0.03] p-4 transition hover:border-[#58a6ff]/50"
                >
                  <span className="inline-flex items-center gap-1 text-xs text-[#8ea0c0]">
                    <ArrowLeft className="h-3.5 w-3.5 transition group-hover:-translate-x-0.5" />
                    Previous Guide
                  </span>
                  <span className="mt-1 text-sm font-semibold text-white">
                    {prevDoc.title}
                  </span>
                </Link>
              ) : (
                <div />
              )}

              {nextDoc ? (
                <Link
                  href={`/docs/${nextDoc.slug}`}
                  className="group flex flex-col items-end text-right rounded-xl border border-white/10 bg-white/[0.03] p-4 transition hover:border-[#58a6ff]/50"
                >
                  <span className="inline-flex items-center gap-1 text-xs text-[#8ea0c0]">
                    Next Guide
                    <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                  </span>
                  <span className="mt-1 text-sm font-semibold text-white">
                    {nextDoc.title}
                  </span>
                </Link>
              ) : (
                <div />
              )}
            </div>
          </div>
        </article>

        {/* Right Table of Contents */}
        {doc.headings.length > 0 && (
          <aside className="hidden xl:block xl:w-56 xl:shrink-0">
            <div className="sticky top-22 rounded-xl border border-white/10 bg-white/[0.03] p-4">
              <div className="text-xs font-semibold uppercase tracking-wider text-white">
                On This Page
              </div>
              <ul className="mt-3 space-y-2 text-xs">
                {doc.headings.map((h) => (
                  <li
                    key={h.id}
                    className={h.level === 3 ? "pl-3" : ""}
                  >
                    <a
                      href={`#${h.id}`}
                      className="block text-[#9aa5be] transition hover:text-white leading-snug"
                    >
                      {h.text}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
}
