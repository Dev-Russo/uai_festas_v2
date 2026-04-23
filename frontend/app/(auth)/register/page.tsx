"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";

export default function RegisterPage() {
  const router = useRouter();
  const [success, setSuccess] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const params = new URLSearchParams(window.location.search);
    setSuccess(params.get("success") === "1");
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    if (password.length < 8) {
      setError("A senha precisa ter no minimo 8 caracteres.");
      return;
    }
    if (password !== confirmPassword) {
      setError("As senhas nao conferem.");
      return;
    }

    setLoading(true);
    try {
      await api.register(name, email, password);
      router.push("/login?success=1");
    } catch {
      setError("Nao foi possivel criar a conta.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-brand-panel">
        <div className="auth-brand-overlay" />
        <div className="auth-brand-content">
          <p>Uai Festas</p>
          <h1>Comece agora e tenha seu centro de comando para eventos.</h1>
          <span>Cadastro rapido para voce acompanhar vendas e performance em minutos.</span>
        </div>
      </section>

      <section className="auth-form-panel">
        <form className="auth-form card" onSubmit={handleSubmit}>
          <div>
            <h2>Crie sua conta</h2>
            <small>Preencha os dados para comecar.</small>
          </div>

          {success ? <p className="inline-success">Conta criada com sucesso. Agora faca login.</p> : null}

          <Input label="Nome completo" value={name} onChange={(e) => setName(e.target.value)} required />
          <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input label="Senha" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Input
            label="Confirmar senha"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          {error ? <p className="inline-error">{error}</p> : null}

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? <span style={{ display: "inline-flex", gap: 8, alignItems: "center" }}><Spinner /> Criando...</span> : "Criar conta"}
          </Button>

          <p className="auth-link-row">
            Ja tem conta? <Link href="/login">Entrar</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
