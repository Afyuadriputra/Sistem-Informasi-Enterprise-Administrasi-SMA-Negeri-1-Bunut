import * as React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate, useLocation } from "react-router-dom";
import { Lock, User, AlertCircle } from "lucide-react";
import { useAuthStore } from "@/stores/auth-store";
import { AuthLayout } from "@/components/templates/AuthLayout";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { FormField } from "@/components/molecules/FormField";

const loginSchema = z.object({
  username: z.string().min(1, "Nama pengguna wajib diisi"),
  password: z.string().min(1, "Kata sandi wajib diisi"),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isLoading, error, clearError } = useAuthStore();

  const from =
    (location.state as { from?: { pathname: string } })?.from?.pathname ||
    "/dashboard";

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    clearError();
    const success = await login(data.username, data.password);
    if (success) {
      navigate(from, { replace: true });
    }
  };

  return (
    <AuthLayout>
      <div className="bg-surface border border-border rounded-card p-8 shadow-sm">
        <div className="mb-6">
          <h2 className="text-2xl font-bold tracking-tight text-text-foreground">
            Masuk ke Akun
          </h2>
          <p className="text-sm text-text-muted mt-1">
            Gunakan kredensial resmi sekolah yang telah diberikan oleh
            Administrator.
          </p>
        </div>

        {error && (
          <div
            role="alert"
            className="flex items-start gap-3 p-3.5 mb-5 rounded-input bg-semantic-danger-bg border border-semantic-danger-border text-semantic-danger-fg text-sm"
          >
            <AlertCircle
              className="h-5 w-5 shrink-0 mt-0.5"
              aria-hidden="true"
            />
            <div>
              <p className="font-semibold">Gagal Masuk</p>
              <p className="text-xs text-text-foreground mt-0.5">{error}</p>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            id="username"
            label="Nama Pengguna"
            isRequired
            error={errors.username?.message}
          >
            <div className="relative">
              <User
                className="absolute left-3 top-2.5 h-4 w-4 text-text-muted pointer-events-none"
                aria-hidden="true"
              />
              <Input
                id="username"
                type="text"
                autoComplete="username"
                placeholder="Masukkan nama pengguna"
                hasError={!!errors.username}
                className="pl-9"
                {...register("username")}
              />
            </div>
          </FormField>

          <FormField
            id="password"
            label="Kata Sandi"
            isRequired
            error={errors.password?.message}
          >
            <div className="relative">
              <Lock
                className="absolute left-3 top-2.5 h-4 w-4 text-text-muted pointer-events-none"
                aria-hidden="true"
              />
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                placeholder="Masukkan kata sandi"
                hasError={!!errors.password}
                className="pl-9"
                {...register("password")}
              />
            </div>
          </FormField>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full mt-2"
            isLoading={isLoading}
          >
            Masuk Sistem
          </Button>
        </form>

        <div className="mt-6 pt-4 border-t border-border text-center text-xs text-text-muted">
          Lupa kata sandi? Hubungi staf Tata Usaha atau Administrator sekolah
          untuk reset akun.
        </div>
      </div>
    </AuthLayout>
  );
};
