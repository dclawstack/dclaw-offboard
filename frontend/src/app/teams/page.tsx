"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { UsersRound, ArrowLeft, UserPlus, Calendar, ShieldCheck, GitMerge } from "lucide-react";
import { listTeamTransitions, createTeamTransition } from "@/lib/api";

const DEPARTMENTS = ["engineering", "sales", "marketing", "hr", "finance", "legal", "product", "design", "operations"];

const statusColor: Record<string, string> = {
  planning: "bg-yellow-100 text-yellow-700",
  in_progress: "bg-blue-100 text-blue-700",
  completed: "bg-green-100 text-green-700",
};

export default function TeamsPage() {
  const [transitions, setTransitions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    departing_employee_name: "",
    departing_employee_email: "",
    department: "",
    role: "",
    last_day: "",
    successor_name: "",
    successor_email: "",
  });
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const res = await listTeamTransitions();
      setTransitions(res.items || []);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createTeamTransition({
        ...form,
        last_day: form.last_day || undefined,
        successor_name: form.successor_name || undefined,
        successor_email: form.successor_email || undefined,
      });
      setForm({
        departing_employee_name: "",
        departing_employee_email: "",
        department: "",
        role: "",
        last_day: "",
        successor_name: "",
        successor_email: "",
      });
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const coverageStats = (t: any) => {
    const items: any[] = t.coverage_items || [];
    const covered = items.filter((i) => i.status === "covered").length;
    return { total: items.length, covered };
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="flex items-center gap-3 mb-6">
          <UsersRound className="w-8 h-8 text-amber-500" />
          <h1 className="text-3xl font-bold text-gray-900">Team Transition &amp; Coverage</h1>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 shadow-sm border">
            <div className="text-2xl font-bold text-gray-900">{transitions.length}</div>
            <div className="text-sm text-gray-500 flex items-center gap-1"><GitMerge className="w-3.5 h-3.5" /> Total Transitions</div>
          </div>
          <div className="bg-blue-50 rounded-xl p-4 shadow-sm border border-blue-100">
            <div className="text-2xl font-bold text-blue-600">
              {transitions.filter((t) => t.status === "in_progress").length}
            </div>
            <div className="text-sm text-blue-500 flex items-center gap-1"><Calendar className="w-3.5 h-3.5" /> In Progress</div>
          </div>
          <div className="bg-green-50 rounded-xl p-4 shadow-sm border border-green-100">
            <div className="text-2xl font-bold text-green-600">
              {transitions.filter((t) => t.status === "completed").length}
            </div>
            <div className="text-sm text-green-500 flex items-center gap-1"><ShieldCheck className="w-3.5 h-3.5" /> Completed</div>
          </div>
          <div className="bg-amber-50 rounded-xl p-4 shadow-sm border border-amber-100">
            <div className="text-2xl font-bold text-amber-600">
              {transitions.filter((t) => t.successor_name).length}
            </div>
            <div className="text-sm text-amber-500 flex items-center gap-1"><UserPlus className="w-3.5 h-3.5" /> With Successor</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Create Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <UserPlus className="w-5 h-5 text-amber-500" /> Create Transition Plan
              </h2>
              <form onSubmit={handleSubmit} className="space-y-3">
                <input
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  placeholder="Departing Employee Name"
                  value={form.departing_employee_name}
                  onChange={(e) => setForm({ ...form, departing_employee_name: e.target.value })}
                  required
                />
                <input
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  placeholder="Departing Employee Email"
                  type="email"
                  value={form.departing_employee_email}
                  onChange={(e) => setForm({ ...form, departing_employee_email: e.target.value })}
                  required
                />
                <select
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  value={form.department}
                  onChange={(e) => setForm({ ...form, department: e.target.value })}
                  required
                >
                  <option value="">Select Department</option>
                  {DEPARTMENTS.map((d) => (
                    <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>
                  ))}
                </select>
                <input
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  placeholder="Role / Title"
                  value={form.role}
                  onChange={(e) => setForm({ ...form, role: e.target.value })}
                  required
                />
                <input
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  type="date"
                  placeholder="Last Day"
                  value={form.last_day}
                  onChange={(e) => setForm({ ...form, last_day: e.target.value })}
                />
                <div className="pt-2 border-t">
                  <p className="text-xs text-gray-400 mb-2">Successor (optional)</p>
                  <input
                    className="w-full border rounded-lg px-3 py-2 text-sm mb-2"
                    placeholder="Successor Name"
                    value={form.successor_name}
                    onChange={(e) => setForm({ ...form, successor_name: e.target.value })}
                  />
                  <input
                    className="w-full border rounded-lg px-3 py-2 text-sm"
                    placeholder="Successor Email"
                    type="email"
                    value={form.successor_email}
                    onChange={(e) => setForm({ ...form, successor_email: e.target.value })}
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-amber-500 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-amber-600 transition"
                >
                  Create Transition Plan
                </button>
              </form>
            </div>
          </div>

          {/* Transitions List + Detail */}
          <div className="lg:col-span-2 space-y-4">
            {loading ? (
              <div className="bg-white rounded-xl shadow-sm border p-8 text-center text-gray-400">Loading...</div>
            ) : transitions.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border p-8 text-center text-gray-400">
                No transitions yet — create one using the form.
              </div>
            ) : (
              transitions.map((t: any) => {
                const { total, covered } = coverageStats(t);
                const isOpen = selected?.id === t.id;
                return (
                  <div key={t.id} className="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <button
                      className="w-full text-left p-4 hover:bg-gray-50 transition"
                      onClick={() => setSelected(isOpen ? null : t)}
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <div className="font-semibold text-gray-900">{t.departing_employee_name}</div>
                          <div className="text-sm text-gray-500">{t.role} · {t.department}</div>
                          {t.successor_name && (
                            <div className="text-xs text-green-600 mt-1">→ {t.successor_name}</div>
                          )}
                        </div>
                        <div className="flex items-center gap-3 flex-shrink-0">
                          {total > 0 && (
                            <div className="text-xs text-gray-500">{covered}/{total} covered</div>
                          )}
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor[t.status] || "bg-gray-100 text-gray-600"}`}>
                            {t.status?.replace("_", " ")}
                          </span>
                        </div>
                      </div>
                    </button>

                    {isOpen && t.coverage_items && t.coverage_items.length > 0 && (
                      <div className="border-t px-4 pb-4">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mt-3 mb-2">Coverage Items</p>
                        <div className="space-y-2">
                          {t.coverage_items.map((item: any) => (
                            <div key={item.id} className="flex items-center justify-between text-sm">
                              <span className="text-gray-700">{item.responsibility}</span>
                              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                                item.status === "covered" ? "bg-green-100 text-green-700" :
                                item.status === "in_progress" ? "bg-blue-100 text-blue-700" :
                                "bg-gray-100 text-gray-600"
                              }`}>
                                {item.status?.replace("_", " ")}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
