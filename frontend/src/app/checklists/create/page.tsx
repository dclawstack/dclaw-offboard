"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Sparkles } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import config from "@/data/app-config.json";

export default function CreateChecklistPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    employee_name: "",
    employee_email: "",
    employee_role: "",
    department: "engineering",
    last_day: "",
    notes: "",
  });
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${apiBase}/api/v1/checklists`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        const data = await res.json();
        router.push(`/checklists/${data.id}`);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
        <Link href="/checklists" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to checklists
        </Link>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-500" />
              Create Offboarding Checklist
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Employee Name *</label>
                  <Input required value={form.employee_name} onChange={(e) => setForm({ ...form, employee_name: e.target.value })} placeholder="John Smith" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Employee Email *</label>
                  <Input required type="email" value={form.employee_email} onChange={(e) => setForm({ ...form, employee_email: e.target.value })} placeholder="john@company.com" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Role *</label>
                  <Input required value={form.employee_role} onChange={(e) => setForm({ ...form, employee_role: e.target.value })} placeholder="Senior Engineer" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Department *</label>
                  <select
                    required
                    value={form.department}
                    onChange={(e) => setForm({ ...form, department: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200"
                  >
                    {config.departments.map((d) => (
                      <option key={d} value={d}>{d.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}</option>
                    ))}
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Last Day *</label>
                  <Input required type="date" value={form.last_day} onChange={(e) => setForm({ ...form, last_day: e.target.value })} />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Notes</label>
                <textarea
                  value={form.notes}
                  onChange={(e) => setForm({ ...form, notes: e.target.value })}
                  placeholder="Any special instructions..."
                  rows={3}
                  className="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 resize-none"
                />
              </div>
              <Button type="submit" disabled={loading} className="w-full">
                {loading ? "Creating..." : "Generate Checklist with AI Tasks"}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
