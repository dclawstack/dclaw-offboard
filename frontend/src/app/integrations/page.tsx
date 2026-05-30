"use client";

import { useState, useEffect } from "react";
import { Blocks, RefreshCw, Link2, Plug } from "lucide-react";
import { listIntegrations, seedIntegrations, syncIntegration, getIntegrationOverview } from "@/lib/api";

export default function IntegrationHubPage() {
  const [integrations, setIntegrations] = useState<any[]>([]);
  const [overview, setOverview] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState<string | null>(null);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const [ints, over] = await Promise.all([listIntegrations(1, 100), getIntegrationOverview()]);
      setIntegrations(ints.items || []);
      setOverview(over);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleSeed = async () => {
    try { await seedIntegrations(); loadData(); } catch (e) { console.error(e); }
  };

  const handleSync = async (id: string) => {
    setSyncing(id);
    try { await syncIntegration(id); loadData(); } catch (e) { console.error(e); }
    setSyncing(null);
  };

  const categoryColors: Record<string, string> = {
    hris: "bg-purple-100 text-purple-700",
    sso: "bg-blue-100 text-blue-700",
    payroll: "bg-green-100 text-green-700",
    mdm: "bg-orange-100 text-orange-700",
    communication: "bg-indigo-100 text-indigo-700",
    other: "bg-gray-100 text-gray-700",
  };

  const statusColors: Record<string, string> = {
    connected: "bg-green-100 text-green-700",
    pending: "bg-yellow-100 text-yellow-700",
    error: "bg-red-100 text-red-700",
    disconnected: "bg-gray-100 text-gray-700",
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Blocks className="w-8 h-8 text-amber-500" />
            <h1 className="text-3xl font-bold text-gray-900">Integration Hub</h1>
          </div>
          <button
            onClick={handleSeed}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition"
          >
            <Plug className="w-4 h-4" />
            Seed Default Connectors
          </button>
        </div>

        {/* Overview */}
        {overview && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl p-4 shadow-sm border">
              <div className="text-2xl font-bold">{overview.total_integrations}</div>
              <div className="text-sm text-gray-500">Total Connectors</div>
            </div>
            <div className="bg-green-50 rounded-xl p-4 shadow-sm border border-green-100">
              <div className="text-2xl font-bold text-green-600">{overview.connected_count}</div>
              <div className="text-sm text-green-500">Connected</div>
            </div>
            <div className="bg-red-50 rounded-xl p-4 shadow-sm border border-red-100">
              <div className="text-2xl font-bold text-red-600">{overview.error_count}</div>
              <div className="text-sm text-red-500">Errors</div>
            </div>
            <div className="bg-yellow-50 rounded-xl p-4 shadow-sm border border-yellow-100">
              <div className="text-2xl font-bold text-yellow-600">{overview.pending_actions}</div>
              <div className="text-sm text-yellow-500">Pending Actions</div>
            </div>
          </div>
        )}

        {/* Integrations Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {integrations.map((i: any) => (
            <div key={i.id} className="bg-white rounded-xl shadow-sm border p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-gray-900">{i.name}</h3>
                  <p className="text-xs text-gray-500 mt-0.5">{i.provider}</p>
                </div>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[i.status] || statusColors.pending}`}>
                  {i.status}
                </span>
              </div>
              <div className="flex items-center gap-2 mb-3">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${categoryColors[i.category] || categoryColors.other}`}>
                  {i.category}
                </span>
                <span className="text-xs text-gray-400">{i.auth_type}</span>
              </div>
              {i.last_sync_at && (
                <div className="text-xs text-gray-400 mb-3">
                  Last sync: {new Date(i.last_sync_at).toLocaleString()}
                </div>
              )}
              <button
                onClick={() => handleSync(i.id)}
                disabled={syncing === i.id}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-lg text-xs font-medium transition disabled:opacity-50"
              >
                <RefreshCw className={`w-3 h-3 ${syncing === i.id ? "animate-spin" : ""}`} />
                {syncing === i.id ? "Syncing..." : "Sync"}
              </button>
            </div>
          ))}
          {integrations.length === 0 && (
            <div className="col-span-full text-center py-12 text-gray-400">
              No integrations yet. Click "Seed Default Connectors" to add the catalog.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
