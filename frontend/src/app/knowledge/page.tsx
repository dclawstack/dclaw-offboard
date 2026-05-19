"use client";

import { ArrowLeft, BookOpen, FileText, Users, Key } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import content from "@/data/landing-content.json";

const ktFeature = content.features.find((f) => f.id === "knowledge")!;

export default function KnowledgePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="w-16 h-16 rounded-2xl bg-blue-100 flex items-center justify-center mx-auto mb-4">
            <BookOpen className="w-8 h-8 text-blue-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{ktFeature.title}</h1>
          <p className="text-gray-500 text-lg">{ktFeature.description}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { icon: FileText, title: "Project Docs", desc: "Active project status, roadmaps, and documentation", color: "#3B82F6" },
            { icon: Users, title: "Key Contacts", desc: "Customer, vendor, and partner relationships", color: "#8B5CF6" },
            { icon: Key, title: "Credentials", desc: "Passwords, API keys, and access tokens", color: "#F59E0B" },
            { icon: BookOpen, title: "Processes", desc: "Internal workflows, runbooks, and SOPs", color: "#10B981" },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <Card key={item.title} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6 text-center">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4" style={{ backgroundColor: item.color + "15" }}>
                    <Icon className="w-6 h-6" style={{ color: item.color }} />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-500">{item.desc}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <Card>
          <CardHeader><CardTitle>Knowledge Transfer Form</CardTitle></CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500">
              The knowledge transfer system captures critical institutional knowledge before employee departure.
              Connect to the backend to create handover documents, assign successors, and validate knowledge completeness.
            </p>
            <div className="mt-4 p-4 bg-gray-50 rounded-xl text-sm text-gray-600">
              <p className="font-medium mb-2">AI Copilot can help:</p>
              <p>Ask: &ldquo;Start a knowledge transfer for [employee]&rdquo; or &ldquo;What should be in a handover document?&rdquo;</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
