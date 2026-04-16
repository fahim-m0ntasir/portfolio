import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Project, ContactMessage, ButtonClick, SectionEngagement


def handle_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)
            return False

        ContactMessage.objects.create(name=name, email=email, message=message)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent successfully. I will get back to you soon.'})

        messages.success(request, 'Thank you! Your message has been sent successfully. I will get back to you soon.')
        return True
    return False


def index(request):
    resp = handle_contact(request)
    if isinstance(resp, JsonResponse):
        return resp
    if resp is True:
        return redirect('home')
    return render(request, 'index.html')


def project_phyto_feeder(request):
    return render(request, 'project_phyto_feeder.html')


def project_env_bot(request):
    return render(request, 'project_env_bot.html')


def project_self_balancing(request):
    return render(request, 'project_self_balancing.html')


def project_line_follower(request):
    return render(request, 'project_line_follower.html')


# ── Analytics Tracking Endpoints ──────────────────────────────────────────────

@csrf_exempt
def track_click(request):
    """Receives button-click events from the frontend."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ButtonClick.objects.create(
                button_id=data.get('button_id', ''),
                button_label=data.get('button_label', '')[:200],
                page=data.get('page', '/')[:300],
            )
            return JsonResponse({'status': 'ok'})
        except Exception:
            pass
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def track_section(request):
    """Receives section-engagement time events from the frontend."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            duration = float(data.get('duration', 0))
            if duration > 0:
                SectionEngagement.objects.create(
                    section_id=data.get('section_id', '')[:100],
                    duration_seconds=round(duration, 2),
                    page=data.get('page', '/')[:300],
                )
            return JsonResponse({'status': 'ok'})
        except Exception:
            pass
    return JsonResponse({'status': 'error'}, status=400)
