import * as React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { AppLayout } from "@/components/templates/AppLayout";
import { ProtectedRoute } from "@/components/ProtectedRoute";

// Pages
import { LoginPage } from "@/pages/auth/LoginPage";
import { ProfilePage } from "@/pages/profile/ProfilePage";
import { DashboardPage } from "@/pages/dashboard/DashboardPage";
import { AccountManagementPage } from "@/pages/accounts/AccountManagementPage";
import { StudentListPage } from "@/pages/students/StudentListPage";
import { AcademicMasterPage } from "@/pages/academic/AcademicMasterPage";
import { AssignmentsPage } from "@/pages/assignments/AssignmentsPage";
import { RecordAttendancePage } from "@/pages/attendance/RecordAttendancePage";
import { AttendanceRecapPage } from "@/pages/attendance/AttendanceRecapPage";
import { CaseListPage } from "@/pages/cases/CaseListPage";
import { CaseDetailPage } from "@/pages/cases/CaseDetailPage";
import { RequestListPage } from "@/pages/administration/RequestListPage";
import { NewRequestPage } from "@/pages/administration/NewRequestPage";
import { RequestDetailPage } from "@/pages/administration/RequestDetailPage";
import { ApprovalsQueuePage } from "@/pages/administration/ApprovalsQueuePage";
import { DocumentArchivePage } from "@/pages/administration/DocumentArchivePage";
import { ReportsPage } from "@/pages/reports/ReportsPage";
import { AuditLogsPage } from "@/pages/audit/AuditLogsPage";
import { NotFoundPage } from "@/pages/error/ErrorPages";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 1000 * 60 * 2, // 2 minutes
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected Application Shell */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="profile" element={<ProfilePage />} />

            {/* Master & Accounts (Admin) */}
            <Route
              path="accounts"
              element={
                <ProtectedRoute allowedRoles={["Administrator"]}>
                  <AccountManagementPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="students"
              element={
                <ProtectedRoute
                  allowedRoles={[
                    "Administrator",
                    "Kesiswaan",
                    "Guru",
                    "Wali Kelas",
                    "Tata Usaha",
                    "Pimpinan",
                  ]}
                >
                  <StudentListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="academic"
              element={
                <ProtectedRoute allowedRoles={["Administrator"]}>
                  <AcademicMasterPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="assignments"
              element={
                <ProtectedRoute allowedRoles={["Administrator"]}>
                  <AssignmentsPage />
                </ProtectedRoute>
              }
            />

            {/* Attendance (Guru, Wali Kelas) */}
            <Route
              path="attendance/record"
              element={
                <ProtectedRoute allowedRoles={["Guru", "Wali Kelas"]}>
                  <RecordAttendancePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="attendance/recap"
              element={
                <ProtectedRoute allowedRoles={["Guru", "Wali Kelas"]}>
                  <AttendanceRecapPage />
                </ProtectedRoute>
              }
            />

            {/* Student Affairs (Kesiswaan, Wali Kelas, Guru) */}
            <Route
              path="cases"
              element={
                <ProtectedRoute
                  allowedRoles={["Kesiswaan", "Wali Kelas", "Guru"]}
                >
                  <CaseListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="cases/:id"
              element={
                <ProtectedRoute
                  allowedRoles={["Kesiswaan", "Wali Kelas", "Guru"]}
                >
                  <CaseDetailPage />
                </ProtectedRoute>
              }
            />

            {/* Administration & Documents (Tata Usaha, Pimpinan) */}
            <Route
              path="requests"
              element={
                <ProtectedRoute allowedRoles={["Tata Usaha"]}>
                  <RequestListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="requests/new"
              element={
                <ProtectedRoute allowedRoles={["Tata Usaha"]}>
                  <NewRequestPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="requests/:id"
              element={
                <ProtectedRoute allowedRoles={["Tata Usaha", "Pimpinan"]}>
                  <RequestDetailPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="approvals"
              element={
                <ProtectedRoute allowedRoles={["Pimpinan"]}>
                  <ApprovalsQueuePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="documents"
              element={
                <ProtectedRoute allowedRoles={["Tata Usaha", "Pimpinan"]}>
                  <DocumentArchivePage />
                </ProtectedRoute>
              }
            />

            {/* Reports & Audit */}
            <Route
              path="reports"
              element={
                <ProtectedRoute
                  allowedRoles={["Pimpinan", "Tata Usaha", "Guru"]}
                >
                  <ReportsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="audit-logs"
              element={
                <ProtectedRoute allowedRoles={["Administrator"]}>
                  <AuditLogsPage />
                </ProtectedRoute>
              }
            />

            {/* 404 Route */}
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
