"use client";

import { PropsWithChildren } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { useAuth } from "@/lib/hooks/useAuth";

export default function DashboardLayout({ children }: PropsWithChildren) {
  const { user, userType, tokenPayload } = useAuth();

  return (
    <div className="dashboard-root">
      <Sidebar
        userName={user?.name}
        role={(user as { role?: string })?.role}
        userType={userType}
        eventId={tokenPayload?.event_id}
      />
      <div className="dashboard-content-area">
        <Topbar userName={user?.name} />
        <div className="dashboard-page-container">{children}</div>
      </div>
    </div>
  );
}
