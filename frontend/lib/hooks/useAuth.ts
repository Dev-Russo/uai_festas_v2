"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { clearToken, decodeToken, getToken, saveToken } from "@/lib/auth";
import { Commissioner, TokenPayload, User, UserType } from "@/types";

export type AuthUser = User | Commissioner;

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [userType, setUserType] = useState<UserType>("user");
  const [tokenPayload, setTokenPayload] = useState<TokenPayload | null>(null);
  const [loading, setLoading] = useState(() => Boolean(getToken()));

  useEffect(() => {
    const token = getToken();
    if (!token) {
      return;
    }

    const payload = decodeToken(token);
    const type: UserType = payload?.user_type ?? "user";
    setUserType(type);
    setTokenPayload(payload);

    const fetchMe = type === "commissioner" ? api.getCommissionerMe() : api.getMe();

    fetchMe
      .then((me) => setUser(me as AuthUser))
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  async function login(identifier: string, password: string): Promise<{ userType: UserType; eventId: number | null }> {
    const result = await api.login(identifier, password);
    saveToken(result.token);
    setUserType(result.userType);
    setTokenPayload(decodeToken(result.token));

    const me = result.userType === "commissioner" ? await api.getCommissionerMe() : await api.getMe();
    setUser(me as AuthUser);

    return { userType: result.userType, eventId: result.eventId };
  }

  function logout() {
    clearToken();
    setUser(null);
    setUserType("user");
    setTokenPayload(null);
  }

  return { user, userType, tokenPayload, loading, login, logout, isAuthenticated: Boolean(user) };
}
