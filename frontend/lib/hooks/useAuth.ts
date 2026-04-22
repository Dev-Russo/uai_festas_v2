"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { clearToken, decodeToken, getToken, saveToken } from "@/lib/auth";
import { Commissioner, User, UserType } from "@/types";

export type AuthUser = User | Commissioner;

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [userType, setUserType] = useState<UserType>("user");
  const [loading, setLoading] = useState(() => Boolean(getToken()));

  useEffect(() => {
    const token = getToken();
    if (!token) {
      return;
    }

    const payload = decodeToken(token);
    const type: UserType = payload?.user_type ?? "user";
    setUserType(type);

    const fetchMe = type === "commissioner" ? api.getCommissionerMe() : api.getMe();

    fetchMe
      .then((me) => setUser(me as AuthUser))
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  async function login(identifier: string, password: string): Promise<{ userType: UserType; eventId: number | null }> {
    const payload = await api.login(identifier, password);
    saveToken(payload.token);
    setUserType(payload.userType);

    const me = payload.userType === "commissioner" ? await api.getCommissionerMe() : await api.getMe();
    setUser(me as AuthUser);

    return { userType: payload.userType, eventId: payload.eventId };
  }

  function logout() {
    clearToken();
    setUser(null);
    setUserType("user");
  }

  return { user, userType, loading, login, logout, isAuthenticated: Boolean(user) };
}
