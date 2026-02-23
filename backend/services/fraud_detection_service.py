

#after facing issues in officerdashboard

import re
from datetime import datetime

class FraudDetectionService:
    @staticmethod
    def calculate_risk_score(extracted_text, gemini_response):
        risk_score = 0
        fraud_indicators = []
        
        confidence = gemini_response.get('confidence_score', 50)
        if confidence < 50:
            risk_score += 40
            fraud_indicators.append('Low AI confidence in document authenticity')
        elif confidence < 70:
            risk_score += 20
            fraud_indicators.append('Medium AI confidence - requires review')
        
        if not gemini_response.get('is_authentic', True):
            risk_score += 50
            fraud_indicators.append('Document flagged as inauthentic by AI')
        
        matches_claimed_type = gemini_response.get('matches_claimed_type', True)
        if not matches_claimed_type:
            risk_score += 60
            fraud_indicators.append('Document type mismatch - claimed type does not match actual document')
        
        document_identification = gemini_response.get('document_identification', '').lower()
        document_country = gemini_response.get('document_country', '').lower()
        
        foreign_indicators = ['poland', 'usa', 'uk', 'germany', 'france', 'canada', 'australia', 'china', 'pakistan', 
                             'bangladesh', 'nepal', 'sri lanka', 'foreign', 'international']
        
        is_foreign = any(indicator in document_identification or indicator in document_country 
                        for indicator in foreign_indicators)
        
        if is_foreign and 'india' not in document_country:
            risk_score += 80
            fraud_indicators.append(f'Foreign document detected: {document_identification} from {document_country}')
        
        fraud_indicators.extend(gemini_response.get('fraud_indicators', []))
        
        suspicious_patterns = [
            (r'\b(fake|forged|counterfeit|duplicate|specimen|sample)\b', 'Suspicious keywords detected'),
            (r'\b(photoshop|edited|modified|altered)\b', 'Evidence of digital manipulation'),
            (r'\b(test|testing|demo|example)\b', 'Test/demo document indicator'),
        ]
        
        for pattern, indicator in suspicious_patterns:
            if re.search(pattern, extracted_text, re.IGNORECASE):
                risk_score += 15
                fraud_indicators.append(indicator)
        
        if len(extracted_text) < 50:
            risk_score += 15
            fraud_indicators.append('Insufficient text extracted - poor quality or tampered document')
        
        risk_score = min(risk_score, 100)
        
        if risk_score < 30:
            risk_level = 'low'
        elif risk_score < 70:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return risk_score, risk_level, fraud_indicators
    
    @staticmethod
    def auto_decision(risk_score, risk_level):
        # Adjusted thresholds to send more documents to manual review
        if risk_level == 'high' and risk_score > 85:
            return 'rejected'
        elif risk_level == 'low' and risk_score < 20:
            return 'approved'
        else:
            return 'manual_review'  # More documents will require officer review