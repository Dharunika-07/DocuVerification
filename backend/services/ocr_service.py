# #after claude
# import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter
# import cv2
# import numpy as np
# import os

# class OCRService:
#     @staticmethod
#     def extract_text(file_path):
#         try:
#             if file_path.lower().endswith('.pdf'):
#                 return OCRService._extract_from_pdf(file_path)
#             else:
#                 return OCRService._extract_from_image(file_path)
#         except Exception as e:
#             return f"Error extracting text: {str(e)}"
    
#     @staticmethod
#     def _preprocess_image(file_path):
#         img = cv2.imread(file_path)
        
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#         denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
#         thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
#         temp_path = file_path + '_processed.jpg'
#         cv2.imwrite(temp_path, thresh)
        
#         return temp_path
    
#     @staticmethod
#     def _extract_from_image(file_path):
#         try:
#             processed_path = OCRService._preprocess_image(file_path)
            
#             config = '--oem 3 --psm 6'
#             text = pytesseract.image_to_string(
#                 Image.open(processed_path), 
#                 lang='eng+hin+tam',
#                 config=config
#             )
            
#             if os.path.exists(processed_path):
#                 os.remove(processed_path)
            
#             return text.strip()
#         except Exception as e:
#             return f"Error: {str(e)}"
    
#     @staticmethod
#     def _extract_from_pdf(file_path):
#         try:
#             from pdf2image import convert_from_path
#             images = convert_from_path(file_path)
#             text = ""
#             for image in images:
#                 text += pytesseract.image_to_string(image, lang='eng+hin+tam') + "\n"
#             return text.strip()
#         except Exception as e:
#             return f"Error extracting PDF text: {str(e)}"

#writing this for correcting blur though the code is running correct
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os
import re

