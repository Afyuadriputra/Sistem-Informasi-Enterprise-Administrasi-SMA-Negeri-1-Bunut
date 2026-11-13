import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LoginPage } from '@/pages/auth/LoginPage';
import { useAuthStore } from '@/stores/auth-store';
import { apiClient } from '@/lib/api-client';

vi.mock('@/lib/api-client', async () => {
  const actual = await vi.importActual<typeof import('@/lib/api-client')>('@/lib/api-client');
  return {
    ...actual,
    apiClient: {
      ...actual.apiClient,
      post: vi.fn(),
      get: vi.fn(),
    },
  };
});

describe('Feature - Auth & LoginPage (S01)', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    useAuthStore.getState().logout();
    vi.clearAllMocks();
  });

  const renderLoginPage = () =>
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </QueryClientProvider>
    );

  it('renders login form elements with accessible labels and brand title', () => {
    renderLoginPage();

    expect(screen.getByText('Masuk ke Akun')).toBeInTheDocument();
    expect(screen.getByLabelText(/Nama Pengguna/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Kata Sandi/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Masuk Sistem/i })).toBeInTheDocument();
  });

  it('validates required fields on empty submit', async () => {
    renderLoginPage();

    const submitBtn = screen.getByRole('button', { name: /Masuk Sistem/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText('Nama pengguna wajib diisi')).toBeInTheDocument();
      expect(screen.getByText('Kata sandi wajib diisi')).toBeInTheDocument();
    });
  });

  it('handles login failure and displays error alert banner', async () => {
    (apiClient.post as any).mockRejectedValueOnce({
      normalized: {
        message: 'Kredensial tidak valid',
      },
    });

    renderLoginPage();

    fireEvent.change(screen.getByLabelText(/Nama Pengguna/i), {
      target: { value: 'admin' },
    });
    fireEvent.change(screen.getByLabelText(/Kata Sandi/i), {
      target: { value: 'wrong-password' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Masuk Sistem/i }));

    await waitFor(() => {
      expect(screen.getByText(/Kredensial tidak valid/i)).toBeInTheDocument();
    });
  });
});
