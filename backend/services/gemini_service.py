# # #after claude
# # import google.generativeai as genai
# # from config import Config
# # import json

# # class GeminiService:
# #     def __init__(self):
# #         genai.configure(api_key=Config.GEMINI_API_KEY)
# #         self.model = genai.GenerativeModel('gemini-2.5-flash')
    
# #     def verify_document(self, extracted_text, document_type):
# #         prompt = f"""
# # You are an AI document verification expert for a telecom company in India.

# # IMPORTANT INSTRUCTIONS:
# # - The extracted text may contain OCR errors, especially with bilingual documents (English/Tamil/Hindi)
# # - Focus on the PRESENCE of key information, not perfect text extraction
# # - Random characters or garbled text from OCR should NOT automatically mean the document is fake
# # - Look for genuine document structure and key identifiable fields

# # Document Type: {document_type}
# # Extracted Text (may contain OCR errors):
# # {extracted_text}

# # For Aadhaar cards, look for:
# # - Aadhaar number (12 digits)
# # - Name
# # - Address
# # - DOB or Year of Birth
# # - Government of India branding
# # - Enrollment number

# # For other ID documents, look for:
# # - Issuing authority
# # - ID number
# # - Personal details
# # - Valid dates

# # Analyze this document and provide:
# # 1. Is this document authentic? (Consider OCR errors - if you see legitimate ID fields despite garbled text, it may still be authentic)
# # 2. List any fraud indicators found (ignore OCR artifacts)
# # 3. Overall confidence score (0-100)
# # 4. Specific concerns or red flags (ignore OCR noise)

# # Respond in JSON format:
# # {{
# #     "is_authentic": true/false,
# #     "fraud_indicators": ["indicator1", "indicator2"],
# #     "confidence_score": 0-100,
# #     "concerns": ["concern1", "concern2"],
# #     "analysis": "detailed analysis"
# # }}
# # """
        
# #         try:
# #             response = self.model.generate_content(prompt)
# #             result_text = response.text.strip()
            
# #             if result_text.startswith('```json'):
# #                 result_text = result_text[7:]
# #             if result_text.endswith('```'):
# #                 result_text = result_text[:-3]
            
# #             result = json.loads(result_text.strip())
# #             return result
# #         except Exception as e:
# #             print(f"Gemini API error: {e}")
# #             return {
# #                 "is_authentic": True,
# #                 "fraud_indicators": ["OCR extraction issues"],
# #                 "confidence_score": 50,
# #                 "concerns": ["Unable to verify due to technical error"],
# #                 "analysis": f"Technical error during verification: {str(e)}"
# #             }



# #Running correctly but just small changes after testing with fake passport
# import google.generativeai as genai
# from config import Config
# import json

# class GeminiService:
#     def __init__(self):
#         genai.configure(api_key=Config.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel('gemini-2.5-flash')
    
#     def verify_document(self, extracted_text, document_type):
#         prompt = self._build_verification_prompt(extracted_text, document_type)
        
#         try:
#             response = self.model.generate_content(prompt)
#             result_text = response.text.strip()
            
#             if result_text.startswith('```json'):
#                 result_text = result_text[7:]
#             if result_text.endswith('```'):
#                 result_text = result_text[:-3]
            
#             result = json.loads(result_text.strip())
#             return result
#         except Exception as e:
#             print(f"Gemini API error: {e}")
#             return {
#                 "is_authentic": False,
#                 "fraud_indicators": ["Technical error during verification"],
#                 "confidence_score": 0,
#                 "concerns": [str(e)],
#                 "analysis": f"Error during verification: {str(e)}",
#                 "document_identification": "Unknown"
#             }
    
#     def _build_verification_prompt(self, extracted_text, document_type):
#         base_prompt = f"""
# You are an AI document verification expert for a telecom company in India.

# CRITICAL INSTRUCTIONS:
# 1. FIRST, identify what type of document this actually is (Aadhaar, Passport, PAN, Driver's License, Utility Bill, Salary Slip, Contract, etc.)
# 2. The user claimed document type is: {document_type}
# 3. If the actual document type does NOT match the claimed type, this is a MAJOR RED FLAG
# 4. OCR may contain errors - focus on document structure, format, and key identifiable elements
# 5. Look for country of origin - documents from other countries are RED FLAGS for Indian telecom verification

# Extracted Text (may contain OCR errors):
# {extracted_text}

# DOCUMENT TYPE IDENTIFICATION:
# - Check for country indicators (Poland, USA, UK, etc. = NOT valid for Indian telecom)
# - Check for document names (Passport, Aadhaar, License, etc.)
# - Check for issuing authorities
# - Check for document structure and format

# """

#         if document_type == 'id_proof':
#             prompt = base_prompt + """
# VERIFICATION CRITERIA FOR ID PROOF:

