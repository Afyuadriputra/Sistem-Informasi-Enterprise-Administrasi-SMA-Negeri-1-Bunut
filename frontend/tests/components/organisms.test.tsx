import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { DataTable } from '@/components/organisms/DataTable';
import { ConfirmDialog } from '@/components/organisms/ConfirmDialog';
import { AppSidebar } from '@/components/organisms/AppSidebar';
import { AppHeader } from '@/components/organisms/AppHeader';

describe('Organisms - DataTable', () => {
  interface MockData {
    id: string;
    nama: string;
    nip: string;
  }

  const columns = [
    { header: 'Nama Pegawai', accessorKey: 'nama' as const },
    { header: 'NIP', accessorKey: 'nip' as const },
  ];

  const data: MockData[] = [
    { id: '1', nama: 'Budi Santoso', nip: '198001012005011001' },
    { id: '2', nama: 'Siti Aminah', nip: '198502022010012002' },
  ];

  it('renders table headers and rows correctly', () => {
    render(
      <DataTable<MockData>
        columns={columns}
        data={data}
        keyExtractor={(item) => item.id}
      />
    );
    expect(screen.getByText('Nama Pegawai')).toBeInTheDocument();
    expect(screen.getByText('NIP')).toBeInTheDocument();
    expect(screen.getByText('Budi Santoso')).toBeInTheDocument();
    expect(screen.getByText('Siti Aminah')).toBeInTheDocument();
  });

  it('renders loading skeleton when isLoading is true', () => {
    const { container } = render(
      <DataTable<MockData>
        columns={columns}
        data={[]}
        isLoading={true}
        keyExtractor={(item) => item.id}
      />
    );
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders empty state when data is empty and not loading', () => {
    render(
      <DataTable<MockData>
        columns={columns}
        data={[]}
        keyExtractor={(item) => item.id}
        emptyTitle="Tidak ada data pegawai"
      />
    );
    expect(screen.getByText('Tidak ada data pegawai')).toBeInTheDocument();
  });
});

describe('Organisms - ConfirmDialog', () => {
  it('renders title, description and handles confirm and cancel', () => {
    const handleConfirm = vi.fn();
    const handleClose = vi.fn();

    render(
      <ConfirmDialog
        isOpen={true}
        onOpenChange={handleClose}
        onConfirm={handleConfirm}
        title="Konfirmasi Pembatalan"
        description="Apakah Anda yakin ingin membatalkan kasus ini?"
        confirmLabel="Ya, Batalkan"
        cancelLabel="Kembali"
        variant="danger"
      />
    );

    expect(screen.getByText('Konfirmasi Pembatalan')).toBeInTheDocument();
    expect(screen.getByText('Apakah Anda yakin ingin membatalkan kasus ini?')).toBeInTheDocument();

    const cancelButton = screen.getByText('Kembali');
    fireEvent.click(cancelButton);
    expect(handleClose).toHaveBeenCalledWith(false);

    const confirmButton = screen.getByText('Ya, Batalkan');
    fireEvent.click(confirmButton);
    expect(handleConfirm).toHaveBeenCalledTimes(1);
  });
});

describe('Organisms - AppSidebar & AppHeader', () => {
  it('renders navigation links in AppSidebar', () => {
    render(
      <BrowserRouter>
        <AppSidebar isOpen={true} onClose={() => {}} />
      </BrowserRouter>
    );

    // Sidebar should display institution brand
    expect(screen.getByText('SMAN 1 BUNUT')).toBeInTheDocument();
    expect(screen.getByText('Sistem Informasi Enterprise')).toBeInTheDocument();
  });

  it('renders header elements with user profile trigger', () => {
    render(
      <BrowserRouter>
        <AppHeader onToggleSidebar={() => {}} />
      </BrowserRouter>
    );

    expect(screen.getByLabelText('Menu pengguna')).toBeInTheDocument();
    expect(screen.getByText('Pengguna')).toBeInTheDocument();
  });
});
