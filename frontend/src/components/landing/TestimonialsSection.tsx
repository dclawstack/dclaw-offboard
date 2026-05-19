"use client";

import { Quote } from "lucide-react";
import content from "@/data/landing-content.json";

export default function TestimonialsSection() {
  return (
    <section className="py-20 sm:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {content.testimonials.map((t) => (
            <div key={t.author} className="relative p-8 rounded-2xl bg-gray-50 border border-gray-100">
              <Quote className="w-8 h-8 text-indigo-200 mb-4" />
              <blockquote className="text-lg text-gray-700 leading-relaxed mb-6">
                &ldquo;{t.quote}&rdquo;
              </blockquote>
              <div>
                <div className="font-semibold text-gray-900">{t.author}</div>
                <div className="text-sm text-gray-500">{t.role}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
