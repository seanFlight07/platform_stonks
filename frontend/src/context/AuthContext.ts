import { createContext } from "react";

export type User = {
  id: number;
  email: string;
  role: string;
};

export type AuthContextType = {
  user: User | null;
  token: string | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);
