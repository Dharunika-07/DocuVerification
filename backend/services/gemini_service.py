#after gettind ai results for fake passport-edited


import google.generativeai as genai
from config import Config
import json
import re
from datetime import datetime

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def verify_document(self, extracted_text, document_type, forensic_indicators=None, date_issues=None):
        prompt = self._build_verification_prompt(extracted_text, document_type, forensic_indicators, date_issues)
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            
            result = json.loads(result_text.strip())
            return result
        except Exception as e:
            print(f"Gemini API error: {e}")
            return {
                "is_authentic": False,
                "fraud_indicators": ["Technical error during verification"],
                "confidence_score": 0,
                "concerns": [str(e)],
                "analysis": f"Error during verification: {str(e)}",
                "document_identification": "Unknown"
            }
    
    def _build_verification_prompt(self, extracted_text, document_type, forensic_indicators=None, date_issues=None):
        
        forensic_context = ""
        if forensic_indicators and len(forensic_indicators) > 0:
            forensic_context = f"""
CRITICAL FORENSIC ANALYSIS RESULTS:
The following technical fraud indicators were detected by image forensics analysis:
{chr(10).join(f"- {indicator}" for indicator in forensic_indicators)}

IMPORTANT: If forensic analysis shows AI-generation, expired documents, or manipulation, 
the document MUST be marked as inauthentic regardless of text content.
"""

        date_context = ""
        if date_issues and len(date_issues) > 0:
            date_context = f"""
CRITICAL DATE VALIDATION ISSUES:
{chr(10).join(f"- {issue}" for issue in date_issues)}

IMPORTANT: An expired document is INVALID and must be rejected.
"""

        base_prompt = f"""
You are an AI document verification expert for a telecom company in India.

{forensic_context}

{date_context}

CRITICAL INSTRUCTIONS:
1. FIRST, identify what type of document this actually is (Aadhaar, Passport, PAN, Driver's License, Utility Bill, Salary Slip, Contract, etc.)
2. The user claimed document type is: {document_type}
3. If the actual document type does NOT match the claimed type, this is a MAJOR RED FLAG
4. OCR may contain errors - focus on document structure, format, and key identifiable elements
5. Look for country of origin - documents from other countries are RED FLAGS for Indian telecom verification
6. CHECK FOR EXPIRY DATES - Any expired document must be marked as inauthentic
7. If forensic analysis detected AI-generation or manipulation, the document is inauthentic
8. PRIORITY ORDER: Forensic evidence > Date validation > Text content analysis

Extracted Text (may contain OCR errors):
{extracted_text}

DOCUMENT TYPE IDENTIFICATION:
- Check for country indicators (Poland, USA, UK, Germany, France, Canada, Australia, China, Pakistan, 
  Bangladesh, Nepal, Sri Lanka, foreign, passport, international)
- Check for document names (Passport, Aadhaar, License, etc.)
- Check for issuing authorities
- Check for document structure and format
- Check dates - expired documents are INVALID

"""

        if document_type == 'id_proof':
            prompt = base_prompt + """
VERIFICATION CRITERIA FOR ID PROOF:

FOR INDIAN AADHAAR CARD:
- Must have "Aadhaar" or "आधार" or "Government of India" text
- Must have 12-digit Aadhaar number (format: XXXX XXXX XXXX)
- Must have enrollment number (format: XXXX/XXXXX/XXXXX)
- Should have Indian name, address, and pincode
- No expiry date (Aadhaar cards are lifetime valid)
- Should have DOB or Year of Birth
- Language: English/Hindi/Regional Indian languages

FOR INDIAN PAN CARD:
- Must have "Income Tax Department" or "Permanent Account Number"
- 10-character alphanumeric format: AAAAA9999A
- Indian name and signature
- No expiry date

FOR INDIAN PASSPORT:
- Must say "Republic of India" or "भारत गणराज्य"
- Passport number format: 1 letter + 7 digits
- Place of issue should be in India
- Valid for Indian citizens only
- **CRITICAL: Must NOT be expired - check expiry date**
- Expiry date must be in the future

FOR INDIAN DRIVING LICENSE:
- Format: State code (2 letters) + RTO code (2 digits) + Year (4 digits) + Unique number (7 digits)
- Issuing authority should be Indian state transport department
- Should have Indian address
- **CRITICAL: Must NOT be expired - check validity dates**

FOR INDIAN VOTER ID:
- Format: 3 letters + 7 digits
- Election Commission of India logo
- Indian address

RED FLAGS (Any one of these makes document INAUTHENTIC):
- Foreign country names (Poland, USA, UK, Germany, etc.)
- Non-Indian document formats
- Non-Indian names (European, American names for primary Indian ID)
- Foreign addresses
- Document type mismatch (user says "ID proof" but it's a passport from Poland)
- Foreign issuing authorities
- Languages other than English/Hindi/Indian regional languages as primary text
- **EXPIRED DOCUMENTS - any document past its expiry date is INVALID**
- **AI-GENERATED or digitally manipulated images (if forensic analysis detected this)**
- **Documents that lack natural photo characteristics (too perfect, too smooth)**
- Issue date in the future
- Expiry date that has already passed (current date is 2026-02-05)
"""
        
        elif document_type == 'address_proof':
            prompt = base_prompt + """
VERIFICATION CRITERIA FOR ADDRESS PROOF:

VALID INDIAN ADDRESS PROOF DOCUMENTS:
- Utility Bills (Electricity, Water, Gas, Telephone)
- Bank Statements
- Rental Agreement
- Property Tax Receipt
- Ration Card

MUST HAVE:
- Indian address with pincode (6 digits)
- Indian service provider or bank name
- Account/Consumer number
- Bill date or statement period (must be recent - within last 3 months)
- Amount (for bills)
- Name of the account holder

RED FLAGS:
- Non-Indian addresses or countries
- Foreign utility companies
- Foreign bank names
- Wrong document type (passport, ID card as address proof)
- Bills older than 3 months
- **AI-generated or manipulated documents**
"""

        elif document_type == 'income_proof':
            prompt = base_prompt + """
VERIFICATION CRITERIA FOR INCOME PROOF:

VALID INCOME PROOF DOCUMENTS:
- Salary Slips/Pay Stubs
- Bank Statements showing salary credits
- Income Tax Returns (ITR)
- Form 16
- Employment Letter

MUST HAVE:
- Employee name
- Company name
- Salary amount (Gross/Net)
- Month/period (must be recent - within last 3 months)
- Employee ID (optional)
- PAN number (for Indian documents)

RED FLAGS:
- Non-Indian company (unless MNC with Indian operations)
- Foreign currency (USD, EUR, GBP for Indian verification)
- Wrong document type
- Very old salary slips (older than 3 months)
- **AI-generated or manipulated documents**
"""

        elif document_type == 'contract':
            prompt = base_prompt + """
VERIFICATION CRITERIA FOR CONTRACTS:

VALID CONTRACT DOCUMENTS:
- Service Agreements
- Lease/Rental Agreements
- Employment Contracts
- Vendor Agreements

MUST HAVE:
- Parties involved (names)
- Contract number/reference
- Date of execution
- Terms and conditions
- Signatures
- Duration/validity period
- **Must not be expired**

RED FLAGS:
- Incomplete contract
- Missing signatures
- Suspicious terms
- Wrong document type
- **Expired contract**
- **AI-generated or manipulated documents**
"""

        else:
            prompt = base_prompt + """
GENERAL DOCUMENT VERIFICATION:
- Identify the actual document type
- Check for authenticity markers
- Look for tampering signs
- Verify document structure
- **Check for expiry dates**
- **Check for AI-generation indicators**
"""

        prompt += """

FINAL DECISION RULES:
1. If forensic analysis detected AI-generation → is_authentic = FALSE
2. If document is expired → is_authentic = FALSE
3. If document is from foreign country → is_authentic = FALSE
4. If document type doesn't match → is_authentic = FALSE
5. Only if ALL checks pass → consider is_authentic = TRUE

Analyze this document and provide your response in this EXACT JSON format:
{
    "document_identification": "Actual document type identified (e.g., 'Indian Passport - EXPIRED', 'AI-Generated Passport', 'Polish Passport', 'Indian Aadhaar Card')",
    "document_country": "Country of origin of the document",
    "matches_claimed_type": true/false,
    "is_authentic": true/false,
    "fraud_indicators": ["List specific fraud indicators found"],
    "confidence_score": 0-100,
    "concerns": ["List specific concerns"],
    "analysis": "Detailed analysis. If document is EXPIRED, state this clearly. If AI-generated, state this clearly. If foreign, state this clearly. Start with the MAIN reason for rejection."
}

REMEMBER: 
- Expired documents are NEVER authentic
- AI-generated documents are NEVER authentic  
- Foreign documents are NEVER valid for Indian telecom verification
- State the PRIMARY rejection reason first in your analysis
"""

        return prompt


