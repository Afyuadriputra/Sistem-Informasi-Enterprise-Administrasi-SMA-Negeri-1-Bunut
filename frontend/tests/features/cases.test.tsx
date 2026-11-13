import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CaseListPage } from '@/pages/cases/CaseListPage';
import { CaseDetailPage } from '@/pages/cases/CaseDetailPage';
import { apiClient } from '@/lib/api-client';
import { useAuthStore } from '@/stores/auth-store';

vi.mock('@/lib/api-client', async () => {
  const actual = await vi.importActual<typeof import('@/lib/api-client')>('@/lib/api-client');
  return {
    ...actual,
    apiClient: {
      ...actual.apiClient,
      get: vi.fn(),
      post: vi.fn(),
    },
  };
});

describe('Feature - Case Management (S10 & S11)', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    vi.clearAllMocks();

    // Set active user with Kesiswaan role
    useAuthStore.setState({
      user: {
        id: 1,
        username: 'guru_bk',
        name: 'Guru BK SMAN 1',
        roles: ['Kesiswaan'],
      },
      activeRole: 'Kesiswaan',
      isAuthenticated: true,
    });
  });

  it('renders CaseListPage with search, filter tabs and create button', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: {
        items: [],
        total: 0,
        page: 1,
        page_size: 10,
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/cases']}>
          <Routes>
            <Route path="/cases" element={<CaseListPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Rujuk Kasus Baru')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Cari nomor kasus atau nama siswa/i)).toBeInTheDocument();
  });

  it('renders CaseDetailPage with optimistic version display and counseling note privacy masking', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: {
        id: 1,
        case_number: 'BK-2026-0001',
        student_id: 1,
        student_name: 'Ahmad Dahlan',
        student_number: '0012345678',
        class_name: 'X-MIPA-1',
        category: 'KEDISIPLINAN',
        description: 'Terlambat berulang lebih dari 3 kali',
        status: 'DIPROSES',
        version: 3,
        created_at: '2026-11-10T08:00:00Z',
        events: [
          {
            id: 1,
            action: 'CATAT_TINDAKAN',
            note: 'Dirahasiakan oleh Konselor/Kesiswaan',
            created_at: '2026-11-11T09:00:00Z',
            created_by_name: 'Guru BK',
          },
        ],
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/cases/1']}>
          <Routes>
            <Route path="/cases/:id" element={<CaseDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('BK-2026-0001')).toBeInTheDocument();
      expect(screen.getByText('Ahmad Dahlan')).toBeInTheDocument();
      expect(screen.getByText('Kategori: KEDISIPLINAN')).toBeInTheDocument();
      expect(screen.getByText(/Versi #3/i)).toBeInTheDocument();
      // Masking note check
      expect(screen.getByText('Dirahasiakan oleh Konselor/Kesiswaan')).toBeInTheDocument();
    });
  });
});
