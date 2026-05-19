"use client";

import { ArrowLeft, Bot, Sparkles } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import content from "@/data/landing-content.json";

const copilotFeature = content.features.find((f) => f.id === "copilot")!;

export default function CopilotPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="w-16 h-16 rounded-2xl bg-indigo-100 flex items-center justify-center mx-auto mb-4">
            <Bot className="w-8 h-8 text-indigo-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{copilotFeature.title}</h1>
          <p className="text-gray-500 text-lg">{copilotFeature.description}</p>
        </div>

        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-500" />
              Copilot is Ready — Start a Conversation
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-gray-600">
              The Offboard Copilot widget is available in the bottom-right corner of every page.
              Click the <Bot className="w-4 h-4 inline text-indigo-500" /> button to open it.
            </p>

            <div className="space-y-3">
              <p className="text-sm font-medium text-gray-700">Try asking:</p>
              {[
                "Create an offboarding checklist for a senior engineer",
                "What's the policy on final pay and PTO payout?",
                "How do I revoke access for a departing employee?",
                "What equipment needs to be returned?",
                "Schedule an exit interview",
              ].map((q) => (
                <div key={q} className="p-3 bg-indigo-50 rounded-lg text-sm text-indigo-700 cursor-pointer hover:bg-indigo-100 transition-colors">
                  &ldquo;{q}&rdquo;
                </div>
              ))}
            </div>

            <div className="pt-4 border-t border-gray-100">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Covered Topics</h3>
              <div className="flex flex-wrap gap-2">
                {[
                  "Checklists", "Final Pay", "Benefits", "Equipment",
                  "Access Revocation", "Exit Interviews", "Knowledge Transfer",
                  "Alumni", "Compliance", "Severance",
                ].map((t) => (
                  <span key={t} className="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-600">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
