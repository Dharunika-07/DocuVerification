# import cv2
# import numpy as np
# from PIL import Image
# from PIL.ExifTags import TAGS
# import os
# from datetime import datetime

# class ImageForensicsService:
    
#     @staticmethod
#     def analyze_image(file_path):
#         results = {
#             'is_suspicious': False,
#             'suspicion_score': 0,
#             'forensic_indicators': []
#         }
        
#         results.update(ImageForensicsService._check_metadata(file_path))
#         results.update(ImageForensicsService._check_quality(file_path))
#         results.update(ImageForensicsService._detect_manipulation(file_path))
#         results.update(ImageForensicsService._check_face_quality(file_path))
        
#         total_score = results['suspicion_score']
        
#         if total_score > 50:
#             results['is_suspicious'] = True
        
#         return results
    
#     @staticmethod
#     def _check_metadata(file_path):
#         indicators = []
#         score = 0
        
#         try:
#             image = Image.open(file_path)
            
#             if not hasattr(image, '_getexif') or image._getexif() is None:
#                 indicators.append('No EXIF metadata - possible screenshot or edited image')
#                 score += 20
#             else:
#                 exif_data = image._getexif()
#                 if exif_data:
#                     exif_dict = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
                    
#                     if 'Software' in exif_dict:
#                         software = str(exif_dict['Software']).lower()
#                         editing_tools = ['photoshop', 'gimp', 'paint', 'canva', 'pixlr', 'snapseed']
#                         if any(tool in software for tool in editing_tools):
#                             indicators.append(f'Edited with image editing software: {exif_dict["Software"]}')
#                             score += 40
                    
#                     if 'Make' not in exif_dict and 'Model' not in exif_dict:
#                         indicators.append('No camera information - possible synthetic/AI-generated image')
#                         score += 25
                    
#                     if 'DateTime' in exif_dict:
#                         try:
#                             date_str = exif_dict['DateTime']
#                             img_date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
#                             days_old = (datetime.now() - img_date).days
                            
#                             if days_old < 1:
#                                 indicators.append('Image created very recently (within 24 hours)')
#                                 score += 10
#                         except:
#                             pass
#         except Exception as e:
#             indicators.append('Unable to read image metadata')
#             score += 15
        
#         return {
#             'metadata_indicators': indicators,
#             'metadata_score': score
#         }
    
#     @staticmethod
#     def _check_quality(file_path):
#         indicators = []
#         score = 0
        
#         try:
#             img = cv2.imread(file_path)
            
#             if img.shape[0] < 400 or img.shape[1] < 400:
#                 indicators.append('Very low resolution - suspicious for official document')
#                 score += 20
            
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
#             if laplacian_var < 50:
#                 indicators.append('Extremely blurry image - possible screenshot or low-quality scan')
#                 score += 25
            
#             mean_brightness = np.mean(gray)
#             if mean_brightness < 40 or mean_brightness > 220:
#                 indicators.append('Abnormal brightness levels - possible manipulation')
#                 score += 15
            
#             file_size = os.path.getsize(file_path)
#             if file_size < 50000:
#                 indicators.append('Very small file size - possible compressed/edited image')
#                 score += 15
            
#         except Exception as e:
#             indicators.append(f'Quality check failed: {str(e)}')
        
#         return {
#             'quality_indicators': indicators,
#             'quality_score': score
#         }
    
#     @staticmethod
#     def _detect_manipulation(file_path):
#         indicators = []
#         score = 0
        
#         try:
#             img = cv2.imread(file_path)
            
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
#             edges = cv2.Canny(gray, 50, 150)
#             edge_density = np.sum(edges > 0) / edges.size
            
#             if edge_density < 0.01:
#                 indicators.append('Very low edge density - possible AI-generated smooth image')
#                 score += 20
            
#             hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
#             hist = hist.flatten()
            
#             peaks = 0
#             for i in range(1, 255):
#                 if hist[i] > hist[i-1] and hist[i] > hist[i+1]:
#                     peaks += 1
            
#             if peaks < 5:
#                 indicators.append('Abnormal histogram - possible digital manipulation')
#                 score += 15
            
#             hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#             h, s, v = cv2.split(hsv)
            
#             if np.std(s) < 10:
#                 indicators.append('Unusually uniform saturation - possible synthetic image')
#                 score += 20
            
#         except Exception as e:
#             indicators.append(f'Manipulation detection failed: {str(e)}')
        
#         return {
#             'manipulation_indicators': indicators,
#             'manipulation_score': score
#         }
    
