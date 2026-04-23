"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { Commissioner, CommissionerRole, CreateCommissionerDTO } from "@/types";
import { Table } from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

const ROLE_LABELS: Record<CommissionerRole, string> = {
  commissioner: "Comissário",
  commissioner_admin: "Comissário Admin",
};

interface FormState {
  username: string;
  name: string;
  password: string;
  role: CommissionerRole;
  fullAccess: boolean;
}

const EMPTY_FORM: FormState = {
  username: "",
  name: "",
  password: "",
  role: "commissioner",
  fullAccess: false,
};

const thStyle: React.CSSProperties = {
  padding: "10px 16px",
  textAlign: "left",
  fontSize: 13,
  fontWeight: 600,
  color: "var(--text-secondary)",
  borderBottom: "1px solid var(--border)",
  background: "var(--surface-2)",
};

const tdStyle: React.CSSProperties = {
  padding: "12px 16px",
  fontSize: 14,
  borderBottom: "1px solid var(--border)",
  verticalAlign: "middle",
};

export default function CommissionersPage() {
  const { id } = useParams<{ id: string }>();
  const [commissioners, setCommissioners] = useState<Commissioner[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<Commissioner | null>(null);
  const [form, setForm] = useState<FormState>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getCommissioners(id)
      .then(setCommissioners)
      .catch(() => setError("Erro ao carregar comissários."))
      .finally(() => setLoading(false));
  }, [id]);

  function openCreate() {
    setEditTarget(null);
    setForm(EMPTY_FORM);
    setFormError(null);
    setModalOpen(true);
  }

  function openEdit(commissioner: Commissioner) {
    setEditTarget(commissioner);
    setForm({
      username: commissioner.username,
      name: commissioner.name,
      password: "",
      role: commissioner.role,
      fullAccess: commissioner.fullAccess,
    });
    setFormError(null);
    setModalOpen(true);
  }

  async function handleSave() {
    setFormError(null);
    setSaving(true);
    try {
      if (editTarget) {
        const updated = await api.updateCommissioner(id, editTarget.id, {
          name: form.name,
          role: form.role,
          fullAccess: form.fullAccess,
          ...(form.password ? { password: form.password } : {}),
        });
        setCommissioners((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
      } else {
        const created = await api.createCommissioner(id, form as CreateCommissionerDTO);
        setCommissioners((prev) => [...prev, created]);
      }
      setModalOpen(false);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erro ao salvar.";
      try {
        const parsed = JSON.parse(msg) as { detail?: string };
        setFormError(parsed.detail ?? msg);
      } catch {
        setFormError(msg);
      }
    } finally {
      setSaving(false);
    }
  }

  async function handleToggleActive(commissioner: Commissioner) {
    try {
      const updated = await api.updateCommissioner(id, commissioner.id, { isActive: !commissioner.isActive });
      setCommissioners((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
    } catch {
      setError("Erro ao atualizar status.");
    }
  }

  async function handleDelete(commissioner: Commissioner) {
    if (!confirm(`Remover o comissário "${commissioner.username}"?`)) return;
    try {
      await api.deleteCommissioner(id, commissioner.id);
      setCommissioners((prev) => prev.filter((c) => c.id !== commissioner.id));
    } catch {
      setError("Erro ao remover comissário.");
    }
  }

  return (
    <div className="page-content">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <div>
          <h1>Comissários</h1>
          <p className="muted">Gerencie os comissários deste evento</p>
        </div>
        <Button onClick={openCreate}>+ Novo Comissário</Button>
      </div>

      {error && <p className="inline-error">{error}</p>}

      {loading ? (
        <p className="muted">Carregando...</p>
      ) : commissioners.length === 0 ? (
        <p className="muted">Nenhum comissário cadastrado.</p>
      ) : (
        <Table>
          <thead>
            <tr>
              <th style={thStyle}>Username</th>
              <th style={thStyle}>Nome</th>
              <th style={thStyle}>Cargo</th>
              <th style={thStyle}>Acesso Total</th>
              <th style={thStyle}>Status</th>
              <th style={thStyle}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {commissioners.map((c) => (
              <tr key={c.id}>
                <td style={tdStyle}><span style={{ fontFamily: "monospace" }}>{c.username}</span></td>
                <td style={tdStyle}>{c.name}</td>
                <td style={tdStyle}>
                  <Badge status={c.role === "commissioner_admin" ? "checked_in" : "draft"}>
                    {ROLE_LABELS[c.role]}
                  </Badge>
                </td>
                <td style={tdStyle}>
                  {c.fullAccess
                    ? <Badge status="active">Sim</Badge>
                    : <span className="muted">—</span>}
                </td>
                <td style={tdStyle}>
                  <Badge status={c.isActive ? "active" : "cancelled"}>
                    {c.isActive ? "Ativo" : "Inativo"}
                  </Badge>
                </td>
                <td style={tdStyle}>
                  <span style={{ display: "flex", gap: 8 }}>
                    <Button variant="ghost" onClick={() => openEdit(c)}>Editar</Button>
                    <Button variant="ghost" onClick={() => handleToggleActive(c)}>
                      {c.isActive ? "Desativar" : "Ativar"}
                    </Button>
                    <Button variant="danger" onClick={() => handleDelete(c)}>Remover</Button>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editTarget ? "Editar Comissário" : "Novo Comissário"}>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Input
            label="Username"
            value={form.username}
            onChange={(e) => setForm((f) => ({ ...f, username: e.target.value }))}
            placeholder="username_comissario"
            disabled={Boolean(editTarget)}
            required
          />
          <Input
            label="Nome"
            value={form.name}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            placeholder="Nome completo"
            required
          />
          <Input
            label={editTarget ? "Nova Senha (deixe em branco para manter)" : "Senha"}
            type="password"
            value={form.password}
            onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
            placeholder="********"
            required={!editTarget}
          />

          <div>
            <label style={{ display: "block", marginBottom: 6, fontSize: 14, fontWeight: 500 }}>Cargo</label>
            <select
              value={form.role}
              onChange={(e) => setForm((f) => ({ ...f, role: e.target.value as CommissionerRole }))}
              style={{ width: "100%", padding: "8px 12px", borderRadius: 8, border: "1px solid var(--border)", background: "var(--card)", color: "var(--text)" }}
            >
              <option value="commissioner">Comissário</option>
              <option value="commissioner_admin">Comissário Admin</option>
            </select>
          </div>

          {form.role === "commissioner_admin" && (
            <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={form.fullAccess}
                onChange={(e) => setForm((f) => ({ ...f, fullAccess: e.target.checked }))}
              />
              <span style={{ fontSize: 14 }}>Acesso total (igual ao admin)</span>
            </label>
          )}

          {formError && <p className="inline-error">{formError}</p>}

          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
            <Button variant="ghost" onClick={() => setModalOpen(false)} disabled={saving}>Cancelar</Button>
            <Button onClick={handleSave} disabled={saving}>{saving ? "Salvando..." : "Salvar"}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
