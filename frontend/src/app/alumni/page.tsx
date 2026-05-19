"use client";

import { ArrowLeft, Users, UserCheck, UserX, TrendingUp } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import content from "@/data/landing-content.json";

const alumniFeature = content.features.find((f) => f.id === "alumni")!;

export default function AlumniPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="w-16 h-16 rounded-2xl bg-pink-100 flex items-center justify-center mx-auto mb-4">
            <Users className="w-8 h-8 text-pink-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{alumniFeature.title}</h1>
          <p className="text-gray-500 text-lg">{alumniFeature.description}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          {[
            { icon: Users, label: "Total Alumni", value: "0", color: "#F472B6" },
            { icon: UserCheck, label: "Rehire Eligible", value: "0", color: "#10B981" },
            { icon: TrendingUp, label: "Engagement Score", value: "—", color: "#3B82F6" },
          ].map((s) => {
            const Icon = s.icon;
            return (
              <Card key={s.label}>
                <CardContent className="py-4 flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: s.color + "15" }}>
                    <Icon className="w-5 h-5" style={{ color: s.color }} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">{s.label}</p>
                    <p className="text-2xl font-bold text-gray-900">{s.value}</p>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Alumni Directory</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center py-12">
              <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No alumni records yet. Alumni are automatically added when offboarding checklists are completed.</p>
              <div className="mt-4 inline-flex gap-2">
                <Badge className="bg-green-100 text-green-700">Eligible</Badge>
                <Badge className="bg-yellow-100 text-yellow-700">Conditional</Badge>
                <Badge className="bg-red-100 text-red-700">Not Eligible</Badge>
                <Badge className="bg-gray-100 text-gray-600">Pending Review</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
