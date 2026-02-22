

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.document_model import DocumentModel
from models.verification_model import VerificationModel
from models.user_model import UserModel
from services.gemini_service import GeminiService
from services.fraud_detection_service import FraudDetectionService
from services.embedding_service import EmbeddingService
from services.image_forensics_service import ImageForensicsService
from services.document_validation_service import DocumentValidationService
from services.ai_detection_service import AIDetectionService
from utils.response_utils import ResponseUtils
from extensions.db import mongo

verification_bp = Blueprint('verification', __name__, url_prefix='/api/verifications')

@verification_bp.route('/verify/<document_id>', methods=['POST'])
@jwt_required()
def verify_document(document_id):
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(user_id)
    
    if not current_user:
        return ResponseUtils.error('User not found', 404)
    
    document = DocumentModel.find_by_id(document_id)
    if not document:
        return ResponseUtils.error('Document not found', 404)
    
    if str(document['user_id']) != str(current_user['_id']):
        return ResponseUtils.error('Access denied', 403)
    
    fraud_indicators = []
    forensic_score = 0
    
    try:
        print("Starting image forensics analysis...")
        forensics_result = ImageForensicsService.analyze_image(document['file_path'])
        
        forensic_score = (
            forensics_result.get('metadata_score', 0) +
            forensics_result.get('quality_score', 0) +
            forensics_result.get('manipulation_score', 0) +
            forensics_result.get('face_score', 0)
        )
        
        print(f"Forensic score: {forensic_score}")
        
        if forensics_result.get('metadata_indicators'):
            fraud_indicators.extend(forensics_result['metadata_indicators'])
        if forensics_result.get('quality_indicators'):
            fraud_indicators.extend(forensics_result['quality_indicators'])
        if forensics_result.get('manipulation_indicators'):
            fraud_indicators.extend(forensics_result['manipulation_indicators'])
        if forensics_result.get('face_indicators'):
            fraud_indicators.extend(forensics_result['face_indicators'])
    except Exception as e:
        print(f"Forensics analysis failed: {e}")
        import traceback
        traceback.print_exc()
        forensic_score = 0
        forensics_result = {'is_suspicious': False}
    
    try:
        print("Starting AI detection analysis...")
        ai_detection = AIDetectionService.detect_ai_generated(document['file_path'])
        
        print(f"AI detection score: {ai_detection['ai_score']}")
        print(f"Is likely AI: {ai_detection['is_likely_ai']}")
        
        if ai_detection['is_likely_ai']:
            fraud_indicators.append('CRITICAL: Document appears to be AI-generated or heavily manipulated')
            fraud_indicators.extend(ai_detection['ai_indicators'])
            forensic_score += ai_detection['ai_score']
    except Exception as e:
        print(f"AI detection failed: {e}")
        import traceback
        traceback.print_exc()
        ai_detection = {'is_likely_ai': False, 'ai_score': 0, 'ai_indicators': []}
    
    try:
        print("Starting date validation...")
        date_validation = DocumentValidationService.validate_document_dates(
            document['extracted_text'],
            document['document_type']
        )
        
        print(f"Date validation valid: {date_validation['is_valid']}")
        print(f"Date issues: {date_validation['date_issues']}")
        
        if not date_validation['is_valid']:
            fraud_indicators.extend(date_validation['date_issues'])
    except Exception as e:
        print(f"Date validation failed: {e}")
        import traceback
        traceback.print_exc()
        date_validation = {'is_valid': True, 'date_issues': []}
    
    try:
        print("Starting number validation...")
        number_validation = DocumentValidationService.validate_document_numbers(
            document['extracted_text'],
            document['document_type']
        )
        
        print(f"Number validation valid: {number_validation['is_valid']}")
        
        if not number_validation['is_valid']:
            fraud_indicators.extend(number_validation['number_issues'])
    except Exception as e:
        print(f"Number validation failed: {e}")
        import traceback
        traceback.print_exc()
        number_validation = {'is_valid': True, 'number_issues': []}
    
    print("Starting Gemini AI verification...")
    gemini_service = GeminiService()
    
    gemini_forensic_indicators = []
    if ai_detection.get('is_likely_ai', False):
        gemini_forensic_indicators.append("CRITICAL: Image forensics detected AI-generated content")
        gemini_forensic_indicators.append("Document shows unnatural uniformity and lacks photo-realistic details")
    if forensic_score > 50:
        gemini_forensic_indicators.append(f"High forensic suspicion score: {forensic_score}/100")
        gemini_forensic_indicators.append("Image analysis shows signs of digital manipulation")
    if forensics_result.get('is_suspicious', False):
        gemini_forensic_indicators.append("Multiple forensic red flags detected in image analysis")
    
    gemini_date_issues = date_validation.get('date_issues', [])
    
    gemini_response = gemini_service.verify_document(
        document['extracted_text'],
        document['document_type'],
        forensic_indicators=gemini_forensic_indicators if gemini_forensic_indicators else None,
        date_issues=gemini_date_issues if gemini_date_issues else None
    )
    
    print(f"Gemini response: {gemini_response}")
    
    risk_score, risk_level, ai_fraud_indicators = FraudDetectionService.calculate_risk_score(
        document['extracted_text'],
        gemini_response
    )
    
    fraud_indicators.extend(ai_fraud_indicators)
    
    print(f"Initial risk score: {risk_score}")
    print(f"Forensic score to add: {min(forensic_score, 60)}")
    
    risk_score += min(forensic_score, 60)
    
    if not date_validation['is_valid']:
        print("Adding 50 points for expired document")
        risk_score += 50
    
    if not number_validation['is_valid']:
        print("Adding 40 points for invalid document numbers")
        risk_score += 40
    
    if ai_detection.get('is_likely_ai', False):
        print("Adding 30 points for AI-generated content")
        risk_score += 30
    
    risk_score = min(risk_score, 100)
    
    print(f"Final risk score: {risk_score}")
    
    if risk_score < 30:
        risk_level = 'low'
    elif risk_score < 70:
        risk_level = 'medium'
    else:
        risk_level = 'high'
    
    print(f"Risk level: {risk_level}")
    
    auto_decision = FraudDetectionService.auto_decision(risk_score, risk_level)
    
    if forensic_score > 60:
        print("Forensic score > 60, auto-rejecting")
        auto_decision = 'rejected'
    
    if not date_validation['is_valid']:
        print("Date validation failed, auto-rejecting")
        auto_decision = 'rejected'
    
    if ai_detection.get('is_likely_ai', False):
        print("AI-generated detected, auto-rejecting")
        auto_decision = 'rejected'
    
    if not gemini_response.get('is_authentic', True):
        print("Gemini marked as inauthentic, auto-rejecting")
        auto_decision = 'rejected'
    
    print(f"Auto decision: {auto_decision}")
    
    embedding = EmbeddingService.generate_embedding(document['extracted_text'])
    
    duplicates = EmbeddingService.find_duplicates(mongo.db, embedding)
    
    if duplicates:
        fraud_indicators.append(f'Potential duplicate documents found: {len(duplicates)}')
        risk_score = min(risk_score + 20, 100)
        if risk_score >= 70:
            risk_level = 'high'
            auto_decision = 'rejected'
    
    verification_id = VerificationModel.create_verification(
        mongo.db,
        document_id,
        str(current_user['_id']),
        risk_score,
        risk_level,
        gemini_response,
        fraud_indicators,
        auto_decision,
        gemini_response,
        embedding
    )
    
    DocumentModel.update_status(mongo.db, document_id, auto_decision)
    
    print(f"Verification created with ID: {verification_id}")
    
    return ResponseUtils.success({
        'verification_id': str(verification_id),
        'risk_score': risk_score,
        'risk_level': risk_level,
        'auto_decision': auto_decision,
        'fraud_indicators': fraud_indicators,
        'duplicates': duplicates,
        'document_identified_as': gemini_response.get('document_identification', 'Unknown'),
        'document_country': gemini_response.get('document_country', 'Unknown'),
        'matches_claimed_type': gemini_response.get('matches_claimed_type', False),
        'forensic_analysis': {
            'is_suspicious': forensics_result.get('is_suspicious', False),
            'forensic_score': forensic_score
        },
        'ai_detection': {
            'is_likely_ai': ai_detection.get('is_likely_ai', False),
            'ai_score': ai_detection.get('ai_score', 0)
        },
        'date_validation': date_validation,
        'number_validation': number_validation
    }, 'Document verified successfully', 201)

