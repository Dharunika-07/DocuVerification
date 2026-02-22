# # from datetime import datetime
# # import re

# # class DocumentValidationService:
    
# #     @staticmethod
# #     def validate_document_dates(extracted_text, document_type):
# #         issues = []
# #         is_valid = True
        
# #         if document_type == 'id_proof':
            
# #             expiry_patterns = [
# #                 r'(?:Expiry|Valid Until|Valid Till|Expires?)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
# #                 r'(?:Date of Expiry|Expiry Date)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
# #             ]
            
# #             for pattern in expiry_patterns:
# #                 match = re.search(pattern, extracted_text, re.IGNORECASE)
# #                 if match:
# #                     try:
# #                         date_str = match.group(1)
# #                         expiry_date = DocumentValidationService._parse_date(date_str)
                        
# #                         if expiry_date:
# #                             if expiry_date < datetime.now():
# #                                 issues.append(f'Document expired on {date_str}')
# #                                 is_valid = False
                            
# #                             days_to_expiry = (expiry_date - datetime.now()).days
# #                             if 0 < days_to_expiry < 90:
# #                                 issues.append(f'Document expiring soon (in {days_to_expiry} days)')
# #                     except:
# #                         pass
            
# #             issue_patterns = [
# #                 r'(?:Issue Date|Date of Issue|Issued?)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
# #             ]
            
# #             for pattern in issue_patterns:
# #                 match = re.search(pattern, extracted_text, re.IGNORECASE)
# #                 if match:
# #                     try:
# #                         date_str = match.group(1)
# #                         issue_date = DocumentValidationService._parse_date(date_str)
                        
# #                         if issue_date:
# #                             if issue_date > datetime.now():
# #                                 issues.append(f'Document issue date is in the future: {date_str}')
# #                                 is_valid = False
# #                     except:
# #                         pass
        
# #         return {
# #             'is_valid': is_valid,
# #             'date_issues': issues
# #         }
    
# #     @staticmethod
# #     def _parse_date(date_str):
# #         formats = ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y']
        
# #         for fmt in formats:
# #             try:
# #                 return datetime.strptime(date_str, fmt)
# #             except:
# #                 continue
        
# #         return None
    
# #     @staticmethod
# #     def validate_document_numbers(extracted_text, document_type):
# #         issues = []
# #         is_valid = True
        
# #         if document_type == 'id_proof':
            
# #             aadhaar_match = re.search(r'(\d{4}\s?\d{4}\s?\d{4})', extracted_text)
# #             if aadhaar_match:
# #                 aadhaar = aadhaar_match.group(1).replace(' ', '')
# #                 if len(aadhaar) != 12:
# #                     issues.append(f'Invalid Aadhaar number length: {len(aadhaar)} digits (should be 12)')
# #                     is_valid = False
                
# #                 if aadhaar[0] in ['0', '1']:
# #                     issues.append('Invalid Aadhaar number (cannot start with 0 or 1)')
# #                     is_valid = False
            
# #             pan_match = re.search(r'\b([A-Z]{5}\d{4}[A-Z])\b', extracted_text)
# #             if pan_match:
# #                 pan = pan_match.group(1)
# #                 if not re.match(r'^[A-Z]{3}[PCHFATBLJG][A-Z]\d{4}[A-Z]$', pan):
# #                     issues.append(f'Invalid PAN card format: {pan}')
# #                     is_valid = False
            
# #             passport_match = re.search(r'\b([A-Z]\d{7})\b', extracted_text)
# #             if passport_match:
# #                 passport = passport_match.group(1)
# #                 if passport[0] not in 'ABCDEFGHJKLMNPQRSTUVWXYZ':
# #                     issues.append(f'Invalid passport number format: {passport}')
# #                     is_valid = False
        
# #         return {
# #             'is_valid': is_valid,
# #             'number_issues': issues
# #         }



# #after testing on 5/2
# from datetime import datetime
# import re

# class DocumentValidationService:
    
#     @staticmethod
#     def validate_document_dates(extracted_text, document_type):
#         issues = []
#         is_valid = True
        
#         if document_type == 'id_proof':
#             expiry_patterns = [
#                 r'(?:Expiry|Valid Until|Valid Till|Expires?|Date of Expiry|Eapiry)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
#             ]
            
#             for pattern in expiry_patterns:
#                 match = re.search(pattern, extracted_text, re.IGNORECASE)
#                 if match:
#                     try:
#                         date_str = match.group(1)
#                         expiry_date = DocumentValidationService._parse_date(date_str)
                        
#                         if expiry_date:
#                             today = datetime.now()
                            
#                             if expiry_date < today:
#                                 years_expired = (today - expiry_date).days / 365
#                                 issues.append(f'CRITICAL: Document EXPIRED on {date_str} ({int(years_expired)} years ago)')
#                                 is_valid = False
                            
#                             days_to_expiry = (expiry_date - today).days
#                             if 0 < days_to_expiry < 90:
#                                 issues.append(f'Document expiring soon (in {days_to_expiry} days)')
#                     except Exception as e:
#                         print(f"Date parsing error: {e}")
            
#             issue_patterns = [
#                 r'(?:Issue Date|Date of Issue|Issued?|Faiert of Date of Issue)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
#             ]
            
