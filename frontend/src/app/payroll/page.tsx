"use client";

import { useState } from "react";
import { ArrowLeft, Calculator, DollarSign, FileText } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import content from "@/data/landing-content.json";

const payFeature = content.features.find((f) => f.id === "payroll")!;

export default function PayrollPage() {
  const [form, setForm] = useState({
    employee_name: "",
    employee_email: "",
    last_day: "",
    base_salary: "0",
    unused_pto_hours: "0",
    pto_payout_rate: "0",
    severance_weeks: "0",
    bonus_amount: "0",
    deductions: "0",
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function calculate(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${apiBase}/api/v1/final-pay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          employee_name: form.employee_name,
          employee_email: form.employee_email,
          last_day: form.last_day,
          base_salary: parseFloat(form.base_salary) || 0,
          unused_pto_hours: parseFloat(form.unused_pto_hours) || 0,
          pto_payout_rate: parseFloat(form.pto_payout_rate) || 0,
          severance_weeks: parseFloat(form.severance_weeks) || 0,
          bonus_amount: parseFloat(form.bonus_amount) || 0,
          deductions: parseFloat(form.deductions) || 0,
        }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="w-16 h-16 rounded-2xl bg-teal-100 flex items-center justify-center mx-auto mb-4">
            <Calculator className="w-8 h-8 text-teal-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{payFeature.title}</h1>
          <p className="text-gray-500 text-lg">{payFeature.description}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-teal-500" />
                Pay Calculation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={calculate} className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Employee Name *</label>
                    <Input required value={form.employee_name} onChange={(e) => setForm({ ...form, employee_name: e.target.value })} placeholder="John Smith" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Email *</label>
                    <Input required type="email" value={form.employee_email} onChange={(e) => setForm({ ...form, employee_email: e.target.value })} placeholder="john@company.com" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Last Day *</label>
                    <Input required type="date" value={form.last_day} onChange={(e) => setForm({ ...form, last_day: e.target.value })} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Annual Base Salary ($)</label>
                    <Input type="number" value={form.base_salary} onChange={(e) => setForm({ ...form, base_salary: e.target.value })} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Unused PTO (hours)</label>
                    <Input type="number" value={form.unused_pto_hours} onChange={(e) => setForm({ ...form, unused_pto_hours: e.target.value })} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">PTO Payout Rate ($/hr)</label>
                    <Input type="number" value={form.pto_payout_rate} onChange={(e) => setForm({ ...form, pto_payout_rate: e.target.value })} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Severance (weeks)</label>
                    <Input type="number" value={form.severance_weeks} onChange={(e) => setForm({ ...form, severance_weeks: e.target.value })} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Bonus ($)</label>
                    <Input type="number" value={form.bonus_amount} onChange={(e) => setForm({ ...form, bonus_amount: e.target.value })} />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Deductions ($)</label>
                    <Input type="number" value={form.deductions} onChange={(e) => setForm({ ...form, deductions: e.target.value })} />
                  </div>
                </div>
                <Button type="submit" disabled={loading} className="w-full">
                  {loading ? "Calculating..." : "Calculate Final Pay"}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-teal-500" />
                Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              {result ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    {[
                      { label: "Severance", value: `$${result.severance_amount?.toLocaleString() || "0"}` },
                      { label: "PTO Payout", value: `$${((result.unused_pto_hours || 0) * (result.pto_payout_rate || 0)).toLocaleString()}` },
                      { label: "Bonus", value: `$${result.bonus_amount?.toLocaleString() || "0"}` },
                      { label: "Deductions", value: `-$${result.deductions?.toLocaleString() || "0"}` },
                    ].map((r) => (
                      <div key={r.label} className="flex justify-between py-2 border-b border-gray-100">
                        <span className="text-gray-500">{r.label}</span>
                        <span className="font-medium text-gray-900">{r.value}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between items-center pt-2">
                    <span className="text-base font-semibold text-gray-900">Total Final Pay</span>
                    <span className="text-2xl font-bold text-teal-600">
                      ${result.total_final_pay?.toLocaleString() || "0"}
                    </span>
                  </div>
                  {result.compliance_notes && (
                    <div className="mt-4 p-3 bg-gray-50 rounded-lg text-xs text-gray-600">
                      {result.compliance_notes}
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 text-gray-400">
                  <Calculator className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Enter employee details and click Calculate to see results.</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
