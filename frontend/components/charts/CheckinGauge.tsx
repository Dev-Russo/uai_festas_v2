"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

export function CheckinGauge({ rate }: { rate: number }) {
  const value = Math.max(0, Math.min(rate * 100, 100));
  const data = [
    { name: "Check-in", value },
    { name: "Restante", value: 100 - value },
  ];

  return (
    <div style={{ width: "100%", height: 220, position: "relative" }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie data={data} dataKey="value" innerRadius={60} outerRadius={80} startAngle={90} endAngle={-270}>
            {data.map((entry, index) => (
              <Cell key={entry.name + index} fill={index === 0 ? "#059669" : "#D1FAE5"} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        <strong style={{ fontFamily: "var(--font-mono)", color: "#059669", fontSize: "1.45rem" }}>
          {value.toFixed(1)}%
        </strong>
      </div>
    </div>
  );
}
