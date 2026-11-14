import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { UserPlus, Shield, Check, X as XIcon, Eye } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { SearchBar } from "@/components/molecules/SearchBar";
import { FormField } from "@/components/molecules/FormField";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { PaginationControl } from "@/components/molecules/PaginationControl";
import * as DialogPrimitive from "@radix-ui/react-dialog";

interface UserItem {
  id: number;
  username: string;
  name: string;
  is_active: boolean;
  roles: string[];
  created_at?: string;
}

interface UserListResponse {
  items: UserItem[];
  total: number;
  page: number;
  page_size: number;
}

const createUserSchema = z.object({
  username: z.string().min(3, "Nama pengguna minimal 3 karakter"),
  name: z.string().min(2, "Nama lengkap minimal 2 karakter"),
  password: z.string().min(8, "Kata sandi minimal 8 karakter"),
  roles: z.array(z.string()).min(1, "Pilih minimal satu peran"),
});

type CreateUserFormData = z.infer<typeof createUserSchema>;

export const AccountManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [search, setSearch] = React.useState("");
  const [roleFilter, setRoleFilter] = React.useState("");
  const [page, setPage] = React.useState(1);
  const pageSize = 10;
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);
  const [selectedUserId, setSelectedUserId] = React.useState<number | null>(
    null,
  );
  const [isDetailOpen, setIsDetailOpen] = React.useState(false);

  // Fetch users
  const { data, isLoading } = useQuery<UserListResponse>({
    queryKey: ["accounts-users", page, pageSize, search, roleFilter],
    queryFn: async () => {
      const params: Record<string, string | number> = {
        page,
        page_size: pageSize,
      };
      if (search) params.search = search;
      if (roleFilter) params.role = roleFilter;
      const res = await apiClient.get<UserListResponse>("/accounts/users", {
        params,
      });
      return res.data;
    },
  });

  // Fetch single user detail (operationId: getUserDetail)
  const { data: userDetail, isLoading: isUserDetailLoading } =
    useQuery<UserItem>({
      queryKey: ["accounts-user-detail", selectedUserId],
      queryFn: async () => {
        const res = await apiClient.get<UserItem>(
          `/accounts/users/${selectedUserId}`,
        );
        return res.data;
      },
      enabled: selectedUserId !== null && isDetailOpen,
    });

  // Fetch available roles
  const { data: rolesData } = useQuery<{
    items: Array<{ id: number; name: string }>;
  }>({
    queryKey: ["accounts-roles"],
    queryFn: async () => {
      const res = await apiClient.get<{
        items: Array<{ id: number; name: string }>;
      }>("/accounts/roles");
      return res.data;
    },
  });

  // Create User Mutation
  const createMutation = useMutation({
    mutationFn: async (payload: CreateUserFormData) => {
      const res = await apiClient.post("/accounts/users", payload);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["accounts-users"] });
      toast.success("Akun pengguna berhasil dibuat");
      setIsCreateOpen(false);
      reset();
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal membuat akun");
    },
  });

  // Toggle Active Mutation
  const toggleActiveMutation = useMutation({
    mutationFn: async ({
      id,
      is_active,
    }: {
      id: number;
      is_active: boolean;
    }) => {
      const res = await apiClient.patch(`/accounts/users/${id}`, { is_active });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["accounts-users"] });
      toast.success("Status keaktifan akun berhasil diperbarui");
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal mengubah status");
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<CreateUserFormData>({
    resolver: zodResolver(createUserSchema),
    defaultValues: {
      username: "",
      name: "",
      password: "",
      roles: ["Guru"],
    },
  });

  const selectedRoles = watch("roles") || [];

  const handleRoleToggle = (roleName: string) => {
    if (selectedRoles.includes(roleName)) {
      setValue(
        "roles",
        selectedRoles.filter((r) => r !== roleName),
      );
    } else {
      setValue("roles", [...selectedRoles, roleName]);
    }
  };

  const onSubmit = (formData: CreateUserFormData) => {
    createMutation.mutate(formData);
  };

  const columns: ColumnDef<UserItem>[] = [
    {
      header: "Nama Lengkap & Akun",
      cell: (user) => (
        <div>
          <div className="font-semibold text-text-foreground">{user.name}</div>
          <div className="text-xs text-text-muted">@{user.username}</div>
        </div>
      ),
    },
    {
      header: "Peran Terdaftar",
      cell: (user) => (
        <div className="flex flex-wrap gap-1">
          {user.roles.map((r) => (
            <span
              key={r}
              className="px-2 py-0.5 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-medium"
            >
              {r}
            </span>
          ))}
        </div>
      ),
    },
    {
      header: "Status",
      cell: (user) => (
        <StatusBadge status={user.is_active ? "AKTIF" : "NONAKTIF"} />
      ),
    },
    {
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (user) => (
        <div className="flex items-center justify-end gap-1.5">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setSelectedUserId(user.id);
              setIsDetailOpen(true);
            }}
            aria-label={`Lihat detail ${user.name}`}
          >
            <Eye className="h-4 w-4" aria-hidden="true" />
          </Button>
          <Button
            variant={user.is_active ? "danger" : "accent"}
            size="sm"
            onClick={() =>
              toggleActiveMutation.mutate({
                id: user.id,
                is_active: !user.is_active,
              })
            }
            isLoading={toggleActiveMutation.isPending}
          >
            {user.is_active ? "Nonaktifkan" : "Aktifkan"}
          </Button>
        </div>
      ),
    },
  ];

  const availableRoles = rolesData?.items || [
    { id: 1, name: "Administrator" },
    { id: 2, name: "Guru" },
    { id: 3, name: "Wali Kelas" },
    { id: 4, name: "Kesiswaan" },
    { id: 5, name: "Tata Usaha" },
    { id: 6, name: "Pimpinan" },
  ];

  return (
    <div className="space-y-6">
      {/* Top Filter and Action Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-surface p-4 rounded-card border border-border shadow-sm">
        <div className="flex flex-1 flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <SearchBar
            value={search}
            onChange={(val) => {
              setSearch(val);
              setPage(1);
            }}
            placeholder="Cari nama atau username..."
          />
          <select
            value={roleFilter}
            onChange={(e) => {
              setRoleFilter(e.target.value);
              setPage(1);
            }}
            className="h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
            aria-label="Filter berdasarkan peran"
          >
            <option value="">Semua Peran</option>
            {availableRoles.map((r) => (
              <option key={r.name} value={r.name}>
                {r.name}
              </option>
            ))}
          </select>
        </div>

        <Button
          variant="primary"
          onClick={() => {
            reset();
            setIsCreateOpen(true);
          }}
        >
          <UserPlus className="h-4 w-4 mr-2" aria-hidden="true" />
          Tambah Akun
        </Button>
      </div>

      {/* Users Table */}
      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<UserItem>
          columns={columns}
          data={data?.items || []}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          emptyTitle="Belum Ada Akun Pengguna"
          emptyDescription="Tidak ada akun pengguna yang sesuai dengan filter pencarian."
        />

        <PaginationControl
          currentPage={page}
          pageSize={pageSize}
          totalItems={data?.total || 0}
          onPageChange={setPage}
        />
      </div>

      {/* Create User Dialog */}
      <DialogPrimitive.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-lg translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <div className="flex items-center gap-2">
                <Shield
                  className="h-5 w-5 text-brand-primary"
                  aria-hidden="true"
                />
                <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                  Tambah Akun Pengguna Baru
                </DialogPrimitive.Title>
              </div>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <XIcon className="h-4 w-4" aria-hidden="true" />
                </button>
              </DialogPrimitive.Close>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 pt-4">
              <FormField
                id="name"
                label="Nama Lengkap"
                isRequired
                error={errors.name?.message}
              >
                <Input
                  id="name"
                  placeholder="Contoh: Budi Santoso, S.Pd."
                  {...register("name")}
                />
              </FormField>

              <FormField
                id="username"
                label="Nama Pengguna"
                isRequired
                error={errors.username?.message}
                helperText="Digunakan saat login ke sistem."
              >
                <Input
                  id="username"
                  placeholder="Contoh: budi.santoso"
                  {...register("username")}
                />
              </FormField>

              <FormField
                id="password"
                label="Kata Sandi Awal"
                isRequired
                error={errors.password?.message}
                helperText="Minimal 8 karakter."
              >
                <Input
                  id="password"
                  type="password"
                  placeholder="Masukkan kata sandi"
                  {...register("password")}
                />
              </FormField>

              <div>
                <label className="text-sm font-medium text-text-foreground block mb-1.5">
                  Tetapkan Peran Pengguna{" "}
                  <span className="text-semantic-danger-fg">*</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {availableRoles.map((r) => {
                    const isChecked = selectedRoles.includes(r.name);
                    return (
                      <button
                        type="button"
                        key={r.name}
                        onClick={() => handleRoleToggle(r.name)}
                        className={`flex items-center justify-between p-2.5 rounded-input border text-xs font-medium transition-colors ${
                          isChecked
                            ? "bg-brand-primary-subtle border-brand-primary text-brand-primary font-semibold"
                            : "bg-surface border-border-input text-text-muted hover:bg-surface-subtle"
                        }`}
                      >
                        <span>{r.name}</span>
                        {isChecked && (
                          <Check className="h-4 w-4" aria-hidden="true" />
                        )}
                      </button>
                    );
                  })}
                </div>
                {errors.roles?.message && (
                  <p className="text-xs text-semantic-danger-fg mt-1.5">
                    {errors.roles.message}
                  </p>
                )}
              </div>

              <div className="flex justify-end gap-2 pt-4 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsCreateOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createMutation.isPending}
                >
                  Simpan Akun
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* User Detail Dialog (getUserDetail) */}
      <DialogPrimitive.Root open={isDetailOpen} onOpenChange={setIsDetailOpen}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <div className="flex items-center gap-2">
                <Shield
                  className="h-5 w-5 text-brand-primary"
                  aria-hidden="true"
                />
                <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                  Detail Akun Pengguna
                </DialogPrimitive.Title>
              </div>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <XIcon className="h-4 w-4" aria-hidden="true" />
                </button>
              </DialogPrimitive.Close>
            </div>

            {isUserDetailLoading ? (
              <div className="py-8 text-center text-sm text-text-muted">
                Memuat informasi akun...
              </div>
            ) : userDetail ? (
              <div className="space-y-4 pt-4 text-sm">
                <div className="bg-surface-subtle p-3.5 rounded-input border border-border space-y-2">
                  <div className="flex justify-between">
                    <span className="text-text-muted text-xs">
                      ID Pengguna:
                    </span>
                    <span className="font-mono text-xs font-semibold">
                      #{userDetail.id}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted text-xs">Username:</span>
                    <span className="font-mono font-semibold">
                      @{userDetail.username}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted text-xs">
                      Nama Lengkap:
                    </span>
                    <span className="font-semibold">
                      {userDetail.name || "-"}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-text-muted text-xs">Status:</span>
                    <StatusBadge
                      status={userDetail.is_active ? "AKTIF" : "NONAKTIF"}
                    />
                  </div>
                  {userDetail.created_at && (
                    <div className="flex justify-between">
                      <span className="text-text-muted text-xs">
                        Terdaftar:
                      </span>
                      <span className="text-xs text-text-muted">
                        {userDetail.created_at}
                      </span>
                    </div>
                  )}
                </div>

                <div>
                  <h4 className="text-xs font-semibold uppercase text-text-muted mb-2">
                    Peran & Hak Akses:
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {userDetail.roles?.map((r) => (
                      <span
                        key={r}
                        className="px-2.5 py-1 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-semibold"
                      >
                        {r}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex justify-end pt-3 border-t border-border">
                  <Button
                    variant="secondary"
                    onClick={() => setIsDetailOpen(false)}
                  >
                    Tutup
                  </Button>
                </div>
              </div>
            ) : null}
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    </div>
  );
};
