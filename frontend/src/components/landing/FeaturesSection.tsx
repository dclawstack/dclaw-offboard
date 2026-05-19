"use client";

import Link from "next/link";
import {
  Bot,
  ClipboardCheck,
  Package,
  ShieldOff,
  MessageSquare,
  BookOpen,
  Users,
  Calculator,
  ArrowRight,
} from "lucide-react";
import content from "@/data/landing-content.json";

const iconMap: Record<string, React.ElementType> = {
  Bot,
  ClipboardCheck,
  Package,
  ShieldOff,
  MessageSquare,
  BookOpen,
  Users,
  Calculator,
};

export default function FeaturesSection() {
  return (
    <section id="features" className="py-20 sm:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
            Everything You Need for Compliant Offboarding
          </h2>
          <p className="mt-4 text-lg text-gray-500">
            From AI-guided workflows to compliance automation — all in one platform.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {content.features.map((feature) => {
            const Icon = iconMap[feature.icon] || Bot;
            return (
              <Link
                key={feature.id}
                href={feature.href}
                className="group relative p-6 rounded-2xl border border-gray-100 bg-white hover:border-gray-200 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center justify-between mb-4">
                  <div
                    className="w-11 h-11 rounded-xl flex items-center justify-center"
                    style={{ backgroundColor: feature.color + "15" }}
                  >
                    <Icon className="w-5 h-5" style={{ color: feature.color }} />
                  </div>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full" style={{ backgroundColor: feature.color + "15", color: feature.color }}>
                    {feature.priority}
                  </span>
                </div>

                <h3 className="text-base font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm text-gray-500 leading-relaxed">
                  {feature.description}
                </p>

                <div className="mt-4 flex items-center gap-1 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity" style={{ color: feature.color }}>
                  Explore <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}
