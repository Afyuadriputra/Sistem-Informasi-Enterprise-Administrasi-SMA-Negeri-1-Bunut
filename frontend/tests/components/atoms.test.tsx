import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/atoms/Button';
import { Input } from '@/components/atoms/Input';
import { Label } from '@/components/atoms/Label';
import { StatusBadge } from '@/components/atoms/StatusBadge';
import { Spinner } from '@/components/atoms/Spinner';
import { Skeleton } from '@/components/atoms/Skeleton';

describe('Atom Components', () => {
  describe('Button', () => {
    it('renders text and handles clicks', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Simpan Data</Button>);

      const btn = screen.getByRole('button', { name: /simpan data/i });
      expect(btn).toBeInTheDocument();
      fireEvent.click(btn);
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('shows loading spinner and disables button when isLoading is true', () => {
      const handleClick = vi.fn();
      render(<Button isLoading onClick={handleClick}>Proses</Button>);

      const btn = screen.getByRole('button');
      expect(btn).toBeDisabled();
      fireEvent.click(btn);
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('applies variant classes correctly', () => {
      const { rerender } = render(<Button variant="danger">Hapus</Button>);
      expect(screen.getByRole('button')).toHaveClass('bg-semantic-danger-fg');

      rerender(<Button variant="accent">Konfirmasi</Button>);
      expect(screen.getByRole('button')).toHaveClass('bg-brand-accent');
    });
  });

  describe('Input', () => {
    it('renders input with accessible states', () => {
      render(<Input placeholder="Masukkan nama..." hasError />);
      const input = screen.getByPlaceholderText('Masukkan nama...');
      expect(input).toHaveAttribute('aria-invalid', 'true');
      expect(input).toHaveClass('border-semantic-danger-fg');
    });
  });

  describe('Label', () => {
    it('renders label with required indicator', () => {
      render(<Label htmlFor="test-id" isRequired>Nama Pengguna</Label>);
      expect(screen.getByText('Nama Pengguna')).toBeInTheDocument();
      expect(screen.getByText('*')).toBeInTheDocument();
    });
  });

  describe('StatusBadge', () => {
    it('maps semantic statuses to proper labels and color classes', () => {
      const { rerender } = render(<StatusBadge status="HADIR" />);
      expect(screen.getByText('Hadir')).toHaveClass('text-semantic-success-fg');

      rerender(<StatusBadge status="ALPA" />);
      expect(screen.getByText('Alpa')).toHaveClass('text-semantic-danger-fg');

      rerender(<StatusBadge status="MENUNGGU_PERSETUJUAN" />);
      expect(screen.getByText('Menunggu Persetujuan')).toHaveClass('text-semantic-warning-fg');
    });
  });

  describe('Spinner and Skeleton', () => {
    it('renders accessible status role for Spinner', () => {
      render(<Spinner label="Memuat konten..." />);
      expect(screen.getByRole('status')).toBeInTheDocument();
      expect(screen.getByText('Memuat konten...')).toHaveClass('sr-only');
    });

    it('renders skeleton element with pulse animation', () => {
      const { container } = render(<Skeleton className="h-6 w-32" />);
      expect(container.firstChild).toHaveClass('animate-pulse');
      expect(container.firstChild).toHaveAttribute('aria-hidden', 'true');
    });
  });
});