# """
# Gemini AI Service for Document Verification
# Improved for Indian Documents
# """

# import google.generativeai as genai
# import os
# import json
# import re

# class GeminiService:
#     def __init__(self):
#         self.api_key = os.getenv('GEMINI_API_KEY')
#         if self.api_key:
#             genai.configure(api_key=self.api_key)
#             self.model = genai.GenerativeModel('gemini-2.5-flash')
#         else:
#             self.model = None
#             print("⚠️  GEMINI_API_KEY not set")
    
#     def analyze_document(self, extracted_text, document_type, file_path=None):
#         """
#         Analyze document with Gemini AI
#         Improved for Indian documents
#         """
#         if not self.model:
#             return {
#                 'authentic': True,
#                 'confidence': 50,
#                 'analysis': 'AI analysis skipped - no API key configured',
#                 'document_details': {}
#             }
        
#         try:
#             # Clean text
#             text_preview = extracted_text[:3000] if extracted_text else "No text extracted"
            
#             # Build prompt based on document type
#             prompt = self._build_prompt(text_preview, document_type)
            
#             print(f"🤖 Sending to Gemini AI...")
#             print(f"   Document type: {document_type}")
#             print(f"   Text length: {len(text_preview)}")
            
#             # Get response
#             response = self.model.generate_content(prompt)
#             result_text = response.text.strip()
            
