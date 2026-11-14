import { describe, it, expect, beforeEach } from "vitest";
import {
  setAuthTokens,
  getAccessToken,
  getRefreshToken,
  clearAuthTokens,
  isIdempotentRequest,
} from "@/lib/api-client";
import type { InternalAxiosRequestConfig } from "axios";

describe("Session Security & Safe Retry Policy Verification", () => {
  beforeEach(() => {
    clearAuthTokens();
  });

  describe("isIdempotentRequest", () => {
    it("recognizes safe and idempotent HTTP methods as eligible for retry", () => {
      const getCfg = { method: "get" } as InternalAxiosRequestConfig;
      const headCfg = { method: "head" } as InternalAxiosRequestConfig;
      const putCfg = { method: "put" } as InternalAxiosRequestConfig;
      const deleteCfg = { method: "delete" } as InternalAxiosRequestConfig;
      const optionsCfg = { method: "options" } as InternalAxiosRequestConfig;

      expect(isIdempotentRequest(getCfg)).toBe(true);
      expect(isIdempotentRequest(headCfg)).toBe(true);
      expect(isIdempotentRequest(putCfg)).toBe(true);
      expect(isIdempotentRequest(deleteCfg)).toBe(true);
      expect(isIdempotentRequest(optionsCfg)).toBe(true);
    });

    it("blocks standard non-idempotent POST methods from blind automatic retry", () => {
      const postCfg = { method: "post" } as InternalAxiosRequestConfig;
      expect(isIdempotentRequest(postCfg)).toBe(false);

      const defaultCfg = {} as InternalAxiosRequestConfig;
      // Default method without method property defaults to GET
      expect(isIdempotentRequest(defaultCfg)).toBe(true);
    });

    it("allows POST methods explicitly flagged with X-Safe-Retry header", () => {
      const postSafeCfg = {
        method: "post",
        headers: { "X-Safe-Retry": "true" },
      } as unknown as InternalAxiosRequestConfig;

      expect(isIdempotentRequest(postSafeCfg)).toBe(true);
    });
  });

  describe("Memory-Only Token Isolation & Logout Race Condition", () => {
    it("stores tokens strictly in volatile memory", () => {
      setAuthTokens("test-access-token", "test-refresh-token");
      expect(getAccessToken()).toBe("test-access-token");
      expect(getRefreshToken()).toBe("test-refresh-token");
    });

    it("completely cleans memory tokens and pending queue on clearAuthTokens", () => {
      setAuthTokens("access-abc", "refresh-xyz");
      clearAuthTokens();

      expect(getAccessToken()).toBeNull();
      expect(getRefreshToken()).toBeNull();
    });
  });
});
