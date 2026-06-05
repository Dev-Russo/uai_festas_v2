"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";

export function TicketModal({ eventId, saleId, open, onClose, onSaved }: { eventId: string; saleId: string | null; open: boolean; onClose: () => void; onSaved?: () => void; }) {
  const [loading, setLoading] = useState(false);
  const [sale, setSale] = useState<any>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!open || !saleId) return;
    setLoading(true);
    api.getSale(String(eventId), String(saleId)).then((s) => setSale(s)).catch(() => setSale(null)).finally(() => setLoading(false));
  }, [open, saleId, eventId]);

  if (!open) return null;

  async function handleSave() {
    if (!sale) return;
    setSaving(true);
    try {
      await api.updateSale(String(eventId), String(sale.id), {
        buyer_name: sale.buyerName,
        buyer_email: sale.buyerEmail,
        buyer_cpf: sale.buyerCpf,
      });
      onSaved && onSaved();
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
      onClose();
    }
  }

  async function handleResend() {
    if (!sale) return;
    try {
      await api.sendTicketEmail(String(eventId), String(sale.id), { to_email: sale.buyerEmail });
      // optionally show feedback
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <Modal open={open} title="Ingresso" onClose={onClose}>
      <div style={{ width: 520 }}>
        <div style={{ padding: "1rem", display: "grid", gap: "0.6rem" }}>
          {loading ? <p className="muted">Carregando...</p> : null}
          {sale ? (
            <>
              <div><strong>Produto:</strong> {sale.productId}</div>
              <Input label="Nome" value={sale.buyerName ?? ""} onChange={(e) => setSale((s: any) => ({ ...s, buyerName: e.target.value }))} />
              <Input label="Email" value={sale.buyerEmail ?? ""} onChange={(e) => setSale((s: any) => ({ ...s, buyerEmail: e.target.value }))} />
              <Input label="CPF" value={sale.buyerCpf ?? ""} onChange={(e) => setSale((s: any) => ({ ...s, buyerCpf: e.target.value }))} />
              <div style={{ display: "flex", gap: 8 }}>
                <Button type="button" onClick={() => api.downloadTicket(String(eventId), String(sale.id))}>Baixar/Imprimir</Button>
                <Button type="button" onClick={handleResend}>Reenviar e-mail</Button>
                <div style={{ flex: 1 }} />
                <Button type="button" variant="primary" onClick={handleSave} disabled={saving}>{saving ? "Salvando..." : "Salvar"}</Button>
              </div>
            </>
          ) : null}
        </div>
      </div>
    </Modal>
  );
}

export default TicketModal;
