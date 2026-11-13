import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RecordAttendancePage } from '@/pages/attendance/RecordAttendancePage';
import { AttendanceRecapPage } from '@/pages/attendance/AttendanceRecapPage';
import { apiClient } from '@/lib/api-client';

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

describe('Feature - Attendance Recording (S08)', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    vi.clearAllMocks();
  });

  it('renders attendance recording header and action controls', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: {
        items: [
          { id: 'c1', name: 'X-MIPA-1' },
          { id: 'c2', name: 'X-MIPA-2' },
        ],
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RecordAttendancePage />
        </BrowserRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Pilih Rombongan Belajar:')).toBeInTheDocument();
    expect(screen.getByText('Tanggal Presensi:')).toBeInTheDocument();
    expect(screen.getByText('Tandai Semua Hadir')).toBeInTheDocument();
    expect(screen.getByText('Simpan Kehadiran')).toBeInTheDocument();
  });
});

describe('Feature - Attendance Recap (S09)', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    vi.clearAllMocks();
  });

  it('renders attendance recap filters and table', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: {
        items: [{ id: 'c1', name: 'X-MIPA-1' }],
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AttendanceRecapPage />
        </BrowserRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Rombongan Belajar:')).toBeInTheDocument();
    expect(screen.getByText('Mulai Tanggal:')).toBeInTheDocument();
    expect(screen.getByText('Ekspor Excel Resmi')).toBeInTheDocument();
  });
});
