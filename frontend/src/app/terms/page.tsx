"use client";

import Link from "next/link";
import { ArrowLeft, FileText } from "lucide-react";

export default function TermsPage() {
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
            <FileText className="w-5 h-5 text-indigo-600" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900">Terms of Service</h1>
        </div>

        <p className="text-sm text-gray-500 mb-10">Last updated: May 28, 2026</p>

        <div className="prose prose-gray max-w-none space-y-6 text-gray-600 leading-relaxed">
          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">1. Acceptance</h2>
            <p>
              By accessing DClaw Offboard, you agree to these terms on behalf of your
              organization. If you do not have authority to bind your organization, do not use
              the service.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">2. Service Description</h2>
            <p>
              DClaw Offboard provides offboarding automation, risk assessment, compliance
              reporting, and related tools. Service availability targets are defined in your
              order form or master agreement.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">3. Acceptable Use</h2>
            <p>
              Do not attempt to reverse-engineer the service, exceed documented rate limits, or
              upload content that violates applicable law or third-party rights.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">4. Customer Data</h2>
            <p>
              You retain all rights to your data. We process it according to our
              {" "}<Link href="/privacy" className="text-indigo-600 hover:underline">Privacy Policy</Link>{" "}
              and DPA.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">5. Termination</h2>
            <p>
              Either party may terminate per the master agreement. Upon termination we return
              or delete customer data per the agreed retention schedule.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">6. Contact</h2>
            <p>
              Legal inquiries: <a className="text-indigo-600 hover:underline" href="mailto:legal@dclaw.example">legal@dclaw.example</a>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
