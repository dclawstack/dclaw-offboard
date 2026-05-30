"use client";

import Link from "next/link";
import { ArrowLeft, BookOpen, Github, FileCode } from "lucide-react";

const sections = [
  {
    title: "Getting Started",
    description: "Run the stack locally with docker-compose; the README walks through env setup.",
    href: "https://github.com/anthropics/claude-code",
    icon: BookOpen,
  },
  {
    title: "API Reference",
    description: "OpenAPI spec served by the FastAPI backend.",
    href: "/api/docs",
    icon: FileCode,
  },
  {
    title: "Source",
    description: "Browse the monorepo on GitHub.",
    href: "https://github.com/",
    icon: Github,
  },
];

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to home
        </Link>

        <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">Documentation</h1>
        <p className="text-lg text-gray-500 mb-10">
          Guides, references, and source links for the DClaw Offboard platform.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {sections.map((s) => {
            const Icon = s.icon;
            return (
              <Link
                key={s.title}
                href={s.href}
                className="group flex flex-col p-6 rounded-2xl bg-white border border-gray-100 hover:border-gray-200 hover:shadow-xl transition-all"
              >
                <div className="w-11 h-11 rounded-xl bg-indigo-50 flex items-center justify-center mb-4">
                  <Icon className="w-5 h-5 text-indigo-600" />
                </div>
                <h2 className="text-base font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors mb-1">
                  {s.title}
                </h2>
                <p className="text-sm text-gray-500">{s.description}</p>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
