import Link from "next/link";
import { Card } from "@/components/ui/card";

const cards = [
  {
    title: "Blog Generator",
    description: "Outline-driven long-form articles with structured flow.",
    href: "/write/blog",
  },
  {
    title: "Email Generator",
    description: "Structured email drafts with JSON output and editing.",
    href: "/write/email",
  },
  {
    title: "Summary Tool",
    description: "Streamed summaries for long documents and notes.",
    href: "/write/summary",
  },
  {
    title: "SEO Article",
    description: "Keyword-focused SEO content with streaming output.",
    href: "/write/seo",
  },
];

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-10 px-6 py-16">
      <header className="space-y-3">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-amber-600">
          Prompt Studio
        </p>
        <h1 className="font-display text-4xl font-semibold text-slate-900">
          AI Writing Assistant
        </h1>
        <p className="max-w-2xl text-sm text-slate-600">
          Build production-grade writing workflows with prompt templates, streaming
          output, and structured edits.
        </p>
      </header>

      <section className="grid gap-6 md:grid-cols-2">
        {cards.map((card) => (
          <Link key={card.href} href={card.href} className="group">
            <Card className="card-glow transition group-hover:-translate-y-1">
              <h2 className="font-display text-xl font-semibold text-slate-900">
                {card.title}
              </h2>
              <p className="mt-2 text-sm text-slate-600">{card.description}</p>
              <div className="mt-6 text-sm font-semibold text-amber-600">
                Launch →
              </div>
            </Card>
          </Link>
        ))}
      </section>
    </main>
  );
}
