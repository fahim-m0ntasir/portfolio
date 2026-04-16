from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

from .models import (
    Project, ContactMessage,
    SiteVisit, ButtonClick, SectionEngagement, AnalyticsDashboard,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'tags')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message_preview', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'sent_at')
    ordering = ('-sent_at',)
    date_hierarchy = 'sent_at'

    def message_preview(self, obj):
        return obj.message[:60] + '…' if len(obj.message) > 60 else obj.message
    message_preview.short_description = 'Message'

    def has_add_permission(self, request):
        return False


# ── Analytics Models ──────────────────────────────────────────────────────────

@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('page', 'ip_address', 'referrer', 'visited_at')
    list_filter = ('visited_at', 'page')
    search_fields = ('page', 'ip_address')
    readonly_fields = ('page', 'ip_address', 'referrer', 'user_agent', 'visited_at')
    ordering = ('-visited_at',)
    date_hierarchy = 'visited_at'

    def has_add_permission(self, request):
        return False


@admin.register(ButtonClick)
class ButtonClickAdmin(admin.ModelAdmin):
    list_display = ('button_label', 'button_id', 'page', 'clicked_at')
    list_filter = ('clicked_at', 'page')
    search_fields = ('button_label', 'button_id', 'page')
    readonly_fields = ('button_id', 'button_label', 'page', 'clicked_at')
    ordering = ('-clicked_at',)
    date_hierarchy = 'clicked_at'

    def has_add_permission(self, request):
        return False


@admin.register(SectionEngagement)
class SectionEngagementAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'duration_seconds', 'page', 'recorded_at')
    list_filter = ('recorded_at', 'section_id')
    search_fields = ('section_id', 'page')
    readonly_fields = ('section_id', 'duration_seconds', 'page', 'recorded_at')
    ordering = ('-recorded_at',)
    date_hierarchy = 'recorded_at'

    def has_add_permission(self, request):
        return False


@admin.register(AnalyticsDashboard)
class AnalyticsDashboardAdmin(admin.ModelAdmin):
    """Custom admin page that renders an aggregated analytics summary."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        now = timezone.now()
        last_7 = now - timedelta(days=7)
        last_30 = now - timedelta(days=30)

        context = {
            **self.admin_site.each_context(request),
            'title': 'Analytics Dashboard',
            'opts': self.model._meta,

            # Visit stats
            'total_visits': SiteVisit.objects.count(),
            'visits_7d': SiteVisit.objects.filter(visited_at__gte=last_7).count(),
            'visits_30d': SiteVisit.objects.filter(visited_at__gte=last_30).count(),
            'top_pages': SiteVisit.objects.values('page').annotate(
                count=Count('id')).order_by('-count')[:8],

            # Button click stats
            'total_clicks': ButtonClick.objects.count(),
            'top_buttons': ButtonClick.objects.values('button_label', 'button_id', 'page').annotate(
                count=Count('id')).order_by('-count')[:10],

            # Section engagement stats
            'section_stats': SectionEngagement.objects.values('section_id').annotate(
                avg_time=Avg('duration_seconds'),
                visits=Count('id'),
            ).order_by('-avg_time'),

            # Total messages
            'total_messages': ContactMessage.objects.count(),
            'messages_30d': ContactMessage.objects.filter(sent_at__gte=last_30).count(),
        }
        return TemplateResponse(request, 'admin/analytics_dashboard.html', context)
