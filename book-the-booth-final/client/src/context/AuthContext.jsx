import { createContext, useState, useEffect } from "react";
import { api } from "../api/client";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  useEffect(() => {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }, [token]);

  useEffect(() => {
    if (user) localStorage.setItem("user", JSON.stringify(user));
    else localStorage.removeItem("user");
  }, [user]);

  async function login(username, password) {
    const data = await api.post("/login", { username, password });
    setToken(data.token);
    setUser(data.user);
    return data.user;
  }

  async function register(formData) {
    await api.post("/register", formData);
    return login(formData.username, formData.password);
  }

  function logout() {
    setToken(null);
    setUser(null);
  }

  const value = { token, user, login, register, logout, isAuthenticated: Boolean(token) };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}