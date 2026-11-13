from django.conf import settings
from django.db import models


class CaseStatusEnum(models.TextChoices):
    BARU = "BARU", "Baru"
    DIPROSES = "DIPROSES", "Diproses"
    SELESAI = "SELESAI", "Selesai"
    DIBATALKAN = "DIBATALKAN", "Dibatalkan"


class CaseActionEnum(models.TextChoices):
    MULAI_PENANGANAN = "MULAI_PENANGANAN", "Mulai Penanganan"
    CATAT_TINDAKAN = "CATAT_TINDAKAN", "Catat Tindakan"
    SELESAIKAN = "SELESAIKAN", "Selesaikan"
    BATALKAN = "BATALKAN", "Batalkan"


class StudentCase(models.Model):
    student = models.ForeignKey(
        "master_data.Student",
        on_delete=models.CASCADE,
        related_name="cases",
        db_column="student_id",
    )
    title = models.CharField(max_length=200)
    summary = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=CaseStatusEnum.choices,
        default=CaseStatusEnum.BARU,
    )
    assigned_to = models.ForeignKey(
        "master_data.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_cases",
        db_column="assigned_to_id",
    )
    version = models.IntegerField(default=1)  # Optimistic concurrency control
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_cases"
        indexes = [
            models.Index(fields=["student"], name="idx_cases_student"),
            models.Index(fields=["status", "created_at"], name="idx_cases_st_cr"),
            models.Index(fields=["assigned_to"], name="idx_cases_assigned"),
        ]

    def __str__(self):
        return f"[{self.status}] {self.title} - {self.student.name} (v{self.version})"


class CaseEvent(models.Model):
    case = models.ForeignKey(
        StudentCase,
        on_delete=models.CASCADE,
        related_name="events",
        db_column="case_id",
    )
    action = models.CharField(max_length=100)
    initial_status = models.CharField(max_length=20, choices=CaseStatusEnum.choices)
    final_status = models.CharField(max_length=20, choices=CaseStatusEnum.choices)
    note = models.TextField()
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="actor_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "case_events"
        indexes = [
            models.Index(fields=["case", "created_at"], name="idx_cev_case_cr"),
        ]

    def __str__(self):
        return f"{self.case.id}: {self.action} ({self.initial_status} -> {self.final_status})"
