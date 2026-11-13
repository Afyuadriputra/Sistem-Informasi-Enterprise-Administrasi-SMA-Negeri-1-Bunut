import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RequestListPage } from '@/pages/administration/RequestListPage';
import { ApprovalsQueuePage } from '@/pages/administration/ApprovalsQueuePage';
import { DocumentArchivePage } from '@/pages/administration/DocumentArchivePage';
import { RequestDetailPage } from '@/pages/administration/RequestDetailPage';
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

describe('Feature - Administration Services (S12, S14, S15)', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    vi.clearAllMocks();

    useAuthStore.setState({
      user: {
        id: 1,
        username: 'staff_tu',
        name: 'Staf Tata Usaha',
        roles: ['Tata Usaha'],
      },
      activeRole: 'Tata Usaha',
      isAuthenticated: true,
    });
  });

  it('renders RequestListPage with request table and create button', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/administration/requests']}>
          <Routes>
            <Route path="/administration/requests" element={<RequestListPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Buat Permohonan Baru')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Cari nomor surat, siswa, atau pemohon/i)).toBeInTheDocument();
  });

  it('renders ApprovalsQueuePage with pimpinan approval banner and table', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/administration/approvals']}>
          <Routes>
            <Route path="/administration/approvals" element={<ApprovalsQueuePage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Antrean Persetujuan Disposisi Pimpinan')).toBeInTheDocument();
    expect(screen.getByText(/Permohonan Menunggu/i)).toBeInTheDocument();
  });

  it('renders DocumentArchivePage with archive search and table', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/administration/documents']}>
          <Routes>
            <Route path="/administration/documents" element={<DocumentArchivePage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Katalog Arsip Dokumen Digital')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Cari nama dokumen atau no\. surat/i)).toBeInTheDocument();
  });

  it('renders RequestDetailPage with workflow action buttons and document attachments', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: {
        id: 1,
        request_number: 'REQ-2026-0001',
        service_type_name: 'Surat Keterangan Aktif Sekolah',
        student_id: 1,
        student_name: 'Budi Darmawan',
        student_number: '0034567890',
        applicant_name: 'Budi Darmawan (Siswa)',
        status: 'DIAJUKAN',
        purpose: 'Keperluan beasiswa Pemkab Pelalawan',
        version: 1,
        created_at: '2026-11-12T08:00:00Z',
        documents: [],
        events: [],
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/administration/requests/1']}>
          <Routes>
            <Route path="/administration/requests/:id" element={<RequestDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('REQ-2026-0001')).toBeInTheDocument();
      expect(screen.getByText('Surat Keterangan Aktif Sekolah')).toBeInTheDocument();
      expect(screen.getByText('Keperluan beasiswa Pemkab Pelalawan')).toBeInTheDocument();
      expect(screen.getByText('Mulai Verifikasi Berkas')).toBeInTheDocument();
    });
  });
});
