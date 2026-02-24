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