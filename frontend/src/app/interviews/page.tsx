"use client";

import { ArrowLeft, MessageSquare, Calendar, Sparkles } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import content from "@/data/landing-content.json";

const interviewFeature = content.features.find((f) => f.id === "interviews")!;

export default function InterviewsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="w-16 h-16 rounded-2xl bg-purple-100 flex items-center justify-center mx-auto mb-4">
            <MessageSquare className="w-8 h-8 text-purple-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{interviewFeature.title}</h1>
          <p className="text-gray-500 text-lg">{interviewFeature.description}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader>
              <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center mb-3">
                <Calendar className="w-5 h-5 text-purple-500" />
              </div>
              <CardTitle>Schedule Interview</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Schedule confidential 30-minute exit interviews. Async or live — flexible for remote employees.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center mb-3">
                <Sparkles className="w-5 h-5 text-indigo-500" />
              </div>
              <CardTitle>AI Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Automatic transcription, sentiment analysis, and theme extraction. Get actionable insights in minutes.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center mb-3">
                <MessageSquare className="w-5 h-5 text-green-500" />
              </div>
              <CardTitle>Insights Dashboard</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Track trends across interviews. Identify systemic issues before they impact retention.</p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader><CardTitle>Exit Interview Form</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-gray-500">This feature will be available when connected to the backend. In the meantime, use the AI Copilot (bottom-right) to get guidance on conducting effective exit interviews.</p>
            <div className="p-4 bg-gray-50 rounded-xl text-sm text-gray-600">
              <p className="font-medium mb-2">Quick access via Copilot:</p>
              <p>Ask: &ldquo;Schedule an exit interview for [employee name]&rdquo; or &ldquo;Analyze exit interview findings&rdquo;</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
