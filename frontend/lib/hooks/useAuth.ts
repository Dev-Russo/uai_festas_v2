"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { clearToken, getToken, saveToken } from "@/lib/auth";
import { User } from "@/types";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(() => Boolean(getToken()));

  useEffect(() => {
    const token = getToken();
    if (!token) {
      return;
    }

    api
      .getMe()
      .then((me) => setUser(me))
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  async function login(email: string, password: string) {
    const payload = await api.login(email, password);
    saveToken(payload.token);
    const me = await api.getMe();
    setUser(me);
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  return { user, loading, login, logout, isAuthenticated: Boolean(user) };
}
