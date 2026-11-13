import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { FormField } from '@/components/molecules/FormField';
import { SearchBar } from '@/components/molecules/SearchBar';
import { EmptyState } from '@/components/molecules/EmptyState';
import { ErrorState } from '@/components/molecules/ErrorState';
import { PaginationControl } from '@/components/molecules/PaginationControl';
import { MetricCard } from '@/components/molecules/MetricCard';

describe('Molecule Components', () => {
  it('renders FormField with label, helper text, and error alert', () => {
    const { rerender } = render(
      <FormField id="username" label="Nama Pengguna" helperText="Minimal 3 karakter">
        <input id="username" />
      </FormField>
    );

    expect(screen.getByText('Nama Pengguna')).toBeInTheDocument();
    expect(screen.getByText('Minimal 3 karakter')).toBeInTheDocument();

    rerender(
      <FormField id="username" label="Nama Pengguna" error="Username sudah terdaftar">
        <input id="username" />
      </FormField>
    );

    expect(screen.getByRole('alert')).toHaveTextContent('Username sudah terdaftar');
  });

  it('renders SearchBar and handles clear action', () => {
    const handleChange = vi.fn();
    render(<SearchBar value="Muhammad" onChange={handleChange} />);

    expect(screen.getByDisplayValue('Muhammad')).toBeInTheDocument();
    const clearBtn = screen.getByLabelText('Bersihkan pencarian');
    fireEvent.click(clearBtn);
    expect(handleChange).toHaveBeenCalledWith('');
  });

  it('renders EmptyState with title and action button', () => {
    const handleAction = vi.fn();
    render(
      <EmptyState
        title="Belum Ada Siswa"
        description="Silakan tambahkan siswa baru."
        actionLabel="Tambah Siswa"
        onAction={handleAction}
      />
    );

    expect(screen.getByText('Belum Ada Siswa')).toBeInTheDocument();
    expect(screen.getByText('Silakan tambahkan siswa baru.')).toBeInTheDocument();
    const btn = screen.getByRole('button', { name: /tambah siswa/i });
    fireEvent.click(btn);
    expect(handleAction).toHaveBeenCalledTimes(1);
  });

  it('renders ErrorState with retry callback and request id', () => {
    const handleRetry = vi.fn();
    render(
      <ErrorState
        title="Koneksi Terputus"
        message="Tidak dapat menghubungi server sekolah."
        requestId="req-12345"
        onRetry={handleRetry}
      />
    );

    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('req-12345')).toBeInTheDocument();
    const retryBtn = screen.getByRole('button', { name: /coba lagi/i });
    fireEvent.click(retryBtn);
    expect(handleRetry).toHaveBeenCalledTimes(1);
  });

  it('renders PaginationControl and handles page changes', () => {
    const handlePageChange = vi.fn();
    render(
      <PaginationControl
        currentPage={2}
        pageSize={10}
        totalItems={45}
        onPageChange={handlePageChange}
      />
    );

    expect(screen.getByText(/11/)).toBeInTheDocument();
    expect(screen.getByText(/20/)).toBeInTheDocument();
    expect(screen.getByText(/45/)).toBeInTheDocument();

    const prevBtn = screen.getByLabelText('Halaman sebelumnya');
    fireEvent.click(prevBtn);
    expect(handlePageChange).toHaveBeenCalledWith(1);

    const nextBtn = screen.getByLabelText('Halaman berikutnya');
    fireEvent.click(nextBtn);
    expect(handlePageChange).toHaveBeenCalledWith(3);
  });

  it('renders MetricCard with formatted value and subtitle', () => {
    render(
      <MetricCard
        title="Kehadiran Hari Ini"
        value="98.5%"
        subtitle="394 Hadir • 6 Alpa"
      />
    );

    expect(screen.getByText('Kehadiran Hari Ini')).toBeInTheDocument();
    expect(screen.getByText('98.5%')).toBeInTheDocument();
    expect(screen.getByText('394 Hadir • 6 Alpa')).toBeInTheDocument();
  });
});
