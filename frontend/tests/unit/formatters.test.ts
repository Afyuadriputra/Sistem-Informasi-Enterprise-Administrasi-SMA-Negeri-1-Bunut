import { describe, it, expect } from 'vitest';
import { formatDate, formatDateTime, formatTime, formatNumber, formatPercent } from '@/lib/formatters';

describe('formatters utility', () => {
  it('formats Indonesian dates correctly', () => {
    expect(formatDate('2026-07-15')).toContain('15');
    expect(formatDate('2026-07-15')).toContain('Juli');
    expect(formatDate('2026-07-15')).toContain('2026');
    expect(formatDate(null)).toBe('-');
    expect(formatDate('')).toBe('-');
  });

  it('formats Indonesian date-time correctly', () => {
    const formatted = formatDateTime('2026-11-13T14:30:00Z');
    expect(formatted).toContain('2026');
    expect(formatted).toContain('WIB');
  });

  it('formats Indonesian time correctly', () => {
    const formatted = formatTime('2026-11-13T10:15:00Z');
    expect(formatted).toContain('WIB');
  });

  it('formats Indonesian numbers correctly', () => {
    expect(formatNumber(1250)).toBe('1.250');
    expect(formatNumber(0)).toBe('0');
    expect(formatNumber(null)).toBe('0');
  });

  it('formats percentage correctly', () => {
    expect(formatPercent(98.5)).toBe('98,5%');
    expect(formatPercent(100)).toBe('100,0%');
    expect(formatPercent(null)).toBe('0%');
  });
});
