import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { remark } from "remark";
import remarkGfm from "remark-gfm";
import remarkHtml from "remark-html";

export interface DocHeading {
  id: string;
  text: string;
  level: 2 | 3;
}

export interface DocMeta {
  slug: string;
  title: string;
  description: string;
  category: string;
  order: number;
  updatedAt: string;
}

export interface DocArticle extends DocMeta {
  content: string;
  html: string;
  headings: DocHeading[];
}

export interface ReleaseItem {
  slug: string;
  version: string;
  codename: string;
  date: string;
  channel: string;
  isoFilename: string;
  isoUrl: string;
  isoSize: string;
  sha256: string;
  kernel: string;
  installer: string;
  shell: string;
  content: string;
  html: string;
}

const CONTENT_ROOT = path.join(process.cwd(), "content");
const DOCS_DIR = path.join(CONTENT_ROOT, "docs");
const RELEASES_DIR = path.join(CONTENT_ROOT, "releases");

function slugifyHeading(text: string): string {
  return text
    .toLowerCase()
    .replace(/[`*_~()[\]]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function injectHeadingIds(html: string): { html: string; headings: DocHeading[] } {
  const headings: DocHeading[] = [];
  const processed = html.replace(/<h([23])>(.*?)<\/h\1>/g, (_match, levelStr, innerHtml) => {
    const plainText = innerHtml.replace(/<[^>]+>/g, "").trim();
    const id = slugifyHeading(plainText);
    const level = Number(levelStr) as 2 | 3;
    headings.push({ id, text: plainText, level });
    return `<h${level} id="${id}">${innerHtml}</h${level}>`;
  });
  return { html: processed, headings };
}

async function renderMarkdown(markdown: string): Promise<{ html: string; headings: DocHeading[] }> {
  const result = await remark().use(remarkGfm).use(remarkHtml, { sanitize: false }).process(markdown);
  return injectHeadingIds(result.toString());
}

export function getAllDocsMeta(): DocMeta[] {
  if (!fs.existsSync(DOCS_DIR)) return [];
  const files = fs.readdirSync(DOCS_DIR).filter((f) => f.endsWith(".md"));

  const docs = files.map((file) => {
    const slug = file.replace(/\.md$/, "");
    const raw = fs.readFileSync(path.join(DOCS_DIR, file), "utf8");
    const { data } = matter(raw);
    return {
      slug,
      title: String(data.title || slug),
      description: String(data.description || ""),
      category: String(data.category || "General"),
      order: Number(data.order ?? 99),
      updatedAt: String(data.updatedAt || "2026-11-07"),
    };
  });

  return docs.sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
}

export async function getDocBySlug(slug: string): Promise<DocArticle | null> {
  const fullPath = path.join(DOCS_DIR, `${slug}.md`);
  if (!fs.existsSync(fullPath)) return null;

  const raw = fs.readFileSync(fullPath, "utf8");
  const { data, content } = matter(raw);
  const { html, headings } = await renderMarkdown(content);

  return {
    slug,
    title: String(data.title || slug),
    description: String(data.description || ""),
    category: String(data.category || "General"),
    order: Number(data.order ?? 99),
    updatedAt: String(data.updatedAt || "2026-11-07"),
    content,
    html,
    headings,
  };
}

export async function getAllReleases(): Promise<ReleaseItem[]> {
  if (!fs.existsSync(RELEASES_DIR)) return [];
  const files = fs.readdirSync(RELEASES_DIR).filter((f) => f.endsWith(".md"));

  const releases = await Promise.all(
    files.map(async (file) => {
      const slug = file.replace(/\.md$/, "");
      const raw = fs.readFileSync(path.join(RELEASES_DIR, file), "utf8");
      const { data, content } = matter(raw);
      const { html } = await renderMarkdown(content);

      return {
        slug,
        version: String(data.version || slug),
        codename: String(data.codename || "Enterprise Workstation"),
        date: String(data.date || "2026-11-07"),
        channel: String(data.channel || "Stable"),
        isoFilename: String(data.isoFilename || `enercoos-${slug}-x86_64.iso`),
        isoUrl: String(data.isoUrl || `/downloads/enercoos-${slug}-x86_64.iso`),
        isoSize: String(data.isoSize || "2.8 GB"),
        sha256: String(data.sha256 || ""),
        kernel: String(data.kernel || "Linux Zen + Linux"),
        installer: String(data.installer || "Calamares 3.3.11"),
        shell: String(data.shell || "MacShell + Hyprland"),
        content,
        html,
      };
    })
  );

  return releases.sort((a, b) => b.version.localeCompare(a.version));
}
