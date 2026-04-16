from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.CharField(max_length=200, help_text="Comma separated tags e.g. 'React, Vue, Node'")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


# ── Analytics Models ──────────────────────────────────────────────────────────

class SiteVisit(models.Model):
    page = models.CharField(max_length=300)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.URLField(blank=True, null=True, max_length=500)
    user_agent = models.CharField(max_length=500, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visited_at']
        verbose_name = 'Site Visit'
        verbose_name_plural = 'Site Visits'

    def __str__(self):
        return f"{self.page} — {self.visited_at.strftime('%Y-%m-%d %H:%M')}"


class ButtonClick(models.Model):
    button_id = models.CharField(max_length=100)
    button_label = models.CharField(max_length=200, blank=True)
    page = models.CharField(max_length=300)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-clicked_at']
        verbose_name = 'Button Click'
        verbose_name_plural = 'Button Clicks'

    def __str__(self):
        return f"'{self.button_label}' on {self.page}"


class SectionEngagement(models.Model):
    section_id = models.CharField(max_length=100)
    duration_seconds = models.FloatField()
    page = models.CharField(max_length=300)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Section Engagement'
        verbose_name_plural = 'Section Engagements'

    def __str__(self):
        return f"#{self.section_id}: {self.duration_seconds:.1f}s"


# Proxy model — no DB table, used purely as an admin dashboard entry point
class AnalyticsDashboard(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Analytics Dashboard'
        verbose_name_plural = 'Analytics Dashboard'
