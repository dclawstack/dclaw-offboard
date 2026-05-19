"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X, UserX } from "lucide-react";
import content from "@/data/landing-content.json";
import config from "@/data/app-config.json";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg flex items-center justify-center transition-colors" style={{ backgroundColor: content.app.color }}>
              <UserX className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-bold text-gray-900">{content.app.name}</span>
            <span className="hidden sm:inline text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">{content.app.category}</span>
          </Link>

          <div className="hidden md:flex items-center gap-6">
            {config.navigation.links.slice(0, 4).map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                {link.text}
              </Link>
            ))}
            <Link
              href="/checklists/create"
              className="text-sm px-4 py-2 rounded-lg text-white font-medium transition-all hover:opacity-90"
              style={{ backgroundColor: content.app.color }}
            >
              {content.hero.ctaPrimary.text}
            </Link>
          </div>

          <button className="md:hidden p-2 rounded-md text-gray-600" onClick={() => setOpen(!open)}>
            {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {open && (
          <div className="md:hidden pb-4 space-y-2">
            {config.navigation.links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="block px-3 py-2 rounded-md text-sm text-gray-600 hover:bg-gray-50"
                onClick={() => setOpen(false)}
              >
                {link.text}
              </Link>
            ))}
            <Link
              href="/checklists/create"
              className="block px-3 py-2 rounded-md text-sm text-white font-medium text-center"
              style={{ backgroundColor: content.app.color }}
              onClick={() => setOpen(false)}
            >
              {content.hero.ctaPrimary.text}
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