@verification_bp.route('/my-verifications', methods=['GET'])
@jwt_required()
def get_my_verifications():
    try:
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        
        if not current_user:
            return ResponseUtils.error('User not found', 404)
        
        verifications = VerificationModel.find_by_user(mongo.db, str(current_user['_id']))
        return ResponseUtils.success(verifications)
    except Exception as e:
        print(f"Error in get_my_verifications: {e}")
        import traceback
        traceback.print_exc()
        return ResponseUtils.error(str(e), 500)

@verification_bp.route('/<verification_id>', methods=['GET'])
@jwt_required()
def get_verification(verification_id):
    try:
        verification = VerificationModel.find_by_id(verification_id)
        if not verification:
            return ResponseUtils.error('Verification not found', 404)
        return ResponseUtils.success(verification)
    except Exception as e:
        print(f"Error in get_verification: {e}")
        import traceback
        traceback.print_exc()
        return ResponseUtils.error(str(e), 500)

@verification_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_verifications():
    try:
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        
        if not current_user:
            return ResponseUtils.error('User not found', 404)
        
        if current_user['role'] not in ['officer', 'admin']:
            return ResponseUtils.error('Access denied', 403)
        
        verifications = VerificationModel.find_pending(mongo.db)
        return ResponseUtils.success(verifications)
    except Exception as e:
        print(f"Error in get_pending_verifications: {e}")
        import traceback
        traceback.print_exc()
        return ResponseUtils.error(str(e), 500)

@verification_bp.route('/<verification_id>/review', methods=['POST'])
@jwt_required()
def review_verification(verification_id):
    try:
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        
        if not current_user:
            return ResponseUtils.error('User not found', 404)
        
        if current_user['role'] not in ['officer', 'admin']:
            return ResponseUtils.error('Access denied', 403)
        
        data = request.get_json()
        
        decision = data.get('decision')
        notes = data.get('notes', '')
        
        if decision not in ['approved', 'rejected']:
            return ResponseUtils.error('Invalid decision', 400)
        
        verification = VerificationModel.find_by_id(verification_id)
        if not verification:
            return ResponseUtils.error('Verification not found', 404)
        
        VerificationModel.update_officer_decision(
            mongo.db,
            verification_id,
            str(current_user['_id']),
            decision,
            notes
        )
        
        DocumentModel.update_status(mongo.db, str(verification['document_id']), decision)
        
        return ResponseUtils.success(message=f'Verification {decision} successfully')
    except Exception as e:
        print(f"Error in review_verification: {e}")
        import traceback
        traceback.print_exc()
        return ResponseUtils.error(str(e), 500)