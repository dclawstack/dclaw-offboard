"use client";

import Link from "next/link";
import { ArrowLeft, ShieldCheck } from "lucide-react";

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to home
        </Link>

        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5 text-indigo-600" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900">Privacy Policy</h1>
        </div>

        <p className="text-sm text-gray-500 mb-10">Last updated: May 28, 2026</p>

        <div className="prose prose-gray max-w-none space-y-6 text-gray-600 leading-relaxed">
          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">1. Data We Collect</h2>
            <p>
              DClaw Offboard processes employee personal data only as instructed by our
              customers (the data controller). This may include name, contact info, role,
              tenure, employment-history events, and access logs needed to execute offboarding
              workflows.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">2. How We Use Data</h2>
            <p>
              Data is used solely to provide the service: generating checklists, revoking access,
              producing compliance reports, and surfacing analytics to authorized personnel at
              the customer organization.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">3. GDPR &amp; CCPA</h2>
            <p>
              Employees covered by GDPR or CCPA may exercise rights of access, correction,
              deletion, and portability through their employer. Contact your HR team to initiate
              a request; we route it through the customer&rsquo;s administrator.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">4. Retention</h2>
            <p>
              Compliance artifacts (audit logs, exit-interview transcripts) are retained per the
              customer&rsquo;s configured retention schedule. Defaults align with SOC2 and EEOC
              recordkeeping standards.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">5. Contact</h2>
            <p>
              Privacy inquiries: <a className="text-indigo-600 hover:underline" href="mailto:privacy@dclaw.example">privacy@dclaw.example</a>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
