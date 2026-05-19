"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, ClipboardCheck, Package, ShieldOff, Users, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import content from "@/data/landing-content.json";

interface Stats {
  total_checklists: number;
  active_checklists: number;
  completed_checklists: number;
  total_assets_pending: number;
  total_revocations_pending: number;
  pending_interviews: number;
  alumni_count: number;
  recent_checklists: any[];
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  async function fetchStats() {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${apiBase}/api/v1/dashboard`);
      const data = await res.json();
      setStats(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  const cards = [
    { label: "Active Checklists", value: stats?.active_checklists ?? "—", icon: ClipboardCheck, color: "#3B82F6" },
    { label: "Completed", value: stats?.completed_checklists ?? "—", icon: ClipboardCheck, color: "#10B981" },
    { label: "Assets Pending Return", value: stats?.total_assets_pending ?? "—", icon: Package, color: "#F59E0B" },
    { label: "Pending Revocations", value: stats?.total_revocations_pending ?? "—", icon: ShieldOff, color: "#EF4444" },
    { label: "Pending Interviews", value: stats?.pending_interviews ?? "—", icon: Users, color: "#8B5CF6" },
    { label: "Alumni Network", value: stats?.alumni_count ?? "—", icon: TrendingUp, color: "#EC4899" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Offboarding overview and key metrics</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {cards.map((card) => {
            const Icon = card.icon;
            return (
              <Card key={card.label}>
                <CardContent className="py-4 flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: card.color + "15" }}>
                    <Icon className="w-5 h-5" style={{ color: card.color }} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">{card.label}</p>
                    <p className="text-2xl font-bold text-gray-900">{loading ? "..." : card.value}</p>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Recent Checklists</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-sm text-gray-500">Loading...</p>
            ) : stats?.recent_checklists?.length ? (
              <div className="space-y-3">
                {stats.recent_checklists.map((c: any) => (
                  <div key={c.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-sm text-gray-900">{c.employee_name}</p>
                      <p className="text-xs text-gray-500">{c.department} · Last day: {c.last_day}</p>
                    </div>
                    <Badge className={c.status === "completed" ? "bg-green-100 text-green-700" : "bg-blue-100 text-blue-700"}>
                      {c.status?.replace("_", " ")}
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <ClipboardCheck className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">No checklists yet.</p>
                <Link href="/checklists/create" className="text-sm text-indigo-600 hover:text-indigo-800 mt-2 inline-block">
                  Create your first checklist →
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
