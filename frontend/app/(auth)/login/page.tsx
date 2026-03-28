"use client";

import Link from "next/link";
import { Eye, EyeOff, Mail, Ticket } from "lucide-react";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { saveToken } from "@/lib/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await api.login(email, password);
      saveToken(result.token);
      if (!remember) {
        document.cookie = "token=; path=/; max-age=0; samesite=lax";
      }
      router.push("/dashboard");
    } catch {
      setError("Email ou senha invalidos.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-brand-panel">
        <div className="auth-brand-overlay" />
        <div className="auth-brand-content">
          <p><Ticket size={20} /> EventOS</p>
          <h1>Controle completo de eventos em uma experiencia premium.</h1>
          <span>Seu backstage digital para vendas, lotes e decisao orientada por dados.</span>
        </div>
      </section>

      <section className="auth-form-panel">
        <form className="auth-form card" onSubmit={handleSubmit}>
          <div>
            <p className="auth-logo">EventOS</p>
            <h2>Bem-vindo de volta</h2>
            <small>Faca login para gerenciar seus eventos</small>
          </div>

          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="voce@evento.com"
            rightSlot={<Mail size={16} color="#7C3AED" />}
            required
          />

          <Input
            label="Senha"
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="********"
            rightSlot={
              <button type="button" onClick={() => setShowPassword((prev) => !prev)} style={{ border: 0, background: "transparent", cursor: "pointer" }}>
                {showPassword ? <EyeOff size={16} color="#7C3AED" /> : <Eye size={16} color="#7C3AED" />}
              </button>
            }
            required
          />

          <label className="remember-row">
            <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} />
            <span>Lembrar de mim</span>
          </label>

          {error ? <p className="inline-error">{error}</p> : null}

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? <span style={{ display: "inline-flex", gap: 8, alignItems: "center" }}><Spinner /> Entrando...</span> : "Entrar"}
          </Button>

          <p className="auth-link-row">
            Nao tem conta? <Link href="/register">Cadastre-se</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
