"use client";

import Link from "next/link";
import { MessageSquare } from "lucide-react";
import content from "@/data/landing-content.json";

export default function CTASection() {
  return (
    <section className="py-20 sm:py-28">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div
          className="rounded-3xl p-10 sm:p-16 text-center text-white relative overflow-hidden"
          style={{ backgroundColor: content.app.color }}
        >
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-50" />

          <div className="relative z-10">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              Ready to Simplify Your Offboarding?
            </h2>
            <p className="text-lg text-white/80 mb-8 max-w-xl mx-auto">
              Join forward-thinking HR teams using DClaw Offboard to protect their business and treat departing employees with respect.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/checklists/create"
                className="px-8 py-3.5 rounded-xl bg-white text-gray-900 font-semibold hover:bg-gray-100 transition-all shadow-lg"
              >
                Start Your First Offboarding
              </Link>
              <Link
                href="/copilot"
                className="px-8 py-3.5 rounded-xl border-2 border-white/30 text-white font-semibold hover:bg-white/10 transition-all flex items-center gap-2"
              >
                <MessageSquare className="w-4 h-4" />
                Ask the AI Copilot
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
