"use client";

import Link from "next/link";
import { ArrowRight, MessageSquare } from "lucide-react";
import content from "@/data/landing-content.json";

export default function HeroSection() {
  const { hero, app } = content;

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-white via-indigo-50/30 to-white">
      <div className="absolute inset-0 bg-grid-pattern opacity-[0.03]" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28 lg:py-36">
        <div className="max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 shadow-sm mb-8">
            <span className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: app.color }} />
            <span className="text-sm text-gray-600">AI-Powered Offboarding Platform</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-gray-900 leading-[1.1]">
            {hero.headline}
          </h1>
          <p className="mt-6 text-lg sm:text-xl text-gray-500 leading-relaxed max-w-2xl mx-auto">
            {hero.subheadline}
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href={hero.ctaPrimary.href}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl text-white font-semibold text-base shadow-lg hover:shadow-xl transition-all hover:-translate-y-0.5 flex items-center justify-center gap-2"
              style={{ backgroundColor: app.color }}
            >
              {hero.ctaPrimary.text}
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href={hero.ctaSecondary.href}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl border-2 border-gray-200 text-gray-700 font-semibold text-base hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center justify-center gap-2"
            >
              <MessageSquare className="w-4 h-4" />
              {hero.ctaSecondary.text}
            </Link>
          </div>

          <div className="mt-16 grid grid-cols-3 gap-8 max-w-lg mx-auto">
            {hero.stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-2xl sm:text-3xl font-bold text-gray-900">{stat.value}</div>
                <div className="text-xs sm:text-sm text-gray-500 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
