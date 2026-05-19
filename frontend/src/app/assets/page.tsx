"use client";

import { useState, useEffect } from "react";
import { Package, Plus, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import config from "@/data/app-config.json";

interface Asset {
  id: string;
  name: string;
  asset_type: string;
  serial_number: string | null;
  assigned_to: string | null;
  status: string;
  value: number | null;
}

export default function AssetsPage() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    name: "",
    asset_type: "laptop",
    serial_number: "",
    assigned_to: "",
    value: "",
  });

  useEffect(() => {
    fetchAssets();
  }, []);

  async function fetchAssets() {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${apiBase}/api/v1/assets`);
      const data = await res.json();
      setAssets(data.items || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function createAsset(e: React.FormEvent) {
    e.preventDefault();
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      await fetch(`${apiBase}/api/v1/assets`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          value: form.value ? parseFloat(form.value) : null,
        }),
      });
      setShowForm(false);
      setForm({
        name: "",
        asset_type: "laptop",
        serial_number: "",
        assigned_to: "",
        value: "",
      });
      fetchAssets();
    } catch (e) {
      console.error(e);
    }
  }

  const totalValue = assets.reduce((sum, a) => sum + (a.value || 0), 0);
  const assignedCount = assets.filter((a) => a.status === "assigned").length;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Asset Recovery &amp; Inventory
            </h1>
            <p className="text-gray-500 mt-1">
              Track and manage company assets during offboarding
            </p>
          </div>
          <Button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" /> Add Asset
          </Button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          {[
            { label: "Total Assets", value: assets.length },
            { label: "Currently Assigned", value: assignedCount },
            {
              label: "Total Value",
              value: `$${totalValue.toLocaleString()}`,
            },
          ].map((s) => (
            <Card key={s.label}>
              <CardContent className="py-4">
                <p className="text-sm text-gray-500">{s.label}</p>
                <p className="text-2xl font-bold text-gray-900">{s.value}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {showForm && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Register New Asset</CardTitle>
            </CardHeader>
            <CardContent>
              <form
                onSubmit={createAsset}
                className="grid grid-cols-1 sm:grid-cols-3 gap-4"
              >
                <div className="space-y-2">
                  <label className="text-sm font-medium">Asset Name *</label>
                  <Input
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder='MacBook Pro 16"'
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Type *</label>
                  <select
                    required
                    value={form.asset_type}
                    onChange={(e) =>
                      setForm({ ...form, asset_type: e.target.value })
                    }
                    className="w-full px-3 py-2 rounded-lg border border-gray-200 text-sm"
                  >
                    {config.assetTypes.map((t) => (
                      <option key={t} value={t}>
                        {t.replace("_", " ")}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Serial Number</label>
                  <Input
                    value={form.serial_number}
                    onChange={(e) =>
                      setForm({ ...form, serial_number: e.target.value })
                    }
                    placeholder="SN-12345"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Assigned To</label>
                  <Input
                    value={form.assigned_to}
                    onChange={(e) =>
                      setForm({ ...form, assigned_to: e.target.value })
                    }
                    placeholder="Employee name"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Value ($)</label>
                  <Input
                    value={form.value}
                    onChange={(e) =>
                      setForm({ ...form, value: e.target.value })
                    }
                    placeholder="2000"
                    type="number"
                  />
                </div>
                <div className="flex items-end">
                  <Button type="submit" className="w-full">
                    Save Asset
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardContent className="p-0">
            {loading ? (
              <div className="text-center py-12 text-gray-500">Loading...</div>
            ) : assets.length === 0 ? (
              <div className="text-center py-12">
                <Package className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">No assets registered yet.</p>
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-100">
                    <th className="text-left py-3 px-4 font-medium text-gray-500">
                      Asset
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-gray-500">
                      Type
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-gray-500">
                      Serial #
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-gray-500">
                      Assigned To
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-gray-500">
                      Status
                    </th>
                    <th className="text-right py-3 px-4 font-medium text-gray-500">
                      Value
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {assets.map((a) => (
                    <tr
                      key={a.id}
                      className="border-b border-gray-50 hover:bg-gray-50/50"
                    >
                      <td className="py-3 px-4 font-medium text-gray-900">
                        {a.name}
                      </td>
                      <td className="py-3 px-4 text-gray-600 capitalize">
                        {a.asset_type}
                      </td>
                      <td className="py-3 px-4 text-gray-500">
                        {a.serial_number || "—"}
                      </td>
                      <td className="py-3 px-4 text-gray-600">
                        {a.assigned_to || "—"}
                      </td>
                      <td className="py-3 px-4">
                        <Badge
                          className={
                            a.status === "assigned"
                              ? "bg-blue-100 text-blue-700"
                              : "bg-green-100 text-green-700"
                          }
                        >
                          {a.status}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-right text-gray-900">
                        ${a.value?.toLocaleString() || "0"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
