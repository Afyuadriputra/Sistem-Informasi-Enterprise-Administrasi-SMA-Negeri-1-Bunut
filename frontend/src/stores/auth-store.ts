import { create } from "zustand";
import {
  apiClient,
  setAuthTokens,
  clearAuthTokens,
  getRefreshToken,
  registerAuthFailureCallback,
} from "@/lib/api-client";

export interface AssignedClass {
  id: number;
  name: string;
  level: number;
  academic_year_name?: string;
  role?: string;
}

export interface UserProfile {
  id: number;
  username: string;
  name: string;
  employee_id?: number | null;
  roles: string[];
  assigned_classes?: AssignedClass[];
}

interface AuthState {
  user: UserProfile | null;
  activeRole: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  fetchCurrentUser: () => Promise<UserProfile | null>;
  setActiveRole: (role: string) => void;
  hasRole: (role: string) => boolean;
  hasAnyRole: (roles: string[]) => boolean;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => {
  // Register auto-logout when refresh fails in api-client
  registerAuthFailureCallback(() => {
    set({
      user: null,
      activeRole: null,
      isAuthenticated: false,
      isLoading: false,
    });
  });

  return {
    user: null,
    activeRole: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,

    login: async (username: string, password: string) => {
      set({ isLoading: true, error: null });
      try {
        const res = await apiClient.post<{
          access_token: string;
          refresh_token: string;
          token_type?: string;
          expires_in?: number;
        }>("/auth/login", { username, password });

        setAuthTokens(res.data.access_token, res.data.refresh_token);

        // Immediately fetch user profile
        const userProfile = await get().fetchCurrentUser();
        if (userProfile) {
          const defaultRole = userProfile.roles[0] || null;
          set({
            user: userProfile,
            activeRole: defaultRole,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          return true;
        }

        set({ isLoading: false, isAuthenticated: false });
        return false;
      } catch (err: unknown) {
        const errorObj = err as { normalized?: { message: string } };
        const msg =
          errorObj?.normalized?.message ||
          "Nama pengguna atau kata sandi tidak sesuai";
        clearAuthTokens();
        set({
          user: null,
          activeRole: null,
          isAuthenticated: false,
          isLoading: false,
          error: msg,
        });
        return false;
      }
    },

    logout: async () => {
      const refreshToken = getRefreshToken();
      try {
        if (refreshToken) {
          await apiClient.post("/auth/logout", { refresh_token: refreshToken });
        }
      } catch {
        // Ignore logout errors
      } finally {
        clearAuthTokens();
        set({
          user: null,
          activeRole: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
      }
    },

    fetchCurrentUser: async () => {
      try {
        const res = await apiClient.get<UserProfile>("/auth/me");
        const user = res.data;
        set({ user, isAuthenticated: true });
        return user;
      } catch {
        return null;
      }
    },

    setActiveRole: (role: string) => {
      const { user } = get();
      if (user && user.roles.includes(role)) {
        set({ activeRole: role });
      }
    },

    hasRole: (role: string) => {
      const { user } = get();
      if (!user) return false;
      return user.roles.includes(role);
    },

    hasAnyRole: (roles: string[]) => {
      const { user } = get();
      if (!user) return false;
      return roles.some((r) => user.roles.includes(r));
    },

    clearError: () => set({ error: null }),
  };
});
