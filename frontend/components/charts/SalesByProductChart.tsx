"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function SalesByProductChart({ data }: { data: Array<{ productName: string; count: number }> }) {
  return (
    <div style={{ width: "100%", height: 270 }}>
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical">
          <CartesianGrid stroke="#E5E0FF" horizontal={false} />
          <XAxis type="number" tick={{ fill: "#4A4A68", fontSize: 12 }} />
          <YAxis dataKey="productName" type="category" tick={{ fill: "#4A4A68", fontSize: 12 }} width={90} />
          <Tooltip contentStyle={{ border: "1.5px solid #E5E0FF", borderRadius: 10 }} />
          <Bar dataKey="count" fill="#7C3AED" radius={[8, 8, 8, 8]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
