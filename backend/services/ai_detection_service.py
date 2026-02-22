import cv2
import numpy as np
from PIL import Image
import os

class AIDetectionService:
    
    @staticmethod
    def detect_ai_generated(file_path):
        score = 0
        indicators = []
        
        try:
            img = cv2.imread(file_path)
            
            face_analysis = AIDetectionService._analyze_face_authenticity(img)
            score += face_analysis['score']
            indicators.extend(face_analysis['indicators'])
            
            texture_analysis = AIDetectionService._analyze_texture_patterns(img)
            score += texture_analysis['score']
            indicators.extend(texture_analysis['indicators'])
            
        except Exception as e:
            print(f"AI detection failed: {e}")
        
        return {
            'ai_score': min(score, 100),
            'is_likely_ai': score > 70,
            'ai_indicators': indicators
        }
    
    @staticmethod
    def _analyze_face_authenticity(img):
        score = 0
        indicators = []
        
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = img[y:y+h, x:x+w]
                face_gray = gray[y:y+h, x:x+w]
                
                face_hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
                h_channel, s_channel, v_channel = cv2.split(face_hsv)
                
                s_std = np.std(s_channel)
                if s_std < 10:
                    indicators.append('Face has extremely uniform skin tone - AI characteristic')
                    score += 30
                
                laplacian = cv2.Laplacian(face_gray, cv2.CV_64F)
                sharpness = laplacian.var()
                
                if sharpness > 2000:
                    indicators.append('Face unnaturally sharp - possible composite')
                    score += 25
                
                edges = cv2.Canny(face_gray, 50, 150)
                edge_density = np.sum(edges > 0) / edges.size
                
                if edge_density < 0.015:
                    indicators.append('Face lacks natural pores and detail - AI-generated')
                    score += 35
                
        except Exception as e:
            print(f"Face analysis failed: {e}")
        
        return {'score': score, 'indicators': indicators}
    
    @staticmethod
    def _analyze_texture_patterns(img):
        score = 0
        indicators = []
        
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            from skimage.feature import graycomatrix, graycoprops
            gray_scaled = (gray / 16).astype(np.uint8)
            glcm = graycomatrix(gray_scaled, [1], [0], symmetric=True, normed=True)
            homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
            
            if homogeneity > 0.9:
                indicators.append('Document texture extremely uniform - suspicious')
                score += 30
            
        except Exception as e:
            print(f"Texture analysis failed: {e}")
        
        return {'score': score, 'indicators': indicators}