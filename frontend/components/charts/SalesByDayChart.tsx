"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function SalesByDayChart({ data }: { data: Array<{ date: string; count: number }> }) {
  return (
    <div style={{ width: "100%", height: 230 }}>
      <ResponsiveContainer>
        <AreaChart data={data}>
          <CartesianGrid stroke="#E5E0FF" vertical={false} />
          <XAxis dataKey="date" tick={{ fill: "#4A4A68", fontSize: 12 }} />
          <YAxis tick={{ fill: "#4A4A68", fontSize: 12 }} />
          <Tooltip contentStyle={{ border: "1.5px solid #E5E0FF", borderRadius: 10 }} />
          <Area type="monotone" dataKey="count" fill="#A78BFA" stroke="#5B21B6" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
