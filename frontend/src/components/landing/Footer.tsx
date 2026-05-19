"use client";

import Link from "next/link";
import { UserX } from "lucide-react";
import content from "@/data/landing-content.json";

export default function Footer() {
  const { footer, app } = content;

  return (
    <footer className="bg-gray-900 text-gray-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: app.color }}>
              <UserX className="w-4 h-4 text-white" />
            </div>
            <span className="text-white font-semibold">{app.name}</span>
          </div>

          <div className="flex flex-wrap items-center gap-6">
            {footer.links.map((link) => (
              <Link key={link.href} href={link.href} className="text-sm hover:text-white transition-colors">
                {link.text}
              </Link>
            ))}
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm">
          {footer.copyright}
        </div>
      </div>
    </footer>
  );
}
