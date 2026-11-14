import { describe, it, expect, beforeEach } from 'vitest';
import {
  setAuthTokens,
  getAccessToken,
  getRefreshToken,
  clearAuthTokens,
  apiClient,
  API_BASE_URL,
  resolveApiBaseUrl,
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

  it('resolves API base URLs accurately across different environment variations', () => {
    // Missing or empty falls back to relative /api
    expect(resolveApiBaseUrl(undefined)).toBe('/api');
    expect(resolveApiBaseUrl('')).toBe('/api');
    expect(resolveApiBaseUrl('   ')).toBe('/api');

    // Relative paths preserved without trailing slashes
    expect(resolveApiBaseUrl('/api')).toBe('/api');
    expect(resolveApiBaseUrl('/api/')).toBe('/api');
    expect(resolveApiBaseUrl('/api///')).toBe('/api');

    // Absolute URLs without /api get /api appended
    expect(resolveApiBaseUrl('http://127.0.0.1:8000')).toBe('http://127.0.0.1:8000/api');
    expect(resolveApiBaseUrl('http://localhost:8000/')).toBe('http://localhost:8000/api');

    // Absolute URLs already specifying /api are normalized
    expect(resolveApiBaseUrl('http://127.0.0.1:8000/api')).toBe('http://127.0.0.1:8000/api');
    expect(resolveApiBaseUrl('http://127.0.0.1:8000/api/')).toBe('http://127.0.0.1:8000/api');
  });

  it('prevents duplicate /api prefix when caller provides /api/... route', async () => {
    const handler = (apiClient.interceptors.request as any).handlers[0].fulfilled;
    const config = await handler({
      url: '/api/auth/login',
      headers: {},
    } as any);

    // /api/auth/login should have duplicate /api stripped to avoid /api/api/auth/login
    expect(config.url).toBe('/auth/login');
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

  it('ensures no sensitive backend database secrets are exposed in import.meta.env', () => {
    const envKeys = Object.keys(import.meta.env);
    const forbiddenPatterns = ['DATABASE_URL', 'REDIS_URL', 'SECRET_KEY', 'PASSWORD', 'BACKEND_PROXY_TARGET'];
    
    for (const key of envKeys) {
      for (const pattern of forbiddenPatterns) {
        expect(key.toUpperCase().includes(pattern)).toBe(false);
      }
    }
  });
});
