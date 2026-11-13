from django.conf import settings
from django.db import models


class ServiceRequestStatusEnum(models.TextChoices):
    DIAJUKAN = "DIAJUKAN", "Diajukan"
    DIPROSES = "DIPROSES", "Diproses"
    MENUNGGU_PERSETUJUAN = "MENUNGGU_PERSETUJUAN", "Menunggu Persetujuan"
    DISETUJUI = "DISETUJUI", "Disetujui"
    DITOLAK = "DITOLAK", "Ditolak"
    SELESAI = "SELESAI", "Selesai"


class ServiceActionEnum(models.TextChoices):
    PROSES = "PROSES", "Proses"
    AJUKAN_PERSETUJUAN = "AJUKAN_PERSETUJUAN", "Ajukan Persetujuan"
    SETUJUI = "SETUJUI", "Setujui"
    TOLAK = "TOLAK", "Tolak"
    SELESAIKAN = "SELESAIKAN", "Selesaikan"


class ServiceType(models.Model):
    code = models.CharField(max_length=30, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    requires_approval = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "service_types"

    def __str__(self):
        return f"{self.code} - {self.name}"


class ServiceRequest(models.Model):
    request_number = models.CharField(max_length=50, unique=True, db_index=True)
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.CASCADE,
        related_name="requests",
        db_column="service_type_id",
    )
    applicant_name = models.CharField(max_length=150)
    applicant_phone = models.CharField(max_length=20, null=True, blank=True)
    student = models.ForeignKey(
        "master_data.Student",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_requests",
        db_column="student_id",
    )
    purpose = models.TextField()
    status = models.CharField(
        max_length=30,
        choices=ServiceRequestStatusEnum.choices,
        default=ServiceRequestStatusEnum.DIAJUKAN,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_service_requests",
        db_column="created_by_id",
    )
    version = models.IntegerField(default=1)  # Optimistic concurrency control
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "service_requests"
        indexes = [
            models.Index(fields=["request_number"], name="idx_requests_number"),
            models.Index(fields=["status", "created_at"], name="idx_req_st_cr"),
            models.Index(fields=["service_type"], name="idx_requests_type"),
        ]

    def __str__(self):
        return f"{self.request_number} ({self.status})"


class ServiceEvent(models.Model):
    request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="events",
        db_column="request_id",
    )
    action = models.CharField(max_length=100)
    initial_status = models.CharField(max_length=30, choices=ServiceRequestStatusEnum.choices)
    final_status = models.CharField(max_length=30, choices=ServiceRequestStatusEnum.choices)
    note = models.TextField(null=True, blank=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="actor_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "service_events"
        indexes = [
            models.Index(fields=["request", "created_at"], name="idx_sev_req_cr"),
        ]

    def __str__(self):
        return f"{self.request.request_number}: {self.action} ({self.initial_status} -> {self.final_status})"


class Document(models.Model):
    request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="documents",
        db_column="request_id",
    )
    storage_key = models.CharField(max_length=100, unique=True, db_index=True)
    original_filename = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    file_size = models.IntegerField()
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="uploaded_by_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"
        indexes = [
            models.Index(fields=["request"], name="idx_docs_request"),
            models.Index(fields=["storage_key"], name="idx_docs_key"),
        ]

    def __str__(self):
        return f"{self.original_filename} ({self.file_size} bytes)"
