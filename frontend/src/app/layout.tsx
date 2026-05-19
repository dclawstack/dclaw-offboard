import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { CopilotProvider } from "@/components/copilot-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "DClaw Offboard — AI-Powered Offboarding",
  description:
    "Secure offboarding platform with AI copilot, smart checklists, asset recovery, access revocation, exit interviews, and compliance automation.",
  keywords: ["offboarding", "HR", "compliance", "asset recovery", "exit interview", "AI"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <CopilotProvider />
      </body>
    </html>
  );
}
