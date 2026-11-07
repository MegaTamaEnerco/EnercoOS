import { redirect } from "next/navigation";
import { getAllDocsMeta } from "@/lib/content";

export default function DocsIndexPage() {
  const docs = getAllDocsMeta();
  const firstSlug = docs[0]?.slug ?? "getting-started";
  redirect(`/docs/${firstSlug}`);
}