#     @staticmethod
#     def _check_face_quality(file_path):
#         indicators = []
#         score = 0
        
#         try:
#             img = cv2.imread(file_path)
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
#             face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
#             faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
#             if len(faces) == 0:
#                 indicators.append('No face detected in photo area - suspicious for ID document')
#                 score += 30
#             elif len(faces) > 1:
#                 indicators.append('Multiple faces detected - suspicious for ID document')
#                 score += 35
#             else:
#                 x, y, w, h = faces[0]
#                 face_roi = gray[y:y+h, x:x+w]
                
#                 laplacian_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
#                 if laplacian_var < 30:
#                     indicators.append('Face area is very blurry - possible AI generation or heavy editing')
#                     score += 25
                
#                 face_area = w * h
#                 total_area = img.shape[0] * img.shape[1]
#                 face_ratio = face_area / total_area
                
#                 if face_ratio < 0.02:
#                     indicators.append('Face too small - unusual for ID document photo')
#                     score += 15
#                 elif face_ratio > 0.5:
#                     indicators.append('Face too large - unusual for ID document photo')
#                     score += 15
        
#         except Exception as e:
#             indicators.append('Face detection check failed')
        
#         return {
#             'face_indicators': indicators,
#             'face_score': score
#         }



import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime

class ImageForensicsService:
    
    @staticmethod
    def analyze_image(file_path):
        results = {
            'is_suspicious': False,
            'suspicion_score': 0,
            'forensic_indicators': []
        }
        
        results.update(ImageForensicsService._check_metadata(file_path))
        results.update(ImageForensicsService._check_quality(file_path))
        results.update(ImageForensicsService._detect_manipulation(file_path))
        results.update(ImageForensicsService._check_face_quality(file_path))
        
        total_score = results['suspicion_score']
        
        if total_score > 80:
            results['is_suspicious'] = True
        
        return results
    
    @staticmethod
    def _check_metadata(file_path):
        indicators = []
        score = 0
        
        try:
            image = Image.open(file_path)
            
            if not hasattr(image, '_getexif') or image._getexif() is None:
                indicators.append('No EXIF metadata (common for scanned documents)')
                score += 5
            else:
                exif_data = image._getexif()
                if exif_data:
                    exif_dict = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
                    
                    if 'Software' in exif_dict:
                        software = str(exif_dict['Software']).lower()
                        editing_tools = ['photoshop', 'gimp', 'canva', 'pixlr']
                        if any(tool in software for tool in editing_tools):
                            indicators.append(f'Edited with image editing software: {exif_dict["Software"]}')
                            score += 40
                    
                    if 'DateTime' in exif_dict:
                        try:
                            date_str = exif_dict['DateTime']
                            img_date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                            days_old = (datetime.now() - img_date).days
                            
                            if days_old < 1:
                                indicators.append('Image created very recently (within 24 hours)')
                                score += 15
                        except:
                            pass
        except Exception as e:
            pass
        
        return {
            'metadata_indicators': indicators,
            'metadata_score': score
        }
    
    @staticmethod
    def _check_quality(file_path):
        indicators = []
        score = 0
        
        try:
            img = cv2.imread(file_path)
            
            if img.shape[0] < 300 or img.shape[1] < 300:
                indicators.append('Very low resolution')
                score += 20
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            if laplacian_var < 30:
                indicators.append('Extremely blurry image')
                score += 25
            
            file_size = os.path.getsize(file_path)
            if file_size < 30000:
                indicators.append('Very small file size - highly compressed')
                score += 15
            
        except Exception as e:
            pass
        
        return {
            'quality_indicators': indicators,
            'quality_score': score
        }
    
    @staticmethod
    def _detect_manipulation(file_path):
        indicators = []
        score = 0
        
        try:
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist = hist.flatten()
            
            peaks = 0
            for i in range(1, 255):
                if hist[i] > hist[i-1] and hist[i] > hist[i+1]:
                    peaks += 1
            
            if peaks < 3:
                indicators.append('Abnormal histogram distribution')
                score += 15
            
        except Exception as e:
            pass
        
        return {
            'manipulation_indicators': indicators,
            'manipulation_score': score
        }
    
    @staticmethod
    def _check_face_quality(file_path):
        indicators = []
        score = 0
        
        try:
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                pass
            elif len(faces) > 1:
                indicators.append('Multiple faces detected')
                score += 35
            
        except Exception as e:
            pass
        
        return {
            'face_indicators': indicators,
            'face_score': score
        }