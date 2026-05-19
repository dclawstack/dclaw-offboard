"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, Circle, Clock, ShieldOff, Package } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ProgressTracker } from "@/components/checklist-tracker";
import config from "@/data/app-config.json";

interface Task {
  id: string;
  title: string;
  category: string;
  assigned_to: string | null;
  status: string;
  due_date: string | null;
}

interface Checklist {
  id: string;
  employee_name: string;
  employee_email: string;
  employee_role: string;
  department: string;
  last_day: string;
  status: string;
  notes: string | null;
  tasks: Task[];
  completion_percent: number;
}

export default function ChecklistDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [checklist, setChecklist] = useState<Checklist | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChecklist();
  }, [id]);

  async function fetchChecklist() {
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const res = await fetch(`${apiBase}/api/v1/checklists/${id}`);
      const data = await res.json();
      setChecklist(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function toggleTask(taskId: string, currentStatus: string) {
    const newStatus = currentStatus === "completed" ? "pending" : "completed";
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      await fetch(`${apiBase}/api/v1/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
      fetchChecklist();
    } catch (e) {
      console.error(e);
    }
  }

  const categoryColor = (cat: string) => {
    const found = config.taskCategories.find((c) => c.value === cat);
    return found?.color || "#6B7280";
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center text-gray-500">Loading...</div>;
  if (!checklist) return <div className="min-h-screen flex items-center justify-center text-gray-500">Checklist not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/checklists" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to checklists
        </Link>

        {/* Header */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{checklist.employee_name}</h1>
              <p className="text-gray-500">{checklist.employee_role} · {checklist.department} · Last day: {checklist.last_day}</p>
            </div>
            <Badge className={checklist.status === "completed" ? "bg-green-100 text-green-700" : "bg-blue-100 text-blue-700"}>
              {checklist.status.replace("_", " ")}
            </Badge>
          </div>
          {checklist.completion_percent !== undefined && (
            <div className="mt-4">
              <ProgressTracker percent={checklist.completion_percent} />
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Tasks */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Tasks ({checklist.tasks.length})</CardTitle>
              </CardHeader>
              <CardContent className="space-y-1">
                {checklist.tasks.map((task) => (
                  <div
                    key={task.id}
                    className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                    onClick={() => toggleTask(task.id, task.status)}
                  >
                    {task.status === "completed" ? (
                      <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                    ) : (
                      <Circle className="w-5 h-5 text-gray-300 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm ${task.status === "completed" ? "text-gray-400 line-through" : "text-gray-900"}`}>
                        {task.title}
                      </p>
                      {task.assigned_to && (
                        <p className="text-xs text-gray-400 mt-0.5">Assigned to: {task.assigned_to}</p>
                      )}
                    </div>
                    <span
                      className="text-[10px] font-medium px-2 py-0.5 rounded-full flex-shrink-0"
                      style={{ backgroundColor: categoryColor(task.category) + "15", color: categoryColor(task.category) }}
                    >
                      {task.category}
                    </span>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Link href="/access">
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <ShieldOff className="w-4 h-4" /> Revoke Access
                  </Button>
                </Link>
                <Link href="/assets">
                  <Button variant="outline" className="w-full justify-start gap-2">
                    <Package className="w-4 h-4" /> Track Assets
                  </Button>
                </Link>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <div>
                  <p className="text-gray-500">Email</p>
                  <p className="text-gray-900">{checklist.employee_email}</p>
                </div>
                <div>
                  <p className="text-gray-500">Role</p>
                  <p className="text-gray-900">{checklist.employee_role}</p>
                </div>
                <div>
                  <p className="text-gray-500">Department</p>
                  <p className="text-gray-900 capitalize">{checklist.department}</p>
                </div>
                <div>
                  <p className="text-gray-500">Last Day</p>
                  <p className="text-gray-900">{checklist.last_day}</p>
                </div>
                {checklist.notes && (
                  <div>
                    <p className="text-gray-500">Notes</p>
                    <p className="text-gray-900">{checklist.notes}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