#             print(f"   Response received: {len(result_text)} chars")
            
#             # Parse response
#             result = self._parse_response(result_text, extracted_text)
            
#             print(f"   Authentic: {result.get('authentic')}")
#             print(f"   Confidence: {result.get('confidence')}%")
            
#             return result
            
#         except Exception as e:
#             print(f"❌ Gemini Error: {e}")
#             import traceback
#             traceback.print_exc()
            
#             # Fallback - be lenient
#             return {
#                 'authentic': True,
#                 'confidence': 60,
#                 'analysis': f'AI analysis error: {str(e)}',
#                 'document_details': {}
#             }
    
#     def _build_prompt(self, text, document_type):
#         """Build appropriate prompt for document type"""
        
#         if document_type == 'id_proof':
#             return f"""
# You are verifying an INDIAN identity document (Aadhaar/PAN/Passport/Driving License/Voter ID).

# CRITICAL RULES:
# 1. ONLY flag as inauthentic if document is CLEARLY from another country
# 2. Aadhaar cards use Hindi and English - BOTH are valid
# 3. Poor OCR quality does NOT mean fake
# 4. Indian names can be in any format/language
# 5. Look for: "AADHAAR" or "आधार" or "UIDAI" or "Government of India" or 12-digit number

# Extracted OCR Text:
# {text}

# VERIFICATION FOR AADHAAR:
# ✓ 12-digit number (XXXX XXXX XXXX)
# ✓ Indian name (any language)
# ✓ "Government of India" or "UIDAI" or "आधार"
# ✓ Date of Birth
# ✓ Indian address

# FOR PAN CARD:
# ✓ 10-character code (ABCDE1234F)
# ✓ "Income Tax Department"
# ✓ Indian name

# FOR INDIAN PASSPORT:
# ✓ "REPUBLIC OF INDIA" or "भारत गणराज्य"
# ✓ Passport number (8 characters)
# ✓ Indian nationality

