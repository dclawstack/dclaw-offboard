"use client";

import dynamic from "next/dynamic";

const OffboardCopilot = dynamic(
  () => import("@/components/offboard-copilot"),
  { ssr: false }
);

export function CopilotProvider() {
  return <OffboardCopilot />;
}
