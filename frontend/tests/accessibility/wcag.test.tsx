import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import axe from 'axe-core';
import { Button } from '@/components/atoms/Button';
import { StatusBadge } from '@/components/atoms/StatusBadge';
import { MetricCard } from '@/components/molecules/MetricCard';
import { EmptyState } from '@/components/molecules/EmptyState';
import { LoginPage } from '@/pages/auth/LoginPage';
import { Users } from 'lucide-react';

const testQueryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

// Configure axe rules for jsdom testing
async function checkA11y(container: HTMLElement) {
  const results = await axe.run(container, {
    rules: {
      // In jsdom environment, color-contrast checks can be noisy due to non-computed CSS canvas
      'color-contrast': { enabled: false },
    },
  });
  return results.violations;
}

describe('Accessibility & WCAG 2.1 AA Audit (axe-core)', () => {
  it('Button atom passes accessibility audit', async () => {
    const { container } = render(<Button aria-label="Simpan Data">Simpan Data</Button>);
    const violations = await checkA11y(container);
    expect(violations).toHaveLength(0);
  });

  it('StatusBadge atom passes accessibility audit with accessible role', async () => {
    const { container } = render(
      <StatusBadge status="DALAM_PENANGANAN" label="Dalam Penanganan" />
    );
    const violations = await checkA11y(container);
    expect(violations).toHaveLength(0);
  });

  it('MetricCard molecule passes accessibility audit', async () => {
    const { container } = render(
      <MetricCard
        title="Total Siswa Aktif"
        value={742}
        icon={<Users className="w-5 h-5" />}
        subtitle="Siswa terdaftar aktif tahun 2026/2027"
      />
    );
    const violations = await checkA11y(container);
    expect(violations).toHaveLength(0);
  });

  it('EmptyState molecule passes accessibility audit', async () => {
    const { container } = render(
      <EmptyState
        title="Tidak Ada Data"
        description="Belum ada catatan presensi untuk tanggal ini."
      />
    );
    const violations = await checkA11y(container);
    expect(violations).toHaveLength(0);
  });

  it('LoginPage passes accessibility audit with accessible form inputs and landmark semantics', async () => {
    const { container } = render(
      <QueryClientProvider client={testQueryClient}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    const violations = await checkA11y(container);
    expect(violations).toHaveLength(0);
  });
});
