"use client";

import { useState } from "react";
import { UserX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface OffboardingChecklist {
  id: string;
  employee_name: string;
  last_day: string;
  access_revocations: string[];
  asset_returns: string[];
  knowledge_transfer_status: string;
  exit_interview_scheduled: boolean;
  created_at: string
}

export default function Dashboard() {
  const [employeeName, setEmployeeName] = useState("");
const [lastDay, setLastDay] = useState("");
  const [offboardingChecklist, setOffboardingChecklist] = useState<OffboardingChecklist | null>(null);
  const [extraData, setExtraData] = useState<any>(null);
const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!employeeName || !lastDay) return;
    setLoading(true);
    try {
      const res = await fetch("/checklists", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        employeeName: employeeName,
        lastDay: lastDay,
        }),
      });
      const data = await res.json();
      setOffboardingChecklist(data);
      const extraRes = await fetch(`/checklists/${data.id}/status`);
      const extraData = await extraRes.json();
      setExtraData(extraData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center gap-3">
        <UserX className="w-8 h-8" style={{ color: "#64748B" }} />
        <div>
          <h1 className="text-2xl font-bold">DClaw Offboard</h1>
          <p className="text-sm text-slate-500">Secure offboarding automation</p>
        </div>
        <Badge className="ml-auto" style={{ backgroundColor: "#64748B" }}>HR</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generate Offboarding Checklist</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <div className="space-y-2">
              <label className="text-sm font-medium">Employee name</label>
              <Input value={employeeName} onChange={(e) => setEmployeeName(e.target.value)} placeholder="e.g. John Smith" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Last day</label>
              <Input value={lastDay} onChange={(e) => setLastDay(e.target.value)} placeholder="e.g. 2025-06-30" />
            </div>

          </div>
          <Button onClick={handleSubmit} disabled={loading || !employeeName || !lastDay}>
            {loading ? "Processing..." : "Generate Offboarding Checklist"}
          </Button>
        </CardContent>
      </Card>

      {offboardingChecklist && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <Card>
            <CardHeader>
              <CardTitle>Checklist Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p><strong>ID:</strong> {offboardingChecklist.id}</p>
              <p><strong>Employee:</strong> {offboardingChecklist.employee_name}</p>
              <p><strong>Last Day:</strong> {offboardingChecklist.last_day}</p>
              <p><strong>Knowledge Transfer:</strong> {offboardingChecklist.knowledge_transfer_status}</p>
              <p><strong>Exit Interview Scheduled:</strong> {offboardingChecklist.exit_interview_scheduled ? 'Yes' : 'No'}</p>
              <p><strong>Created:</strong> {new Date(offboardingChecklist.created_at).toLocaleString()}</p>
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Access Revocations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {offboardingChecklist.access_revocations.map((item: string, i: number) => (
                  <Badge key={i} variant="secondary">{item}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Asset Returns</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {offboardingChecklist.asset_returns.map((item: string, i: number) => (
                  <Badge key={i} variant="secondary">{item}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Status</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm"><strong>Completion:</strong> {extraData?.completion_percent}%</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
