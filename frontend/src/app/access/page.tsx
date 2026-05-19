"use client";

import { ArrowLeft, ShieldOff, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AccessPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <Link href="/" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-4 h-4" /> Back to home
        </Link>

        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="w-16 h-16 rounded-2xl bg-red-100 flex items-center justify-center mx-auto mb-4">
            <ShieldOff className="w-8 h-8 text-red-500" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Access Revocation</h1>
          <p className="text-gray-500 text-lg">
            Revoke system access across 20+ integrated platforms. Generate audit trails for compliance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {[
            { system: "Google Workspace (Email)", type: "email", status: "ready" },
            { system: "Slack", type: "saas", status: "ready" },
            { system: "GitHub Enterprise", type: "saas", status: "ready" },
            { system: "AWS IAM", type: "cloud", status: "ready" },
            { system: "VPN Access", type: "vpn", status: "ready" },
            { system: "Building Access", type: "physical", status: "pending" },
            { system: "HRIS / Payroll", type: "saas", status: "ready" },
            { system: "Salesforce CRM", type: "saas", status: "ready" },
            { system: "Jira / Confluence", type: "saas", status: "ready" },
          ].map((s) => (
            <Card key={s.system} className="hover:shadow-md transition-shadow">
              <CardContent className="p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900 text-sm">{s.system}</p>
                  <p className="text-xs text-gray-500 capitalize">{s.type}</p>
                </div>
                <div className="flex items-center gap-2">
                  <Badge className={s.status === "ready" ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}>
                    {s.status}
                  </Badge>
                  <ShieldCheck className="w-5 h-5 text-green-400" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Audit Trail</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500">
              Access revocation history is automatically logged with timestamps, 
              revoked-by attribution, and system-level detail. Navigate to a specific 
              offboarding checklist to view its associated audit trail.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
