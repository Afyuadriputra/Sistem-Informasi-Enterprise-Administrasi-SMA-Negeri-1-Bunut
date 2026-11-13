from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class AttendanceStatusEnum(models.TextChoices):
    HADIR = "HADIR", "Hadir"
    SAKIT = "SAKIT", "Sakit"
    IZIN = "IZIN", "Izin"
    ALPA = "ALPA", "Alpa"


class Attendance(models.Model):
    student = models.ForeignKey(
        "master_data.Student",
        on_delete=models.CASCADE,
        related_name="attendances",
        db_column="student_id",
    )
    school_class = models.ForeignKey(
        "master_data.SchoolClass",
        on_delete=models.CASCADE,
        related_name="attendances",
        db_column="class_id",
    )
    date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatusEnum.choices,
        default=AttendanceStatusEnum.HADIR,
    )
    note = models.CharField(max_length=255, default="", blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="recorded_by_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords(table_name="historical_attendances")

    class Meta:
        db_table = "attendances"
        unique_together = (("student", "school_class", "date"),)
        indexes = [
            models.Index(fields=["school_class", "date"], name="idx_att_cls_dt"),
            models.Index(fields=["student", "date"], name="idx_att_std_dt"),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.school_class.name} ({self.date}): {self.status}"
