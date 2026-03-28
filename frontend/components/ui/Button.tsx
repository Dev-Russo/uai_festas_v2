import { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "ghost" | "danger";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  fullWidth?: boolean;
};

export function Button({ variant = "primary", fullWidth, style, ...props }: Props) {
  const className = variant === "primary" ? "button-primary" : "button-ghost";
  const mergedStyle = {
    ...(fullWidth ? { width: "100%" } : {}),
    ...(variant === "danger" ? { borderColor: "var(--danger)", color: "var(--danger)" } : {}),
    ...style,
  };

  return <button {...props} className={className} style={mergedStyle} />;
}
