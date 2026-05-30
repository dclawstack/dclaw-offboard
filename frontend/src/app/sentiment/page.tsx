"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Activity, ArrowLeft, AlertCircle, TrendingUp, Users, Brain } from "lucide-react";
import {
  listSentimentPulses,
  createSentimentPulse,
  listFlightRiskAlerts,
  detectFlightRisk,
  getSentimentOverview,
} from "@/lib/api";

const CATEGORIES = ["engagement", "burnout", "management", "compensation", "growth", "culture"];
const DEPARTMENTS = ["engineering", "sales", "marketing", "hr", "finance", "legal", "product", "design", "operations"];

const riskColor: Record<string, string> = {
  critical: "bg-red-100 text-red-700",
  high: "bg-orange-100 text-orange-700",
  medium: "bg-yellow-100 text-yellow-700",
  low: "bg-green-100 text-green-700",
};

const sentimentColor: Record<string, string> = {
  positive: "bg-green-100 text-green-700",
  neutral: "bg-gray-100 text-gray-700",
  negative: "bg-red-100 text-red-700",
};

export default function SentimentPage() {
  const [pulses, setPulses] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [overview, setOverview] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"pulses" | "risks">("pulses");

  const [pulseForm, setPulseForm] = useState({
    title: "",
    category: "engagement",
    department: "",
    team_size: "",
    survey_date: "",
  });

  const [riskForm, setRiskForm] = useState({
    employee_name: "",
    employee_email: "",
    department: "",
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [p, a, o] = await Promise.all([
        listSentimentPulses(),
        listFlightRiskAlerts(),
        getSentimentOverview(),
      ]);
      setPulses(p.items || []);
      setAlerts(a.items || []);
      setOverview(o);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handlePulseSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createSentimentPulse({
        ...pulseForm,
        team_size: pulseForm.team_size ? Number(pulseForm.team_size) : undefined,
        survey_date: pulseForm.survey_date || undefined,
        department: pulseForm.department || undefined,
      });
      setPulseForm({ title: "", category: "engagement", department: "", team_size: "", survey_date: "" });
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleRiskDetect = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await detectFlightRisk(riskForm.employee_name, riskForm.employee_email, riskForm.department);
      setRiskForm({ employee_name: "", employee_email: "", department: "" });
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="flex items-center gap-3 mb-6">
          <Activity className="w-8 h-8 text-pink-500" />
          <h1 className="text-3xl font-bold text-gray-900">Sentiment &amp; Early Warning</h1>
        </div>

        {/* Overview Cards */}
        {overview && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl p-4 shadow-sm border">
              <div className="text-2xl font-bold text-gray-900">{overview.total_pulses ?? 0}</div>
              <div className="text-sm text-gray-500 flex items-center gap-1"><TrendingUp className="w-3.5 h-3.5" /> Total Surveys</div>
            </div>
            <div className="bg-red-50 rounded-xl p-4 shadow-sm border border-red-100">
              <div className="text-2xl font-bold text-red-600">{overview.critical_risks ?? 0}</div>
              <div className="text-sm text-red-500 flex items-center gap-1"><AlertCircle className="w-3.5 h-3.5" /> Critical Flight Risks</div>
            </div>
            <div className="bg-orange-50 rounded-xl p-4 shadow-sm border border-orange-100">
              <div className="text-2xl font-bold text-orange-600">{overview.high_risks ?? 0}</div>
              <div className="text-sm text-orange-500 flex items-center gap-1"><Users className="w-3.5 h-3.5" /> High Flight Risks</div>
            </div>
            <div className="bg-pink-50 rounded-xl p-4 shadow-sm border border-pink-100">
              <div className="text-2xl font-bold text-pink-600">
                {overview.avg_sentiment_score ? Number(overview.avg_sentiment_score).toFixed(1) : "—"}
              </div>
              <div className="text-sm text-pink-500 flex items-center gap-1"><Brain className="w-3.5 h-3.5" /> Avg Sentiment Score</div>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab("pulses")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${activeTab === "pulses" ? "bg-pink-600 text-white" : "bg-white border text-gray-600 hover:bg-gray-50"}`}
          >
            Pulse Surveys ({pulses.length})
          </button>
          <button
            onClick={() => setActiveTab("risks")}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${activeTab === "risks" ? "bg-red-600 text-white" : "bg-white border text-gray-600 hover:bg-gray-50"}`}
          >
            Flight Risk Alerts ({alerts.length})
          </button>
        </div>

        {activeTab === "pulses" && (
          <>
            <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-pink-500" /> Create Pulse Survey
              </h2>
              <form onSubmit={handlePulseSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input
                  className="border rounded-lg px-3 py-2 text-sm col-span-1 md:col-span-2"
                  placeholder="Survey title (e.g. Q2 Engineering Engagement)"
                  value={pulseForm.title}
                  onChange={(e) => setPulseForm({ ...pulseForm, title: e.target.value })}
                  required
                />
                <select
                  className="border rounded-lg px-3 py-2 text-sm"
                  value={pulseForm.category}
                  onChange={(e) => setPulseForm({ ...pulseForm, category: e.target.value })}
                >
                  {CATEGORIES.map((c) => (
                    <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                  ))}
                </select>
                <select
                  className="border rounded-lg px-3 py-2 text-sm"
                  value={pulseForm.department}
                  onChange={(e) => setPulseForm({ ...pulseForm, department: e.target.value })}
                >
                  <option value="">All Departments</option>
                  {DEPARTMENTS.map((d) => (
                    <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
                  ))}
                </select>
                <input
                  className="border rounded-lg px-3 py-2 text-sm"
                  placeholder="Team size (optional)"
                  type="number"
                  min={1}
                  value={pulseForm.team_size}
                  onChange={(e) => setPulseForm({ ...pulseForm, team_size: e.target.value })}
                />
                <input
                  className="border rounded-lg px-3 py-2 text-sm"
                  type="date"
                  value={pulseForm.survey_date}
                  onChange={(e) => setPulseForm({ ...pulseForm, survey_date: e.target.value })}
                />
                <button
                  type="submit"
                  className="md:col-span-3 bg-pink-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-pink-700 transition"
                >
                  Run Survey Analysis
                </button>
              </form>
            </div>

            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-4 border-b">
                <h2 className="text-lg font-semibold">Pulse Survey Results</h2>
              </div>
              {loading ? (
                <div className="p-8 text-center text-gray-400">Loading...</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="text-left p-3 font-medium text-gray-600">Title</th>
                        <th className="text-left p-3 font-medium text-gray-600">Category</th>
                        <th className="text-left p-3 font-medium text-gray-600">Department</th>
                        <th className="text-left p-3 font-medium text-gray-600">Avg Score</th>
                        <th className="text-left p-3 font-medium text-gray-600">Sentiment</th>
                        <th className="text-left p-3 font-medium text-gray-600">Responses</th>
                        <th className="text-left p-3 font-medium text-gray-600">Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {pulses.map((p: any) => (
                        <tr key={p.id} className="border-t hover:bg-gray-50">
                          <td className="p-3 font-medium">{p.title}</td>
                          <td className="p-3 text-gray-500 capitalize">{p.category}</td>
                          <td className="p-3 text-gray-500 capitalize">{p.department || "All"}</td>
                          <td className="p-3 font-mono">{p.avg_score ? Number(p.avg_score).toFixed(1) : "—"}</td>
                          <td className="p-3">
                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${sentimentColor[p.sentiment_label] || "bg-gray-100 text-gray-600"}`}>
                              {p.sentiment_label || "—"}
                            </span>
                          </td>
                          <td className="p-3 text-gray-500">{p.response_count ?? "—"}</td>
                          <td className="p-3 text-gray-500 text-xs">
                            {p.survey_date || new Date(p.created_at).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                      {pulses.length === 0 && (
                        <tr><td colSpan={7} className="p-6 text-center text-gray-400">No pulse surveys yet — run one above</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        )}

        {activeTab === "risks" && (
          <>
            <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-red-500" /> Detect Flight Risk
              </h2>
              <form onSubmit={handleRiskDetect} className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input
                  className="border rounded-lg px-3 py-2 text-sm"
                  placeholder="Employee Name"
                  value={riskForm.employee_name}
                  onChange={(e) => setRiskForm({ ...riskForm, employee_name: e.target.value })}
                  required
                />
                <input
                  className="border rounded-lg px-3 py-2 text-sm"
                  placeholder="Employee Email"
                  type="email"
                  value={riskForm.employee_email}
                  onChange={(e) => setRiskForm({ ...riskForm, employee_email: e.target.value })}
                  required
                />
                <select
                  className="border rounded-lg px-3 py-2 text-sm"
                  value={riskForm.department}
                  onChange={(e) => setRiskForm({ ...riskForm, department: e.target.value })}
                  required
                >
                  <option value="">Select Department</option>
                  {DEPARTMENTS.map((d) => (
                    <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
                  ))}
                </select>
                <button
                  type="submit"
                  className="md:col-span-3 bg-red-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-red-700 transition"
                >
                  Run AI Flight Risk Detection
                </button>
              </form>
            </div>

            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-4 border-b">
                <h2 className="text-lg font-semibold">Flight Risk Alerts</h2>
              </div>
              {loading ? (
                <div className="p-8 text-center text-gray-400">Loading...</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="text-left p-3 font-medium text-gray-600">Employee</th>
                        <th className="text-left p-3 font-medium text-gray-600">Department</th>
                        <th className="text-left p-3 font-medium text-gray-600">Risk Level</th>
                        <th className="text-left p-3 font-medium text-gray-600">Risk Score</th>
                        <th className="text-left p-3 font-medium text-gray-600">Top Signal</th>
                        <th className="text-left p-3 font-medium text-gray-600">Status</th>
                        <th className="text-left p-3 font-medium text-gray-600">Detected</th>
                      </tr>
                    </thead>
                    <tbody>
                      {alerts.map((a: any) => (
                        <tr key={a.id} className="border-t hover:bg-gray-50">
                          <td className="p-3">
                            <div className="font-medium">{a.employee_name}</div>
                            <div className="text-xs text-gray-400">{a.employee_email}</div>
                          </td>
                          <td className="p-3 text-gray-500 capitalize">{a.department}</td>
                          <td className="p-3">
                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${riskColor[a.flight_risk_level] || "bg-gray-100 text-gray-600"}`}>
                              {a.flight_risk_level}
                            </span>
                          </td>
                          <td className="p-3 font-mono">{a.risk_score}</td>
                          <td className="p-3 text-gray-500 text-xs max-w-xs truncate">
                            {(a.risk_signals || [])[0] || "—"}
                          </td>
                          <td className="p-3">
                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                              a.status === "resolved" ? "bg-green-100 text-green-700" :
                              a.status === "acknowledged" ? "bg-blue-100 text-blue-700" :
                              "bg-yellow-100 text-yellow-700"
                            }`}>
                              {a.status}
                            </span>
                          </td>
                          <td className="p-3 text-gray-500 text-xs">{new Date(a.created_at).toLocaleDateString()}</td>
                        </tr>
                      ))}
                      {alerts.length === 0 && (
                        <tr><td colSpan={7} className="p-6 text-center text-gray-400">No flight risk alerts — detect one above</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
