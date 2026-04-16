from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/phyto-feeder/', views.project_phyto_feeder, name='project_phyto_feeder'),
    path('projects/env-bot/', views.project_env_bot, name='project_env_bot'),
    path('projects/self-balancing/', views.project_self_balancing, name='project_self_balancing'),
    path('projects/line-follower/', views.project_line_follower, name='project_line_follower'),

    # Analytics tracking endpoints
    path('analytics/click/', views.track_click, name='track_click'),
    path('analytics/section/', views.track_section, name='track_section'),
]
