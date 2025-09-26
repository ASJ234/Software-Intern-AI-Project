from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin interface for Report model"""
    
    list_display = [
        'id', 'drug', 'severity', 'outcome', 
        'adverse_events_list', 'created_at'
    ]
    list_filter = ['severity', 'outcome', 'created_at']
    search_fields = ['drug', 'original_report']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('original_report', 'created_at')
        }),
        ('Extracted Data', {
            'fields': ('drug', 'adverse_events', 'severity', 'outcome')
        }),
    )
    
    def adverse_events_list(self, obj):
        """Display adverse events as a comma-separated string"""
        return obj.adverse_events_list
    adverse_events_list.short_description = 'Adverse Events'
