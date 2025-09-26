from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Report
from .serializers import (
    ReportSerializer, ProcessReportSerializer, ReportResponseSerializer,
    TranslationRequestSerializer, TranslationResponseSerializer
)
from .nlp_processor import nlp_processor


@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Regulatory Report Assistant API',
        'version': '1.0.0',
        'endpoints': {
            'process_report': '/api/process-report/',
            'reports': '/api/reports/',
            'translate': '/api/translate/',
            'admin': '/admin/'
        }
    })


@api_view(['POST'])
def process_report(request):
    """Process adverse event report and extract structured data"""
    serializer = ProcessReportSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Process the report using NLP
        processed_data = nlp_processor.process_report(serializer.validated_data['report'])
        
        # Save to database
        report = Report.objects.create(
            original_report=serializer.validated_data['report'],
            drug=processed_data['drug'],
            adverse_events=processed_data['adverse_events'],
            severity=processed_data['severity'],
            outcome=processed_data['outcome']
        )
        
        # Return the processed data
        response_serializer = ReportResponseSerializer(processed_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing report: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_reports(request):
    """Get all processed reports"""
    try:
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response({'reports': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error fetching reports: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_report_detail(request, report_id):
    """Get a specific report by ID"""
    try:
        report = get_object_or_404(Report, id=report_id)
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error fetching report: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def translate_text(request):
    """Translate text to French or Swahili"""
    serializer = TranslationRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        translated_text = nlp_processor.translate_text(
            serializer.validated_data['text'],
            serializer.validated_data['target_language']
        )
        
        response_data = {
            'translated_text': translated_text,
            'original_text': serializer.validated_data['text'],
            'target_language': serializer.validated_data['target_language']
        }
        
        response_serializer = TranslationResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error translating text: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_analytics(request):
    """Get analytics data for reports"""
    try:
        reports = Report.objects.all()
        
        # Severity distribution
        severity_counts = {}
        for report in reports:
            severity = report.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Outcome distribution
        outcome_counts = {}
        for report in reports:
            outcome = report.outcome
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        
        # Most common adverse events
        adverse_event_counts = {}
        for report in reports:
            for event in report.adverse_events:
                adverse_event_counts[event] = adverse_event_counts.get(event, 0) + 1
        
        # Most common drugs
        drug_counts = {}
        for report in reports:
            drug = report.drug
            drug_counts[drug] = drug_counts.get(drug, 0) + 1
        
        analytics_data = {
            'total_reports': reports.count(),
            'severity_distribution': severity_counts,
            'outcome_distribution': outcome_counts,
            'common_adverse_events': dict(sorted(adverse_event_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            'common_drugs': dict(sorted(drug_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        
        return Response(analytics_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error generating analytics: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
