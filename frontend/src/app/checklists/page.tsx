"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Plus, Search, ClipboardCheck, Trash2, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Checklist {
  id: string;
  employee_name: string;
  employee_email: string;
  employee_role: string;
  department: string;
  last_day: string;
  status: string;
  created_at: string;
}

export default function ChecklistsPage() {
  const [checklists, setChecklists] = useState<Checklist[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChecklists();
  }, []);

  async function fetchChecklists() {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${apiBase}/api/v1/checklists`);
      const data = await res.json();
      setChecklists(data.items || []);
    } catch (e) {
      console.error("Failed to fetch checklists:", e);
    } finally {
      setLoading(false);
    }
  }

  const filtered = checklists.filter(
    (c) =>
      c.employee_name.toLowerCase().includes(search.toLowerCase()) ||
      c.department.toLowerCase().includes(search.toLowerCase()) ||
      c.employee_email.toLowerCase().includes(search.toLowerCase())
  );

  const statusColor = (s: string) => {
    switch (s) {
      case "completed": return "bg-green-100 text-green-700";
      case "in_progress": return "bg-blue-100 text-blue-700";
      default: return "bg-gray-100 text-gray-600";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Offboarding Checklists</h1>
            <p className="text-gray-500 mt-1">Manage and track employee offboarding journeys</p>
          </div>
          <Link href="/checklists/create">
            <Button className="flex items-center gap-2">
              <Plus className="w-4 h-4" /> New Checklist
            </Button>
          </Link>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-4">
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="Search by name, department, or email..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-12 text-gray-500">Loading checklists...</div>
            ) : filtered.length === 0 ? (
              <div className="text-center py-12">
                <ClipboardCheck className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">No checklists found. Create your first one!</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100">
                      <th className="text-left py-3 px-4 font-medium text-gray-500">Employee</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-500">Role</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-500">Department</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-500">Last Day</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-500">Status</th>
                      <th className="text-right py-3 px-4 font-medium text-gray-500">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((c) => (
                      <tr key={c.id} className="border-b border-gray-50 hover:bg-gray-50/50">
                        <td className="py-3 px-4">
                          <div className="font-medium text-gray-900">{c.employee_name}</div>
                          <div className="text-gray-500 text-xs">{c.employee_email}</div>
                        </td>
                        <td className="py-3 px-4 text-gray-600">{c.employee_role}</td>
                        <td className="py-3 px-4 text-gray-600 capitalize">{c.department}</td>
                        <td className="py-3 px-4 text-gray-600">{c.last_day}</td>
                        <td className="py-3 px-4">
                          <Badge className={statusColor(c.status)}>
                            {c.status.replace("_", " ")}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <Link href={`/checklists/${c.id}`} className="text-indigo-600 hover:text-indigo-800 text-xs font-medium inline-flex items-center gap-1">
                            View <ArrowRight className="w-3 h-3" />
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
