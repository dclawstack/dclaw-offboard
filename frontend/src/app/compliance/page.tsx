"use client";

import { useState, useEffect } from "react";
import { Scale, FileCheck, ShieldCheck, Clock } from "lucide-react";
import { listComplianceReports, generateComplianceReport } from "@/lib/api";

const FRAMEWORKS = ["eeoc", "osha", "gdpr", "ccpa", "soc2", "sox", "hipaa"];

const frameworkLabels: Record<string, string> = {
  eeoc: "EEOC", osha: "OSHA", gdpr: "GDPR", ccpa: "CCPA",
  soc2: "SOC2", sox: "SOX", hipaa: "HIPAA",
};

const frameworkColors: Record<string, string> = {
  eeoc: "bg-blue-100 text-blue-700", osha: "bg-green-100 text-green-700",
  gdpr: "bg-purple-100 text-purple-700", ccpa: "bg-orange-100 text-orange-700",
  soc2: "bg-indigo-100 text-indigo-700", sox: "bg-red-100 text-red-700",
  hipaa: "bg-teal-100 text-teal-700",
};

export default function CompliancePage() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    employee_name: "", employee_email: "", department: "", last_day: "", framework: "gdpr",
  });

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try { const r = await listComplianceReports(1, 100); setReports(r.items || []); } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    try { await generateComplianceReport(form); setForm({ ...form, employee_name: "", employee_email: "", department: "", last_day: "" }); loadData(); } catch (e) { console.error(e); }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-6">
          <Scale className="w-8 h-8 text-emerald-500" />
          <h1 className="text-3xl font-bold text-gray-900">Compliance Automation</h1>
        </div>

        {/* Generate Report Form */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <FileCheck className="w-5 h-5 text-indigo-500" />
            Generate Compliance Report
          </h2>
          <form onSubmit={handleGenerate} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input className="border rounded-lg px-3 py-2 text-sm" placeholder="Employee Name"
              value={form.employee_name} onChange={(e) => setForm({ ...form, employee_name: e.target.value })} required />
            <input className="border rounded-lg px-3 py-2 text-sm" placeholder="Employee Email" type="email"
              value={form.employee_email} onChange={(e) => setForm({ ...form, employee_email: e.target.value })} required />
            <input className="border rounded-lg px-3 py-2 text-sm" placeholder="Department"
              value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} required />
            <input className="border rounded-lg px-3 py-2 text-sm" type="date"
              value={form.last_day} onChange={(e) => setForm({ ...form, last_day: e.target.value })} required />
            <select className="border rounded-lg px-3 py-2 text-sm"
              value={form.framework} onChange={(e) => setForm({ ...form, framework: e.target.value })}>
              {FRAMEWORKS.map((fw) => (
                <option key={fw} value={fw}>{frameworkLabels[fw]}</option>
              ))}
            </select>
            <button type="submit" className="bg-emerald-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-emerald-700 transition">
              Generate Report
            </button>
          </form>
        </div>

        {/* Reports List */}
        <div className="bg-white rounded-xl shadow-sm border">
          <div className="p-4 border-b"><h2 className="text-lg font-semibold">Generated Reports</h2></div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-3 font-medium text-gray-600">Employee</th>
                  <th className="text-left p-3 font-medium text-gray-600">Framework</th>
                  <th className="text-left p-3 font-medium text-gray-600">Status</th>
                  <th className="text-left p-3 font-medium text-gray-600">AI Validated</th>
                  <th className="text-left p-3 font-medium text-gray-600">Retention Deadline</th>
                  <th className="text-left p-3 font-medium text-gray-600">Date</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((r: any) => (
                  <tr key={r.id} className="border-t hover:bg-gray-50">
                    <td className="p-3 font-medium">{r.employee_name}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${frameworkColors[r.framework] || ""}`}>
                        {frameworkLabels[r.framework] || r.framework}
                      </span>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        r.status === "submitted" ? "bg-green-100 text-green-700" :
                        r.status === "validated" ? "bg-blue-100 text-blue-700" :
                        r.status === "generated" ? "bg-yellow-100 text-yellow-700" :
                        "bg-gray-100 text-gray-700"
                      }`}>{r.status}</span>
                    </td>
                    <td className="p-3">
                      {r.ai_validated ? (
                        <span className="flex items-center gap-1 text-green-600 text-xs"><ShieldCheck className="w-3 h-3" /> Validated</span>
                      ) : <span className="text-gray-400 text-xs">Pending</span>}
                    </td>
                    <td className="p-3 text-xs text-gray-500">
                      {r.retention_deadline ? new Date(r.retention_deadline).toLocaleDateString() : "—"}
                    </td>
                    <td className="p-3 text-xs text-gray-500">{new Date(r.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
                {reports.length === 0 && <tr><td colSpan={6} className="p-6 text-center text-gray-400">No reports generated yet</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
