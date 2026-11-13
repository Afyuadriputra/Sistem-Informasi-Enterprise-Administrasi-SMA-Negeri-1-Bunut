import { describe, it, expect, beforeEach } from 'vitest';
import {
  setAuthTokens,
  getAccessToken,
  getRefreshToken,
  clearAuthTokens,
  apiClient,
  API_BASE_URL,
} from '@/lib/api-client';

describe('api-client and memory token management', () => {
  beforeEach(() => {
    clearAuthTokens();
  });

  it('manages tokens exclusively in memory', () => {
    expect(getAccessToken()).toBeNull();
    expect(getRefreshToken()).toBeNull();

    setAuthTokens('test-access-token-123', 'test-refresh-token-456');

    expect(getAccessToken()).toBe('test-access-token-123');
    expect(getRefreshToken()).toBe('test-refresh-token-456');

    // Verify localStorage and sessionStorage contain NO tokens
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(sessionStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('refresh_token')).toBeNull();

    clearAuthTokens();
    expect(getAccessToken()).toBeNull();
    expect(getRefreshToken()).toBeNull();
  });

  it('normalizes API base URL without trailing slash or duplicate /api', () => {
    expect(API_BASE_URL.endsWith('/')).toBe(false);
    expect(API_BASE_URL).toContain('/api');
    expect(API_BASE_URL.includes('/api/api')).toBe(false);
  });

  it('attaches X-Request-ID and bearer token to request headers', async () => {
    setAuthTokens('valid-jwt-token');
    const config = await (apiClient.interceptors.request as any).handlers[0].fulfilled({
      headers: {},
    } as any);

    expect(config.headers['Authorization']).toBe('Bearer valid-jwt-token');
    expect(config.headers['X-Request-ID']).toBeDefined();
    expect(typeof config.headers['X-Request-ID']).toBe('string');
    expect(config.headers['X-Request-ID'].length).toBeGreaterThan(5);
  });
});
