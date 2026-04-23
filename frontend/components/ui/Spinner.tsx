export function Spinner() {
  return (
    <span
      style={{
        width: 16,
        height: 16,
        border: "2px solid rgba(255,255,255,0.5)",
        borderTopColor: "white",
        borderRadius: "50%",
        display: "inline-block",
        animation: "spin 0.9s linear infinite",
      }}
    />
  );
}
