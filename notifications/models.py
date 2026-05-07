from django.db import models
from candidates.models import Candidate
from jobs.models import Job


class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest first
        indexes = [
            models.Index(fields=['is_read', '-created_at']),
        ]

    def __str__(self):
        status = '✓' if self.is_read else '●'
        return f"[{status}] {self.message[:60]}"
