"""
NLP processing module for extracting structured data from medical reports
"""
import re
import spacy
from typing import List, Dict, Any


class NLPProcessor:
    """Class to handle NLP processing of medical reports"""
    
    def __init__(self):
        """Initialize the NLP processor"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy English model not found. Using fallback regex patterns.")
            self.nlp = None
        
        # Drug extraction patterns
        self.drug_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:tablet|capsule|injection|dose|mg|ml|g)\b',
            r'\bDrug\s+[A-Z]\b',
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:X|Y|Z)\b',
            r'\b(?:aspirin|ibuprofen|acetaminophen|morphine|penicillin|insulin|warfarin|metformin)\b'
        ]
        
        # Adverse event keywords
        self.adverse_events = {
            'nausea': ['nausea', 'nauseous', 'nauseated', 'queasy'],
            'headache': ['headache', 'head pain', 'migraine', 'cephalgia'],
            'dizziness': ['dizziness', 'dizzy', 'vertigo', 'lightheaded'],
            'rash': ['rash', 'skin irritation', 'dermatitis', 'hives', 'skin reaction'],
            'fatigue': ['fatigue', 'tiredness', 'exhaustion', 'weakness'],
            'diarrhea': ['diarrhea', 'diarrhoea', 'loose stools'],
            'vomiting': ['vomiting', 'vomit', 'throwing up', 'emesis'],
            'fever': ['fever', 'pyrexia', 'elevated temperature'],
            'pain': ['pain', 'ache', 'soreness', 'discomfort', 'chest pain'],
            'swelling': ['swelling', 'edema', 'inflammation'],
            'shortness of breath': ['shortness of breath', 'breathing difficulty', 'dyspnea'],
            'allergic reaction': ['allergic reaction', 'allergy', 'hypersensitivity']
        }
        
        # Severity indicators
        self.severity_indicators = {
            'severe': ['severe', 'serious', 'critical', 'life-threatening', 'intense', 'extreme'],
            'moderate': ['moderate', 'modest', 'noticeable', 'significant'],
            'mild': ['mild', 'slight', 'minor', 'light', 'gentle']
        }
        
        # Outcome indicators
        self.outcome_indicators = {
            'recovered': ['recovered', 'recovery', 'resolved', 'better', 'improved', 'healed'],
            'ongoing': ['ongoing', 'continuing', 'persistent', 'still', 'remains'],
            'fatal': ['fatal', 'death', 'died', 'deceased', 'expired', 'passed away']
        }
    
    def extract_drug(self, text: str) -> str:
        """Extract drug name from text using NLP and pattern matching"""
        text_lower = text.lower()
        
        # Try spaCy NER if available
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["DRUG", "CHEMICAL"]:
                    return ent.text
        
        # Fallback to regex patterns
        for pattern in self.drug_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        # Simple fallback - look for "Drug X" pattern
        drug_match = re.search(r'\bDrug\s+[A-Z]\b', text, re.IGNORECASE)
        if drug_match:
            return drug_match.group()
        
        return "Unknown Drug"
    
    def extract_adverse_events(self, text: str) -> List[str]:
        """Extract adverse events from text"""
        text_lower = text.lower()
        found_events = []
        
        for event, keywords in self.adverse_events.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_events.append(event)
                    break
        
        return list(set(found_events))  # Remove duplicates
    
    def extract_severity(self, text: str) -> str:
        """Extract severity level from text"""
        text_lower = text.lower()
        
        for severity, indicators in self.severity_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return severity
        
        return "mild"  # Default to mild if not specified
    
    def extract_outcome(self, text: str) -> str:
        """Extract outcome from text"""
        text_lower = text.lower()
        
        for outcome, indicators in self.outcome_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return outcome
        
        return "ongoing"  # Default to ongoing if not specified
    
    def process_report(self, report_text: str) -> Dict[str, Any]:
        """Process a medical report and extract structured data"""
        return {
            'drug': self.extract_drug(report_text),
            'adverse_events': self.extract_adverse_events(report_text),
            'severity': self.extract_severity(report_text),
            'outcome': self.extract_outcome(report_text)
        }
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Simple translation function (mock implementation)"""
        translations = {
            'french': {
                'recovered': 'rétabli',
                'ongoing': 'en cours',
                'fatal': 'fatal',
                'mild': 'léger',
                'moderate': 'modéré',
                'severe': 'sévère',
                'nausea': 'nausée',
                'headache': 'mal de tête',
                'dizziness': 'étourdissement',
                'rash': 'éruption cutanée',
                'fatigue': 'fatigue',
                'diarrhea': 'diarrhée',
                'vomiting': 'vomissements',
                'fever': 'fièvre',
                'pain': 'douleur',
                'swelling': 'gonflement'
            },
            'swahili': {
                'recovered': 'amepona',
                'ongoing': 'inaendelea',
                'fatal': 'la kufa',
                'mild': 'nyepesi',
                'moderate': 'wastani',
                'severe': 'kali',
                'nausea': 'kichefuchefu',
                'headache': 'kichwa cha maumivu',
                'dizziness': 'kizunguzungu',
                'rash': 'mashavu',
                'fatigue': 'uchovu',
                'diarrhea': 'kuhara',
                'vomiting': 'kutapika',
                'fever': 'homa',
                'pain': 'maumivu',
                'swelling': 'uvimbe'
            }
        }
        
        if target_language.lower() in translations:
            return translations[target_language.lower()].get(text.lower(), text)
        
        return text


# Global instance
nlp_processor = NLPProcessor()
