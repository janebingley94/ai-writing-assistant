import Link from "next/link";
import { BlogGenerator } from "@/components/writing/BlogGenerator";

export default function BlogPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-10 px-6 py-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-amber-600">
            Writing Suite
          </p>
          <h1 className="font-display text-3xl font-semibold text-slate-900">
            Blog Generator
          </h1>
        </div>
        <Link href="/" className="text-sm text-slate-500 underline">
          Back to Home
        </Link>
      </div>
      <BlogGenerator />
    </main>
  );
}