#             for pattern in issue_patterns:
#                 match = re.search(pattern, extracted_text, re.IGNORECASE)
#                 if match:
#                     try:
#                         date_str = match.group(1)
#                         issue_date = DocumentValidationService._parse_date(date_str)
                        
#                         if issue_date:
#                             if issue_date > datetime.now():
#                                 issues.append(f'CRITICAL: Document issue date is in the future: {date_str}')
#                                 is_valid = False
#                     except:
#                         pass
        
#         return {
#             'is_valid': is_valid,
#             'date_issues': issues
#         }
    
#     @staticmethod
#     def _parse_date(date_str):
#         formats = ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y']
        
#         for fmt in formats:
#             try:
#                 return datetime.strptime(date_str, fmt)
#             except:
#                 continue
        
#         return None
    
#     @staticmethod
#     def validate_document_numbers(extracted_text, document_type):
#         issues = []
#         is_valid = True
        
#         if document_type == 'id_proof':
#             aadhaar_match = re.search(r'(\d{4}\s?\d{4}\s?\d{4})', extracted_text)
#             if aadhaar_match:
#                 aadhaar = aadhaar_match.group(1).replace(' ', '')
#                 if len(aadhaar) != 12:
#                     issues.append(f'Invalid Aadhaar number length: {len(aadhaar)} digits (should be 12)')
#                     is_valid = False
                
#                 if aadhaar[0] in ['0', '1']:
#                     issues.append('Invalid Aadhaar number (cannot start with 0 or 1)')
#                     is_valid = False
            
#             pan_match = re.search(r'\b([A-Z]{5}\d{4}[A-Z])\b', extracted_text)
#             if pan_match:
#                 pan = pan_match.group(1)
#                 if not re.match(r'^[A-Z]{3}[PCHFATBLJG][A-Z]\d{4}[A-Z]$', pan):
#                     issues.append(f'Invalid PAN card format: {pan}')
#                     is_valid = False
            
#             passport_match = re.search(r'\b([A-Z]\d{7})\b', extracted_text)
#             if passport_match:
#                 passport = passport_match.group(1)
#                 if passport[0] not in 'ABCDEFGHJKLMNPQRSTUVWXYZ':
#                     issues.append(f'Invalid passport number format: {passport}')
#                     is_valid = False
        
#         return {
#             'is_valid': is_valid,
#             'number_issues': issues
#         }


from datetime import datetime
import re

class DocumentValidationService:
    
    @staticmethod
    def validate_document_dates(extracted_text, document_type):
        issues = []
        is_valid = True
        
        if document_type == 'id_proof':
            expiry_patterns = [
                r'(?:Expiry|Valid Until|Valid Till|Expires?|Date of Expiry|Eapiry)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
            ]
            
            for pattern in expiry_patterns:
                match = re.search(pattern, extracted_text, re.IGNORECASE)
                if match:
                    try:
                        date_str = match.group(1)
                        expiry_date = DocumentValidationService._parse_date(date_str)
                        
                        if expiry_date:
                            today = datetime.now()
                            
                            if expiry_date < today:
                                years_expired = (today - expiry_date).days / 365
                                issues.append(f'CRITICAL: Document EXPIRED on {date_str} ({int(years_expired)} years ago)')
                                is_valid = False
                    except Exception as e:
                        print(f"Date parsing error: {e}")
            
            issue_patterns = [
                r'(?:Issue Date|Date of Issue|Issued?|Faiert of Date of Issue)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
            ]
            
            for pattern in issue_patterns:
                match = re.search(pattern, extracted_text, re.IGNORECASE)
                if match:
                    try:
                        date_str = match.group(1)
                        issue_date = DocumentValidationService._parse_date(date_str)
                        
                        if issue_date:
                            if issue_date > datetime.now():
                                issues.append(f'Document issue date is in the future: {date_str}')
                                is_valid = False
                    except:
                        pass
        
        return {
            'is_valid': is_valid,
            'date_issues': issues
        }
    
    @staticmethod
    def _parse_date(date_str):
        formats = ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y']
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        
        return None
    
    @staticmethod
    def validate_document_numbers(extracted_text, document_type):
        issues = []
        is_valid = True
        
        if document_type == 'id_proof':
            aadhaar_patterns = [
                r'(\d{4}\s\d{4}\s\d{4})',
                r'(\d{12})',
            ]
            
            found_aadhaar = False
            for pattern in aadhaar_patterns:
                aadhaar_match = re.search(pattern, extracted_text)
                if aadhaar_match:
                    aadhaar = aadhaar_match.group(1).replace(' ', '')
                    
                    if len(aadhaar) == 12:
                        found_aadhaar = True
                        if aadhaar[0] in ['0', '1']:
                            issues.append('Invalid Aadhaar: cannot start with 0 or 1')
                            is_valid = False
                        break
            
            pan_match = re.search(r'\b([A-Z]{5}\d{4}[A-Z])\b', extracted_text)
            if pan_match:
                pan = pan_match.group(1)
                if not re.match(r'^[A-Z]{3}[PCHFATBLJG][A-Z]\d{4}[A-Z]$', pan):
                    issues.append(f'Invalid PAN format')
                    is_valid = False
        
        return {
            'is_valid': is_valid,
            'number_issues': issues
        }