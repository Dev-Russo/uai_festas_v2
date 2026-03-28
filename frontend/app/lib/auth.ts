export const tokenKey = "uai_festas_token";

export function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(tokenKey);
}

export function saveToken(token: string): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(tokenKey, token);
}

export function clearToken(): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(tokenKey);
}
