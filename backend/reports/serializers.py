from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model"""
    
    class Meta:
        model = Report
        fields = [
            'id', 'original_report', 'drug', 'adverse_events', 
            'severity', 'outcome', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProcessReportSerializer(serializers.Serializer):
    """Serializer for processing report requests"""
    report = serializers.CharField(
        max_length=10000,
        help_text="Medical report text to process"
    )


class ReportResponseSerializer(serializers.Serializer):
    """Serializer for processed report responses"""
    drug = serializers.CharField(max_length=255)
    adverse_events = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    severity = serializers.ChoiceField(choices=Report.SEVERITY_CHOICES)
    outcome = serializers.ChoiceField(choices=Report.OUTCOME_CHOICES)


class TranslationRequestSerializer(serializers.Serializer):
    """Serializer for translation requests"""
    text = serializers.CharField(max_length=500)
    target_language = serializers.ChoiceField(
        choices=[('french', 'French'), ('swahili', 'Swahili')]
    )


class TranslationResponseSerializer(serializers.Serializer):
    """Serializer for translation responses"""
    translated_text = serializers.CharField(max_length=500)
    original_text = serializers.CharField(max_length=500)
    target_language = serializers.CharField(max_length=20)
