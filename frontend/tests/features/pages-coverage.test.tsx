import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DashboardPage } from '@/pages/dashboard/DashboardPage';
import { AccountManagementPage } from '@/pages/accounts/AccountManagementPage';
import { StudentListPage } from '@/pages/students/StudentListPage';
import { AcademicMasterPage } from '@/pages/academic/AcademicMasterPage';
import { AssignmentsPage } from '@/pages/assignments/AssignmentsPage';
import { ReportsPage } from '@/pages/reports/ReportsPage';
import { AuditLogsPage } from '@/pages/audit/AuditLogsPage';
import { ProfilePage } from '@/pages/profile/ProfilePage';
import { ForbiddenPage, NotFoundPage, ServerErrorPage } from '@/pages/error/ErrorPages';
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
      patch: vi.fn(),
    },
  };
});

describe('Feature - Full Pages Coverage', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    vi.clearAllMocks();

    useAuthStore.setState({
      user: {
        id: 1,
        username: 'admin',
        name: 'Administrator Sekolah',
        roles: ['Administrator'],
      },
      activeRole: 'Administrator',
      isAuthenticated: true,
    });
  });

  it('renders DashboardPage with metrics and quick links', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: {
        total_students: 750,
        today_attendance_percentage: 96.5,
        active_cases_count: 3,
        pending_requests_count: 5,
        role_specific_metrics: { total_active_users: 42 },
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <DashboardPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText(/Selamat Datang/i)).toBeInTheDocument();
    expect(screen.getByText('Tingkat Kehadiran Hari Ini')).toBeInTheDocument();
  });

  it('renders AccountManagementPage with user management table', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <AccountManagementPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Tambah Akun')).toBeInTheDocument();
  });

  it('renders StudentListPage with student database search', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <StudentListPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Tambah Siswa')).toBeInTheDocument();
  });

  it('renders AcademicMasterPage with academic year tabs', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <AcademicMasterPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Siklus Tahun Ajaran')).toBeInTheDocument();
  });

  it('renders AssignmentsPage with enrollment tabs', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 10 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <AssignmentsPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Penempatan Rombel Siswa')).toBeInTheDocument();
  });

  it('renders ReportsPage with report export cards', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [] },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <ReportsPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Laporan Rekapitulasi Presensi (.xlsx)')).toBeInTheDocument();
  });

  it('renders AuditLogsPage with system audit table', async () => {
    (apiClient.get as any).mockResolvedValueOnce({
      data: { items: [], total: 0, page: 1, page_size: 15 },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <AuditLogsPage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Log Rekaman Jejak Audit Sistem')).toBeInTheDocument();
  });

  it('renders ProfilePage with authenticated user metadata', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <ProfilePage />
        </MemoryRouter>
      </QueryClientProvider>
    );

    expect(screen.getByText('Administrator Sekolah')).toBeInTheDocument();
    expect(screen.getByText('@admin')).toBeInTheDocument();
    expect(screen.getByText('Hak Akses & Konteks Peran')).toBeInTheDocument();
  });

  it('renders ErrorPages (403, 404, 500) correctly', () => {
    const { rerender } = render(
      <MemoryRouter>
        <ForbiddenPage />
      </MemoryRouter>
    );
    expect(screen.getByText('Akses Terbatas (403)')).toBeInTheDocument();

    rerender(
      <MemoryRouter>
        <NotFoundPage />
      </MemoryRouter>
    );
    expect(screen.getByText('Halaman Tidak Ditemukan (404)')).toBeInTheDocument();

    rerender(
      <MemoryRouter>
        <ServerErrorPage />
      </MemoryRouter>
    );
    expect(screen.getByText('Kendala Sistem (500)')).toBeInTheDocument();
  });
});
