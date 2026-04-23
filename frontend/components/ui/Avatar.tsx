export function Avatar({ name }: { name?: string }) {
  const initial = (name?.trim()?.[0] ?? "U").toUpperCase();
  return (
    <span
      style={{
        width: 34,
        height: 34,
        borderRadius: 999,
        display: "grid",
        placeItems: "center",
        background: "var(--primary-glow)",
        color: "var(--primary)",
        fontWeight: 700,
      }}
    >
      {initial}
    </span>
  );
}
