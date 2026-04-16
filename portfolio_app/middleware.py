from .models import SiteVisit

IGNORE_PATHS = ('/admin/', '/static/', '/analytics/', '/favicon')


class AnalyticsMiddleware:
    """Automatically records every HTML page GET request as a SiteVisit."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET' and not any(request.path.startswith(p) for p in IGNORE_PATHS):
            x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded.split(',')[0].strip() if x_forwarded else request.META.get('REMOTE_ADDR')
            SiteVisit.objects.create(
                page=request.path,
                ip_address=ip,
                referrer=request.META.get('HTTP_REFERER') or None,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            )

        return response
