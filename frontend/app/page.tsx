"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken, saveToken } from "./lib/auth";
import { login } from "./lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (getToken()) {
      router.replace("/events");
    }
  }, [router]);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const token = await login(email, password);
      saveToken(token);
      router.push("/events");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Erro inesperado ao autenticar.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      className="page-shell grid grid-cols-1 lg:grid-cols-[1.1fr_1fr]"
      style={{
        minHeight: "calc(100vh - 4rem)",
        gap: "1rem",
        alignItems: "center",
      }}
    >
      <section style={{ padding: "0.5rem 0.6rem" }}>
        <p style={{ margin: 0, fontFamily: "var(--font-plex-mono)", color: "var(--app-accent-strong)" }}>
          UAI FESTAS PLATFORM
        </p>
        <h1 style={{ fontSize: "clamp(2rem, 4vw, 3.4rem)", lineHeight: 1.05, margin: "0.6rem 0 0.8rem" }}>
          Seu painel de eventos,
          <br />
          vendas e decisao rapida.
        </h1>
        <p className="muted" style={{ maxWidth: 520, fontSize: "1.02rem" }}>
          Entre para acompanhar os seus eventos em tempo real, entender resultados e agir rapido com base nos
          dados do seu dashboard.
        </p>
      </section>

      <section className="card" style={{ padding: "1.4rem" }}>
        <h2 style={{ margin: 0 }}>Entrar na sua conta</h2>
        <p className="muted" style={{ marginTop: "0.35rem", marginBottom: "1rem" }}>
          Use o mesmo email e senha do seu backend.
        </p>

        <form onSubmit={handleLogin} style={{ display: "grid", gap: "0.8rem" }}>
          <label style={{ display: "grid", gap: "0.4rem" }}>
            <span>Email</span>
            <input
              className="input-field"
              type="email"
              placeholder="voce@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label style={{ display: "grid", gap: "0.4rem" }}>
            <span>Senha</span>
            <input
              className="input-field"
              type="password"
              placeholder="********"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          {error ? (
            <p style={{ margin: 0, color: "var(--app-danger)", fontSize: "0.92rem" }}>
              {error}
            </p>
          ) : null}

          <button type="submit" className="button-primary" disabled={loading}>
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </section>
    </main>
  );
}
