"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

export function CancellationGauge({ rate }: { rate: number }) {
  const value = Math.max(0, Math.min(rate * 100, 100));
  const data = [
    { name: "Cancelamento", value },
    { name: "Restante", value: 100 - value },
  ];

  return (
    <div style={{ width: "100%", height: 220, position: "relative" }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie data={data} dataKey="value" innerRadius={60} outerRadius={80} startAngle={90} endAngle={-270}>
            {data.map((entry, index) => (
              <Cell key={entry.name + index} fill={index === 0 ? "#7C3AED" : "#DDD6FE"} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        <strong style={{ fontFamily: "var(--font-mono)", color: "var(--primary)", fontSize: "1.45rem" }}>
          {value.toFixed(1)}%
        </strong>
      </div>
    </div>
  );
}
