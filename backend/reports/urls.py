from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('process-report/', views.process_report, name='process_report'),
    path('reports/', views.get_reports, name='get_reports'),
    path('reports/<int:report_id>/', views.get_report_detail, name='get_report_detail'),
    path('translate/', views.translate_text, name='translate_text'),
    path('analytics/', views.get_analytics, name='get_analytics'),
]
