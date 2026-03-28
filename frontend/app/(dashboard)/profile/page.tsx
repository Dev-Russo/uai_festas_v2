"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { User } from "@/types";

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    api.getMe().then(setUser).catch(() => setUser(null));
  }, []);

  return (
    <main className="card" style={{ padding: "1rem" }}>
      <h1 style={{ marginTop: 0 }}>Perfil</h1>
      {user ? (
        <div style={{ display: "grid", gap: "0.35rem" }}>
          <p><strong>Nome:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Papel:</strong> {user.role}</p>
        </div>
      ) : (
        <p className="muted">Nao foi possivel carregar os dados.</p>
      )}
    </main>
  );
}
