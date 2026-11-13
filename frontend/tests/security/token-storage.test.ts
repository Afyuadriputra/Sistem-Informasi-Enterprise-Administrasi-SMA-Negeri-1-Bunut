import { describe, it, expect, beforeEach } from 'vitest';
import {
  setAuthTokens,
  getAccessToken,
  getRefreshToken,
  clearAuthTokens,
} from '@/lib/api-client';
import { useAuthStore } from '@/stores/auth-store';

describe('Security Hardening - Memory-Only Token Architecture', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    clearAuthTokens();
    useAuthStore.getState().logout();
  });

  it('guarantees access token and refresh token are NOT stored in localStorage', () => {
    setAuthTokens('jwt-access-sensitive-token', 'jwt-refresh-sensitive-token');

    expect(getAccessToken()).toBe('jwt-access-sensitive-token');
    expect(getRefreshToken()).toBe('jwt-refresh-sensitive-token');

    // Audit localStorage
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('token')).toBeNull();
    expect(localStorage.getItem('refresh_token')).toBeNull();
    expect(localStorage.getItem('jwt')).toBeNull();
    expect(localStorage.getItem('auth')).toBeNull();

    // Audit sessionStorage
    expect(sessionStorage.getItem('access_token')).toBeNull();
    expect(sessionStorage.getItem('refresh_token')).toBeNull();

    // Audit document.cookie
    expect(document.cookie).not.toContain('jwt-access-sensitive-token');
    expect(document.cookie).not.toContain('jwt-refresh-sensitive-token');
  });

  it('purges memory tokens completely on logout', async () => {
    setAuthTokens('jwt-access-to-purge', 'jwt-refresh-to-purge');
    expect(getAccessToken()).toBe('jwt-access-to-purge');

    await useAuthStore.getState().logout();

    expect(getAccessToken()).toBeNull();
    expect(getRefreshToken()).toBeNull();
    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().isAuthenticated).toBe(false);
  });

  it('verifies auth-store does not persist tokens in Zustand persistence', () => {
    // Only non-sensitive user metadata and active role are kept in localStorage
    const storedState = localStorage.getItem('sie-auth-store');
    if (storedState) {
      const parsed = JSON.parse(storedState);
      expect(parsed.state?.token).toBeUndefined();
      expect(parsed.state?.accessToken).toBeUndefined();
      expect(parsed.state?.refreshToken).toBeUndefined();
    }
  });
});