class OCRService:
    @staticmethod
    def extract_text(file_path, document_type='general'):
        try:
            if file_path.lower().endswith('.pdf'):
                return OCRService._extract_from_pdf(file_path, document_type)
            else:
                return OCRService._extract_from_image_advanced(file_path, document_type)
        except Exception as e:
            print(f"Error extracting text: {e}")
            return f"Error extracting text: {str(e)}"
    
    @staticmethod
    def _detect_blur(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var < 100
    
    @staticmethod
    def _auto_rotate(image):
        try:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb)
            
            osd = pytesseract.image_to_osd(pil_image)
            rotation_angle = int(re.search(r'Rotate: (\d+)', osd).group(1))
            
            if rotation_angle != 0:
                print(f"Auto-rotating image by {rotation_angle} degrees")
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
                image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        except Exception as e:
            print(f"Auto-rotation failed: {e}")
        
        return image
    
    @staticmethod
    def _deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        if abs(angle) > 0.5:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return image
    
    @staticmethod
    def _sharpen_image(image):
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return sharpened
    
    @staticmethod
    def _unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened
    
    @staticmethod
    def _denoise_image(image):
        return cv2.fastNlMeansDenoising(image, None, h=10, templateWindowSize=7, searchWindowSize=21)
    
    @staticmethod
    def _enhance_contrast(image):
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        return clahe.apply(image)
    
    @staticmethod
    def _binarize_image(image):
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        binary = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        return binary
    
    @staticmethod
    def _morphological_operations(image):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
        return closing
    
    @staticmethod
    def _remove_shadows(image):
        rgb_planes = cv2.split(image)
        result_planes = []
        
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(norm_img)
        
        return cv2.merge(result_planes)
    
    @staticmethod
    def _preprocess_pipeline(file_path):
        processed_images = []
        
        original = cv2.imread(file_path)
        if original is None:
            raise Exception("Failed to load image")
        
        original = OCRService._auto_rotate(original)
        
        is_blurry = OCRService._detect_blur(original)
        print(f"Image blur detected: {is_blurry}")
        
        shadow_removed = OCRService._remove_shadows(original)
        gray = cv2.cvtColor(shadow_removed, cv2.COLOR_BGR2GRAY)
        
        denoised = OCRService._denoise_image(gray)
        
        if is_blurry:
            print("Applying blur correction techniques...")
            
            sharpened = OCRService._sharpen_image(denoised)
            processed_images.append(('sharpened', sharpened))
            
            unsharp = OCRService._unsharp_mask(denoised, kernel_size=(5, 5), sigma=1.0, amount=2.0)
            processed_images.append(('unsharp_mask', unsharp))
            
            kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
            enhanced_sharp = cv2.filter2D(denoised, -1, kernel)
            processed_images.append(('enhanced_sharp', enhanced_sharp))
        
        contrast_enhanced = OCRService._enhance_contrast(denoised)
        processed_images.append(('contrast_enhanced', contrast_enhanced))
        
        deskewed = OCRService._deskew(contrast_enhanced)
        processed_images.append(('deskewed', deskewed))
        
        binary = OCRService._binarize_image(deskewed)
        processed_images.append(('binary', binary))
        
        morph = OCRService._morphological_operations(binary)
        processed_images.append(('morphological', morph))
        
        _, otsu = cv2.threshold(deskewed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_images.append(('otsu', otsu))
        
        processed_images.append(('original_gray', gray))
        
        temp_paths = []
        for name, img in processed_images:
            temp_path = f"{file_path}_{name}.jpg"
            cv2.imwrite(temp_path, img)
            temp_paths.append(temp_path)
        
        return temp_paths
    
    @staticmethod
    def _extract_from_image_advanced(file_path, document_type='general'):
        all_texts = []
        
        try:
            processed_paths = OCRService._preprocess_pipeline(file_path)
            
            tesseract_configs = [
                '--oem 3 --psm 6',
                '--oem 3 --psm 3',
                '--oem 3 --psm 4',
                '--oem 3 --psm 11',
                '--oem 3 --psm 12',
                '--oem 1 --psm 6',
            ]
            
            for processed_path in processed_paths:
                for config in tesseract_configs:
                    try:
                        text = pytesseract.image_to_string(
                            Image.open(processed_path),
                            lang='eng',
                            config=config
                        )
                        if text and len(text.strip()) > 10:
                            all_texts.append(text)
                    except Exception as e:
                        print(f"OCR failed for {processed_path} with config {config}: {e}")
                        continue
            
            for processed_path in processed_paths[:3]:
                try:
                    text_data = pytesseract.image_to_data(
                        Image.open(processed_path),
                        lang='eng',
                        config='--oem 3 --psm 6',
                        output_type=pytesseract.Output.DICT
                    )
                    
                    confident_text = []
                    for i, conf in enumerate(text_data['conf']):
                        if int(conf) > 30:
                            word = text_data['text'][i]
                            if word.strip():
                                confident_text.append(word)
                    
                    if confident_text:
                        all_texts.append(' '.join(confident_text))
                except:
                    pass
            
            for processed_path in processed_paths:
                if os.path.exists(processed_path):
                    os.remove(processed_path)
        
        except Exception as e:
            print(f"Preprocessing pipeline failed: {e}")
        
        try:
            original_text = pytesseract.image_to_string(
                Image.open(file_path),
                lang='eng',
                config='--oem 3 --psm 6'
            )
            all_texts.append(original_text)
        except:
            pass
        
        print(f"Extracted {len(all_texts)} text variations")
        
        best_text = OCRService._select_best_text(all_texts)
        cleaned_text = OCRService._clean_extracted_text(best_text)
        structured_text = OCRService._extract_structured_info(cleaned_text, document_type)
        
        return structured_text
    
    @staticmethod
    def _select_best_text(texts):
        if not texts:
            return ""
        
        scored_texts = []
        for text in texts:
            score = 0
            
            if re.search(r'\d{4}\s?\d{4}\s?\d{4}', text):
                score += 100
            
            if re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', text):
                score += 50
            
            if re.search(r'(?i)(aadhaar|government|india|name|address|dob|birth|passport|license|pan)', text):
                score += 30
            
            id_patterns = [
                r'\b[A-Z]{5}\d{4}[A-Z]\b',
                r'\b[A-Z]{2}\d{13}\b',
                r'\b[A-Z]{3}\d{7}\b',
                r'\d{4}/\d{5}/\d{5}',
            ]
            for pattern in id_patterns:
                if re.search(pattern, text):
                    score += 40
            
            alpha_count = len(re.findall(r'[a-zA-Z]', text))
            digit_count = len(re.findall(r'\d', text))
            total_chars = len(text)
            
            if total_chars > 0:
                alpha_ratio = alpha_count / total_chars
                digit_ratio = digit_count / total_chars
                score += (alpha_ratio * 20) + (digit_ratio * 10)
            
            word_count = len(text.split())
            score += min(word_count * 0.5, 30)
            
            gibberish_count = len(re.findall(r'[^a-zA-Z0-9\s:,./\-()]', text))
            gibberish_penalty = (gibberish_count / (total_chars + 1)) * 50
            score -= gibberish_penalty
            
            scored_texts.append((score, text))
        
        scored_texts.sort(reverse=True, key=lambda x: x[0])
        
        print(f"Best text score: {scored_texts[0][0]}")
        return scored_texts[0][1] if scored_texts else ""
    
    @staticmethod
    def _clean_extracted_text(text):
        if not text:
            return ""
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            if len(line) < 2:
                continue
            
            if re.match(r'^[^a-zA-Z0-9]+$', line):
                continue
            
            gibberish_ratio = len(re.findall(r'[^a-zA-Z0-9\s:,./\-()@]', line)) / (len(line) + 1)
            if gibberish_ratio > 0.4:
                continue
            
            consecutive_special = re.search(r'[^a-zA-Z0-9\s]{4,}', line)
            if consecutive_special:
                continue
            
            line = re.sub(r'[^\w\s:,./\-()@]', ' ', line)
            line = re.sub(r'\s+', ' ', line)
            
            cleaned_lines.append(line)
        
        cleaned_text = '\n'.join(cleaned_lines)
        
        return cleaned_text.strip()
    
    @staticmethod
    def _extract_structured_info(text, document_type='general'):
        structured_parts = []
        
        document_type = document_type.lower()
        
        if document_type == 'id_proof':
            structured_parts.extend(OCRService._extract_id_proof_fields(text))
        elif document_type == 'address_proof':
            structured_parts.extend(OCRService._extract_address_proof_fields(text))
        elif document_type == 'income_proof':
            structured_parts.extend(OCRService._extract_income_proof_fields(text))
        elif document_type == 'contract':
            structured_parts.extend(OCRService._extract_contract_fields(text))
        else:
            structured_parts.extend(OCRService._extract_general_fields(text))
        
        if structured_parts:
            structured_text = '\n'.join(structured_parts)
            return f"=== EXTRACTED INFORMATION ===\n{structured_text}\n\n=== ORIGINAL TEXT ===\n{text}"
        
        return text
    
    @staticmethod
    def _extract_id_proof_fields(text):
        fields = []
        
        aadhaar_patterns = [
            r'(\d{4}\s\d{4}\s\d{4})',
            r'(\d{12})',
        ]
        for pattern in aadhaar_patterns:
            aadhaar_match = re.search(pattern, text)
            if aadhaar_match:
                number = aadhaar_match.group(1)
                if len(number.replace(' ', '')) == 12:
                    fields.append(f"Aadhaar Number: {number}")
                    break
        
        pan_match = re.search(r'\b([A-Z]{5}\d{4}[A-Z])\b', text)
        if pan_match:
            fields.append(f"PAN Number: {pan_match.group(1)}")
        
        passport_match = re.search(r'\b([A-Z]\d{7}|[A-Z]{2}\d{7})\b', text)
        if passport_match:
            fields.append(f"Passport Number: {passport_match.group(1)}")
        
        dl_patterns = [
            r'\b([A-Z]{2}\d{13})\b',
            r'\b([A-Z]{2}-\d{13})\b',
            r'\b([A-Z]{2}\d{2}\s?\d{11})\b',
        ]
        for pattern in dl_patterns:
            dl_match = re.search(pattern, text)
            if dl_match:
                fields.append(f"Driving License: {dl_match.group(1)}")
                break
        
        voter_match = re.search(r'\b([A-Z]{3}\d{7})\b', text)
        if voter_match:
            fields.append(f"Voter ID: {voter_match.group(1)}")
        
        enrollment_match = re.search(r'(\d{4}/\d{5}/\d{5})', text)
        if enrollment_match:
            fields.append(f"Enrollment Number: {enrollment_match.group(1)}")
        
        dob_patterns = [
            r'(?:DOB|Date of Birth|D\.O\.B|Birth)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})',
            r'\b(\d{2}[/-]\d{2}[/-]\d{4})\b',
        ]
        for pattern in dob_patterns:
            dob_match = re.search(pattern, text, re.IGNORECASE)
            if dob_match:
                fields.append(f"Date of Birth: {dob_match.group(1)}")
                break
        
        yob_match = re.search(r'(?:Year of Birth|YOB)[\s:]*(\d{4})', text, re.IGNORECASE)
        if yob_match:
            fields.append(f"Year of Birth: {yob_match.group(1)}")
        
        name_patterns = [
            r'(?:Name|Full Name)[\s:]+([A-Z][a-zA-Z\s]{3,50})',
            r'(?:To)[\s:]+([A-Z][a-zA-Z\s]{3,50})',
        ]
        for pattern in name_patterns:
            name_match = re.search(pattern, text)
            if name_match:
                name = name_match.group(1).strip()
                if len(name.split()) >= 2:
                    fields.append(f"Name: {name}")
                    break
        
        father_match = re.search(r'(?:Father|S/O|Son of)[\s:]+([A-Z][a-zA-Z\s]{3,50})', text, re.IGNORECASE)
        if father_match:
            fields.append(f"Father Name: {father_match.group(1).strip()}")
        
        gender_match = re.search(r'(?:Gender|Sex)[\s:]*([MaleFemale]+)', text, re.IGNORECASE)
        if gender_match:
            fields.append(f"Gender: {gender_match.group(1)}")
        
        address_match = re.search(r'(?:Address|D/O|S/O|C/O)[\s:]+(.+?)(?:\d{6}|\n\n|$)', text, re.IGNORECASE | re.DOTALL)
        if address_match:
            address = address_match.group(1).strip()
            address = ' '.join(address.split())[:200]
            if len(address) > 10:
                fields.append(f"Address: {address}")
        
        pincode_match = re.search(r'\b(\d{6})\b', text)
        if pincode_match:
            fields.append(f"Pincode: {pincode_match.group(1)}")
        
        phone_match = re.search(r'\b([6-9]\d{9})\b', text)
        if phone_match:
            fields.append(f"Mobile: {phone_match.group(1)}")
        
        return fields
    
    @staticmethod
    def _extract_address_proof_fields(text):
        fields = []
        
        name_patterns = [
            r'(?:Name|Customer Name|Account Holder)[\s:]+([A-Z][a-zA-Z\s]{3,50})',
        ]
        for pattern in name_patterns:
            name_match = re.search(pattern, text, re.IGNORECASE)
            if name_match:
                fields.append(f"Name: {name_match.group(1).strip()}")
                break
        
        address_match = re.search(r'(?:Address|Service Address)[\s:]+(.+?)(?:\d{6}|$)', text, re.IGNORECASE | re.DOTALL)
        if address_match:
            address = ' '.join(address_match.group(1).strip().split())[:300]
            if len(address) > 15:
                fields.append(f"Address: {address}")
        
        pincode_match = re.search(r'\b(\d{6})\b', text)
        if pincode_match:
            fields.append(f"Pincode: {pincode_match.group(1)}")
        
        account_match = re.search(r'(?:Account|Consumer|Service)[\s:]+([A-Z0-9\-]{5,20})', text, re.IGNORECASE)
        if account_match:
            fields.append(f"Account Number: {account_match.group(1)}")
        
        date_match = re.search(r'(?:Date|Bill Date)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})', text, re.IGNORECASE)
        if date_match:
            fields.append(f"Date: {date_match.group(1)}")
        
        amount_match = re.search(r'(?:Amount|Total|Due)[\s:]*(?:Rs|INR|₹)?[\s]*([0-9,]+\.?\d*)', text, re.IGNORECASE)
        if amount_match:
            fields.append(f"Amount: Rs. {amount_match.group(1)}")
        
        return fields
    
    @staticmethod
    def _extract_income_proof_fields(text):
        fields = []
        
        name_match = re.search(r'(?:Name|Employee)[\s:]+([A-Z][a-zA-Z\s]{3,50})', text, re.IGNORECASE)
        if name_match:
            fields.append(f"Name: {name_match.group(1).strip()}")
        
        emp_id_match = re.search(r'(?:Employee ID|Emp ID)[\s:]+([A-Z0-9\-]{3,20})', text, re.IGNORECASE)
        if emp_id_match:
            fields.append(f"Employee ID: {emp_id_match.group(1)}")
        
        gross_match = re.search(r'(?:Gross|Total Earnings)[\s:]*(?:Rs|INR|₹)?[\s]*([0-9,]+\.?\d*)', text, re.IGNORECASE)
        if gross_match:
            fields.append(f"Gross Salary: Rs. {gross_match.group(1)}")
        
        net_match = re.search(r'(?:Net|Take Home)[\s:]*(?:Rs|INR|₹)?[\s]*([0-9,]+\.?\d*)', text, re.IGNORECASE)
        if net_match:
            fields.append(f"Net Salary: Rs. {net_match.group(1)}")
        
        return fields
    
    @staticmethod
    def _extract_contract_fields(text):
        fields = []
        
        contract_match = re.search(r'(?:Contract|Agreement)[\s:]+([A-Z0-9\-/]{5,30})', text, re.IGNORECASE)
        if contract_match:
            fields.append(f"Contract Number: {contract_match.group(1)}")
        
        date_match = re.search(r'(?:Date|Dated)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})', text, re.IGNORECASE)
        if date_match:
            fields.append(f"Date: {date_match.group(1)}")
        
        return fields
    
    @staticmethod
    def _extract_general_fields(text):
        fields = []
        
        name_match = re.search(r'(?:Name)[\s:]+([A-Z][a-zA-Z\s]{3,50})', text, re.IGNORECASE)
        if name_match:
            fields.append(f"Name: {name_match.group(1).strip()}")
        
        date_match = re.search(r'\b(\d{2}[/-]\d{2}[/-]\d{4})\b', text)
        if date_match:
            fields.append(f"Date: {date_match.group(1)}")
        
        phone_match = re.search(r'\b([6-9]\d{9})\b', text)
        if phone_match:
            fields.append(f"Mobile: {phone_match.group(1)}")
        
        email_match = re.search(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', text)
        if email_match:
            fields.append(f"Email: {email_match.group(1)}")
        
        return fields
    
    @staticmethod
    def _extract_from_pdf(file_path, document_type='general'):
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(file_path, dpi=400)
            all_text = []
            
            for i, image in enumerate(images):
                temp_image_path = f"{file_path}_page_{i}.jpg"
                image.save(temp_image_path, 'JPEG', quality=95)
                
                text = OCRService._extract_from_image_advanced(temp_image_path, document_type)
                all_text.append(text)
                
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
            
            return '\n\n=== PAGE BREAK ===\n\n'.join(all_text)
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"