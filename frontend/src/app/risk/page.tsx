"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { AlertTriangle, Shield, Download, FileSearch, Activity } from "lucide-react";
import { listRiskAssessments, runRiskAssessment, getRiskOverview } from "@/lib/api";

export default function RiskAssessmentPage() {
  const [assessments, setAssessments] = useState<any[]>([]);
  const [overview, setOverview] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    employee_name: "",
    employee_email: "",
    department: "",
    role: "",
    last_day: "",
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [assess, over] = await Promise.all([listRiskAssessments(), getRiskOverview()]);
      setAssessments(assess.items || []);
      setOverview(over);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleRunAssessment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await runRiskAssessment({ ...form, last_day: form.last_day || undefined });
      setForm({ employee_name: "", employee_email: "", department: "", role: "", last_day: "" });
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-6">
          <AlertTriangle className="w-8 h-8 text-red-500" />
          <h1 className="text-3xl font-bold text-gray-900">Risk Assessment & IP Protection</h1>
        </div>

        {/* Overview Cards */}
        {overview && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl p-4 shadow-sm border">
              <div className="text-2xl font-bold text-gray-900">{overview.total_assessments}</div>
              <div className="text-sm text-gray-500">Total Assessments</div>
            </div>
            <div className="bg-red-50 rounded-xl p-4 shadow-sm border border-red-100">
              <div className="text-2xl font-bold text-red-600">{overview.critical_risks}</div>
              <div className="text-sm text-red-500">Critical Risks</div>
            </div>
            <div className="bg-orange-50 rounded-xl p-4 shadow-sm border border-orange-100">
              <div className="text-2xl font-bold text-orange-600">{overview.high_risks}</div>
              <div className="text-sm text-orange-500">High Risks</div>
            </div>
            <div className="bg-green-50 rounded-xl p-4 shadow-sm border border-green-100">
              <div className="text-2xl font-bold text-green-600">{overview.evidence_preserved_count}</div>
              <div className="text-sm text-green-500">Evidence Preserved</div>
            </div>
          </div>
        )}

        {/* Run Assessment Form */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <FileSearch className="w-5 h-5 text-indigo-500" />
            Run New Risk Assessment
          </h2>
          <form onSubmit={handleRunAssessment} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              className="border rounded-lg px-3 py-2 text-sm"
              placeholder="Employee Name"
              value={form.employee_name}
              onChange={(e) => setForm({ ...form, employee_name: e.target.value })}
              required
            />
            <input
              className="border rounded-lg px-3 py-2 text-sm"
              placeholder="Employee Email"
              type="email"
              value={form.employee_email}
              onChange={(e) => setForm({ ...form, employee_email: e.target.value })}
              required
            />
            <input
              className="border rounded-lg px-3 py-2 text-sm"
              placeholder="Department"
              value={form.department}
              onChange={(e) => setForm({ ...form, department: e.target.value })}
              required
            />
            <input
              className="border rounded-lg px-3 py-2 text-sm"
              placeholder="Role"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
              required
            />
            <input
              className="border rounded-lg px-3 py-2 text-sm"
              type="date"
              value={form.last_day}
              onChange={(e) => setForm({ ...form, last_day: e.target.value })}
            />
            <button
              type="submit"
              className="bg-red-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-red-700 transition"
            >
              Run Assessment
            </button>
          </form>
        </div>

        {/* Assessments List */}
        <div className="bg-white rounded-xl shadow-sm border">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold">Risk Assessments</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-3 font-medium text-gray-600">Employee</th>
                  <th className="text-left p-3 font-medium text-gray-600">Department</th>
                  <th className="text-left p-3 font-medium text-gray-600">Risk Score</th>
                  <th className="text-left p-3 font-medium text-gray-600">Risk Level</th>
                  <th className="text-left p-3 font-medium text-gray-600">Evidence</th>
                  <th className="text-left p-3 font-medium text-gray-600">Date</th>
                </tr>
              </thead>
              <tbody>
                {assessments.map((a: any) => (
                  <tr key={a.id} className="border-t hover:bg-gray-50">
                    <td className="p-3">{a.employee_name}</td>
                    <td className="p-3 text-gray-500">{a.department}</td>
                    <td className="p-3 font-mono">{a.risk_score}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        a.risk_level === "critical" ? "bg-red-100 text-red-700" :
                        a.risk_level === "high" ? "bg-orange-100 text-orange-700" :
                        a.risk_level === "medium" ? "bg-yellow-100 text-yellow-700" :
                        "bg-green-100 text-green-700"
                      }`}>
                        {a.risk_level}
                      </span>
                    </td>
                    <td className="p-3">
                      {a.evidence_preserved ? (
                        <span className="text-green-600 text-xs font-medium">Preserved ✓</span>
                      ) : (
                        <span className="text-gray-400 text-xs">None</span>
                      )}
                    </td>
                    <td className="p-3 text-gray-500 text-xs">
                      {new Date(a.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
                {assessments.length === 0 && (
                  <tr><td colSpan={6} className="p-6 text-center text-gray-400">No assessments yet</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
