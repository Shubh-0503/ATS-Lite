from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Job title, e.g. 'Senior Python Developer'"
    )
    description = models.TextField(
        blank=True,
        help_text="Full job description (optional)"
    )
    required_skills = models.TextField(
        help_text="Comma-separated skills, e.g. 'Python, Django, REST API'"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive jobs don't appear in listings but data is preserved"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Keep job even if recruiter account deleted
        null=True,
        blank=True,
        related_name='posted_jobs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest jobs first
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_skills_list(self):
        
        if not self.required_skills or not self.required_skills.strip():
            return []
        skills = [s.strip().lower() for s in self.required_skills.split(',')]
        # Remove empty strings and deduplicate while preserving order
        seen = set()
        result = []
        for skill in skills:
            if skill and skill not in seen:
                seen.add(skill)
                result.append(skill)
        return result
