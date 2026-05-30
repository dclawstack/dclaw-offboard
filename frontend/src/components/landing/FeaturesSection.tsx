"use client";

import Link from "next/link";
import {
  Bot,
  ClipboardCheck,
  ShieldOff,
  AlertTriangle,
  MessageSquare,
  BrainCircuit,
  Blocks,
  Users,
  Scale,
  Activity,
  UsersRound,
  Landmark,
  ArrowRight,
  Check,
} from "lucide-react";
import content from "@/data/landing-content.json";

const iconMap: Record<string, React.ElementType> = {
  Bot,
  ClipboardCheck,
  ShieldOff,
  AlertTriangle,
  MessageSquare,
  BrainCircuit,
  Blocks,
  Users,
  Scale,
  Activity,
  UsersRound,
  Landmark,
};

const tierMeta: Record<string, { bg: string; border: string; badge: string; badgeText: string }> = {
  P0: {
    bg: "bg-indigo-50",
    border: "border-indigo-100",
    badge: "bg-indigo-100 text-indigo-700",
    badgeText: "Core Platform",
  },
  P1: {
    bg: "bg-violet-50",
    border: "border-violet-100",
    badge: "bg-violet-100 text-violet-700",
    badgeText: "AI-Powered",
  },
  P2: {
    bg: "bg-emerald-50",
    border: "border-emerald-100",
    badge: "bg-emerald-100 text-emerald-700",
    badgeText: "Enterprise",
  },
};

type Feature = {
  id: string;
  tier: string;
  title: string;
  description: string;
  bullets: string[];
  icon: string;
  href: string;
  priority: string;
  color: string;
};

function FeatureCard({ feature }: { feature: Feature }) {
  const Icon = iconMap[feature.icon] || Bot;
  const meta = tierMeta[feature.tier] || tierMeta["P2"];

  return (
    <Link
      href={feature.href}
      className="group flex flex-col p-6 rounded-2xl bg-white border border-gray-100 hover:border-gray-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
    >
      <div className="flex items-start justify-between mb-4">
        <div
          className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0"
          style={{ backgroundColor: feature.color + "18" }}
        >
          <Icon className="w-5 h-5" style={{ color: feature.color }} />
        </div>
        <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${meta.badge}`}>
          {meta.badgeText}
        </span>
      </div>

      <h3 className="text-base font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors mb-2">
        {feature.title}
      </h3>
      <p className="text-sm text-gray-500 leading-relaxed mb-4">
        {feature.description}
      </p>

      <ul className="space-y-2 mt-auto">
        {feature.bullets.map((bullet) => (
          <li key={bullet} className="flex items-start gap-2 text-sm text-gray-600">
            <Check className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" style={{ color: feature.color }} />
            <span>{bullet}</span>
          </li>
        ))}
      </ul>

      <div
        className="mt-5 flex items-center gap-1 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity"
        style={{ color: feature.color }}
      >
        Explore feature <ArrowRight className="w-3.5 h-3.5" />
      </div>
    </Link>
  );
}

export default function FeaturesSection() {
  const tiers = content.featureTiers as { tier: string; label: string; description: string }[];
  const features = content.features as Feature[];

  return (
    <section id="features" className="py-20 sm:py-28 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Section header */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <span className="inline-block text-xs font-bold uppercase tracking-widest text-indigo-500 mb-3">
            Platform Features
          </span>
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
            Everything You Need for Compliant Offboarding
          </h2>
          <p className="mt-4 text-lg text-gray-500">
            12 production-ready features across three capability tiers — from core workflows to AI-powered enterprise intelligence.
          </p>
        </div>

        {/* Tier groups */}
        {tiers.map((tierDef) => {
          const tierFeatures = features.filter((f) => f.tier === tierDef.tier);
          const meta = tierMeta[tierDef.tier] || tierMeta["P2"];

          return (
            <div key={tierDef.tier} className="mb-20 last:mb-0">
              {/* Tier header */}
              <div className={`flex flex-col sm:flex-row sm:items-center gap-3 mb-8 pb-6 border-b ${meta.border}`}>
                <span className={`self-start text-xs font-bold uppercase tracking-widest px-3 py-1.5 rounded-full ${meta.badge}`}>
                  {tierDef.tier} — {tierDef.label}
                </span>
                <p className="text-sm text-gray-500">{tierDef.description}</p>
                <span className="sm:ml-auto text-xs text-gray-400 font-medium flex-shrink-0">
                  {tierFeatures.length} feature{tierFeatures.length !== 1 ? "s" : ""}
                </span>
              </div>

              {/* Feature cards grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {tierFeatures.map((feature) => (
                  <FeatureCard key={feature.id} feature={feature} />
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
