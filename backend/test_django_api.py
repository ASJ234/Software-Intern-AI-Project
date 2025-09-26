#!/usr/bin/env python3
"""
Test script for the Django Regulatory Report Assistant API
"""
import requests
import json
import time
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

API_BASE_URL = "http://localhost:8000/api"

def test_api():
    """Test all API endpoints"""
    print("🧪 Testing Django Regulatory Report Assistant API")
    print("=" * 60)
    
    # Test cases
    test_reports = [
        {
            "name": "Basic Report",
            "report": "Patient experienced severe nausea and headache after taking Drug X. Patient recovered."
        },
        {
            "name": "Multiple Adverse Events",
            "report": "Patient reported mild dizziness, fatigue, and skin rash after taking Aspirin 500mg. Symptoms are ongoing."
        },
        {
            "name": "Fatal Outcome",
            "report": "Patient experienced severe allergic reaction to Penicillin injection. Patient died."
        },
        {
            "name": "Complex Report",
            "report": "65-year-old patient developed moderate chest pain and shortness of breath after taking Warfarin 5mg daily. Patient was hospitalized and recovered after treatment."
        }
    ]
    
    # Test API root endpoint
    print("🔍 Testing API root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API root endpoint error: {e}")
    
    print("\n" + "=" * 60)
    
    # Test process-report endpoint
    for i, test_case in enumerate(test_reports, 1):
        print(f"🔍 Testing {test_case['name']}...")
        try:
            response = requests.post(
                f"{API_BASE_URL}/process-report/",
                json={"report": test_case["report"]},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Report processed successfully")
                print(f"   Drug: {result['drug']}")
                print(f"   Adverse Events: {result['adverse_events']}")
                print(f"   Severity: {result['severity']}")
                print(f"   Outcome: {result['outcome']}")
            else:
                print(f"❌ Report processing failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Report processing error: {e}")
        
        print()
    
    # Test reports endpoint
    print("🔍 Testing reports endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/reports/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reports endpoint working - {len(data['reports'])} reports found")
        else:
            print(f"❌ Reports endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Reports endpoint error: {e}")
    
    # Test analytics endpoint
    print("\n🔍 Testing analytics endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics endpoint working")
            print(f"   Total reports: {data['total_reports']}")
            print(f"   Severity distribution: {data['severity_distribution']}")
        else:
            print(f"❌ Analytics endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analytics endpoint error: {e}")
    
    # Test translation endpoint
    print("\n🔍 Testing translation endpoint...")
    test_translations = [
        {"text": "recovered", "target_language": "french"},
        {"text": "severe", "target_language": "swahili"},
        {"text": "ongoing", "target_language": "french"}
    ]
    
    for translation in test_translations:
        try:
            response = requests.post(
                f"{API_BASE_URL}/translate/",
                json=translation,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Translation successful: '{translation['text']}' -> '{result['translated_text']}' ({translation['target_language']})")
            else:
                print(f"❌ Translation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Translation error: {e}")
    
    print("\n🎉 Django API testing completed!")

if __name__ == "__main__":
    print("Make sure the Django server is running on http://localhost:8000")
    print("You can start it with: python manage.py runserver")
    print()
    
    # Wait a moment for user to start server if needed
    time.sleep(2)
    
    test_api()
