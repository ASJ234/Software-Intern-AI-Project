from django.db import models
from django.utils import timezone


class Report(models.Model):
    """Model to store processed adverse event reports"""
    
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    
    OUTCOME_CHOICES = [
        ('recovered', 'Recovered'),
        ('ongoing', 'Ongoing'),
        ('fatal', 'Fatal'),
    ]
    
    original_report = models.TextField(help_text="Original medical report text")
    drug = models.CharField(max_length=255, help_text="Extracted drug name")
    adverse_events = models.JSONField(default=list, help_text="List of adverse events")
    severity = models.CharField(
        max_length=20, 
        choices=SEVERITY_CHOICES, 
        help_text="Severity level of the adverse events"
    )
    outcome = models.CharField(
        max_length=20, 
        choices=OUTCOME_CHOICES, 
        help_text="Patient outcome"
    )
    created_at = models.DateTimeField(default=timezone.now, help_text="When the report was processed")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Adverse Event Report"
        verbose_name_plural = "Adverse Event Reports"
    
    def __str__(self):
        return f"Report #{self.id} - {self.drug} ({self.severity})"
    
    @property
    def adverse_events_list(self):
        """Return adverse events as a formatted string"""
        return ', '.join(self.adverse_events) if self.adverse_events else 'None'