# FOR INDIAN AADHAAR CARD:
# - Must have "Aadhaar" or "आधार" or "Government of India" text
# - Must have 12-digit Aadhaar number (format: XXXX XXXX XXXX)
# - Must have enrollment number (format: XXXX/XXXXX/XXXXX)
# - Should have Indian name, address, and pincode
# - No expiry date (Aadhaar cards are lifetime valid)
# - Should have DOB or Year of Birth
# - Language: English/Hindi/Regional Indian languages

# FOR INDIAN PAN CARD:
# - Must have "Income Tax Department" or "Permanent Account Number"
# - 10-character alphanumeric format: AAAAA9999A
# - Indian name and signature
# - No expiry date

# FOR INDIAN PASSPORT:
# - Must say "Republic of India" or "भारत गणराज्य"
# - Passport number format: 1 letter + 7 digits
# - Place of issue should be in India
# - Valid for Indian citizens only

# FOR INDIAN DRIVING LICENSE:
# - Format: State code (2 letters) + RTO code (2 digits) + Year (4 digits) + Unique number (7 digits)
# - Issuing authority should be Indian state transport department
# - Should have Indian address

# FOR INDIAN VOTER ID:
# - Format: 3 letters + 7 digits
# - Election Commission of India logo
# - Indian address

# RED FLAGS:
# - Foreign country names (Poland, USA, UK, Germany, etc.)
# - Non-Indian document formats
# - Non-Indian names (European, American names for primary Indian ID)
# - Foreign addresses
# - Document type mismatch (user says "ID proof" but it's a passport from Poland)
# - Foreign issuing authorities
# - Languages other than English/Hindi/Indian regional languages as primary text
# """
        
#         elif document_type == 'address_proof':
#             prompt = base_prompt + """
# VERIFICATION CRITERIA FOR ADDRESS PROOF:

# VALID INDIAN ADDRESS PROOF DOCUMENTS:
# - Utility Bills (Electricity, Water, Gas, Telephone)
# - Bank Statements
# - Rental Agreement
# - Property Tax Receipt
# - Ration Card

# MUST HAVE:
# - Indian address with pincode (6 digits)
# - Indian service provider or bank name
# - Account/Consumer number
# - Bill date or statement period
# - Amount (for bills)
# - Name of the account holder

# RED FLAGS:
# - Non-Indian addresses or countries
# - Foreign utility companies
# - Foreign bank names
# - Wrong document type (passport, ID card as address proof)
# """

#         elif document_type == 'income_proof':
#             prompt = base_prompt + """
# VERIFICATION CRITERIA FOR INCOME PROOF:

# VALID INCOME PROOF DOCUMENTS:
# - Salary Slips/Pay Stubs
# - Bank Statements showing salary credits
# - Income Tax Returns (ITR)
# - Form 16
# - Employment Letter

# MUST HAVE:
# - Employee name
# - Company name
# - Salary amount (Gross/Net)
# - Month/period
# - Employee ID (optional)
# - PAN number (for Indian documents)

# RED FLAGS:
# - Non-Indian company (unless MNC with Indian operations)
# - Foreign currency (USD, EUR, GBP for Indian verification)
# - Wrong document type
# """

#         elif document_type == 'contract':
#             prompt = base_prompt + """
# VERIFICATION CRITERIA FOR CONTRACTS:

# VALID CONTRACT DOCUMENTS:
# - Service Agreements
# - Lease/Rental Agreements
# - Employment Contracts
# - Vendor Agreements

# MUST HAVE:
# - Parties involved (names)
# - Contract number/reference
# - Date of execution
# - Terms and conditions
# - Signatures
# - Duration/validity period

# RED FLAGS:
# - Incomplete contract
# - Missing signatures
# - Suspicious terms
# - Wrong document type
# """

#         else:
#             prompt = base_prompt + """
# GENERAL DOCUMENT VERIFICATION:
# - Identify the actual document type
# - Check for authenticity markers
# - Look for tampering signs
# - Verify document structure
# """

#         prompt += """

# Analyze this document and provide your response in this EXACT JSON format:
# {
#     "document_identification": "Actual document type identified (e.g., 'Polish Passport', 'Indian Aadhaar Card', 'US Driver's License', 'Indian Utility Bill')",
#     "document_country": "Country of origin of the document",
#     "matches_claimed_type": true/false,
#     "is_authentic": true/false,
#     "fraud_indicators": ["List specific fraud indicators found"],
#     "confidence_score": 0-100,
#     "concerns": ["List specific concerns"],
#     "analysis": "Detailed analysis explaining your verdict. If document type doesn't match or is from wrong country, explain this clearly."
# }

# IMPORTANT: 
# - If this is a foreign document (non-Indian), clearly state it's INVALID for Indian telecom verification
# - If document type doesn't match claimed type, set is_authentic to FALSE
# - Be specific about what document this actually is
# """

#         return prompt



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