# IMPORTANT: If you see Aadhaar/UIDAI/Government of India → Mark as AUTHENTIC.

# Respond ONLY in JSON (no markdown):
# {{
#     "authentic": true,
#     "confidence": 85,
#     "analysis": "Valid Indian Aadhaar card detected. Found: Government of India authority, 12-digit number, Indian name.",
#     "document_details": {{
#         "type_detected": "Aadhaar",
#         "name": "extracted name if found",
#         "id_number": "extracted number if found"
#     }}
# }}
# """
        
#         elif document_type == 'address_proof':
#             return f"""
# Verify INDIAN address proof (utility bill/bank statement/rental agreement).

# Text:
# {text}

# Look for:
# - Indian address with 6-digit PIN code
# - Indian company (BSNL, Jio, HDFC, SBI, electricity board)
# - Bill date
# - Amount in ₹ (INR)

# Mark as inauthentic ONLY if clearly foreign.

# JSON response:
# {{
#     "authentic": true,
#     "confidence": 80,
#     "analysis": "Valid Indian utility bill",
#     "document_details": {{"type_detected": "Utility Bill", "company": "if found"}}
# }}
# """
        
#         elif document_type == 'income_proof':
#             return f"""
# Verify INDIAN income proof (salary slip/Form 16/bank statement).

# Text:
# {text}

# Check for:
# - Indian company name
# - Salary in INR/₹
# - Employee name
# - Tax deductions (PF/TDS/EPF)
# - Pay period/month

# JSON response:
# {{
#     "authentic": true,
#     "confidence": 85,
#     "analysis": "Valid salary slip",
#     "document_details": {{"company": "if found", "employee": "if found"}}
# }}
# """
        
#         else:
#             return f"""
# Analyze this Indian document.

# Text: {text}

# Is this authentic? JSON response:
# {{
#     "authentic": true,
#     "confidence": 70,
#     "analysis": "Document analyzed"
# }}
# """
    
#     def _parse_response(self, result_text, original_text):
#         """Parse Gemini response into structured format"""
        
#         # Remove markdown code blocks
#         result_text = re.sub(r'```json\s*|\s*```', '', result_text)
#         result_text = result_text.strip()
        
#         try:
#             result = json.loads(result_text)
            
#             # Ensure required fields exist
#             if 'authentic' not in result:
#                 result['authentic'] = True
#             if 'confidence' not in result:
#                 result['confidence'] = 70
#             if 'analysis' not in result:
#                 result['analysis'] = 'Document processed'
#             if 'document_details' not in result:
#                 result['document_details'] = {}
            
#             # Sanity checks
#             # If we extracted substantial text, don't give 0% confidence
#             if len(original_text) > 100:
#                 if result.get('confidence', 0) < 30:
#                     result['confidence'] = 60
#                     result['analysis'] += " (Adjusted - sufficient text extracted)"
            
#             # If marked as 100% fake but we have good text extraction, reconsider
#             if not result.get('authentic') and result.get('confidence', 0) > 95:
#                 if len(original_text) > 200:
#                     result['confidence'] = 75  # Reduce overconfidence
            
#             return result
            
#         except json.JSONDecodeError as e:
#             print(f"⚠️  JSON parse error: {e}")
#             print(f"   Raw response: {result_text[:200]}")
            
#             # Fallback parsing - look for keywords
#             text_lower = result_text.lower()
            
#             # Check if response indicates authentic
#             is_authentic = (
#                 'authentic' in text_lower or
#                 'valid' in text_lower or
#                 'genuine' in text_lower or
#                 'aadhaar' in text_lower or
#                 'government of india' in text_lower
#             )
            
#             # Check if response indicates fake
#             is_fake = (
#                 'inauthentic' in text_lower or
#                 'fake' in text_lower or
#                 'forged' in text_lower or
#                 'foreign' in text_lower
#             )
            
#             # Default to authentic if unclear
#             authentic = is_authentic or not is_fake
            
#             return {
#                 'authentic': authentic,
#                 'confidence': 65,
#                 'analysis': result_text[:500] if result_text else 'Unable to analyze',
#                 'document_details': {}
#             }