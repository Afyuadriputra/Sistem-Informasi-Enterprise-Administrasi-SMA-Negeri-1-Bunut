import { describe, it, expect, beforeEach } from 'vitest';
import { useAuthStore } from '@/stores/auth-store';

describe('auth-store state and RBAC checks', () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: null,
      activeRole: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  });

  it('correctly evaluates hasRole and hasAnyRole for single-role user', () => {
    useAuthStore.setState({
      user: {
        id: 1,
        username: 'guru_siti',
        name: 'Siti Aminah, S.Pd.',
        roles: ['Guru'],
      },
      isAuthenticated: true,
      activeRole: 'Guru',
    });

    const store = useAuthStore.getState();
    expect(store.hasRole('Guru')).toBe(true);
    expect(store.hasRole('Administrator')).toBe(false);
    expect(store.hasAnyRole(['Guru', 'Wali Kelas'])).toBe(true);
    expect(store.hasAnyRole(['Administrator', 'Pimpinan'])).toBe(false);
  });

  it('correctly handles multi-role users with additive union', () => {
    useAuthStore.setState({
      user: {
        id: 2,
        username: 'wali_budi',
        name: 'Budi Santoso, M.Pd.',
        roles: ['Guru', 'Wali Kelas'],
      },
      isAuthenticated: true,
      activeRole: 'Guru',
    });

    const store = useAuthStore.getState();
    expect(store.hasRole('Guru')).toBe(true);
    expect(store.hasRole('Wali Kelas')).toBe(true);
    expect(store.hasRole('Pimpinan')).toBe(false);

    // Switch active context
    store.setActiveRole('Wali Kelas');
    expect(useAuthStore.getState().activeRole).toBe('Wali Kelas');

    // Attempt invalid role switch
    store.setActiveRole('Administrator');
    expect(useAuthStore.getState().activeRole).toBe('Wali Kelas'); // Unchanged
  });

  it('resets state on logout', async () => {
    useAuthStore.setState({
      user: { id: 3, username: 'admin', name: 'Admin', roles: ['Administrator'] },
      isAuthenticated: true,
      activeRole: 'Administrator',
    });

    await useAuthStore.getState().logout();

    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.activeRole).toBeNull();
  });
});
