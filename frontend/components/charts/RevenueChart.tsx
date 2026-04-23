"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export function RevenueChart({ data }: { data: Array<{ date: string; count: number; revenue?: number }> }) {
  return (
    <div style={{ width: "100%", height: 280 }}>
      <ResponsiveContainer>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="revGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.35} />
              <stop offset="95%" stopColor="#7C3AED" stopOpacity={0.03} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#E5E0FF" vertical={false} />
          <XAxis dataKey="date" tick={{ fill: "#4A4A68", fontSize: 12 }} />
          <YAxis tick={{ fill: "#4A4A68", fontSize: 12 }} />
          <Tooltip contentStyle={{ border: "1.5px solid #E5E0FF", borderRadius: 10 }} />
          <Area type="monotone" dataKey="count" stroke="#7C3AED" fill="url(#revGradient)" strokeWidth={2.5} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
