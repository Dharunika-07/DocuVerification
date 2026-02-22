from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.verification_model import VerificationModel
from models.document_model import DocumentModel
from models.user_model import UserModel
from utils.response_utils import ResponseUtils
from extensions.db import mongo

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/verifications', methods=['GET'])
@jwt_required()
def get_all_verifications():
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(mongo.db, user_id)
    
    if not current_user or current_user['role'] != 'admin':
        return ResponseUtils.error('Access denied', 403)
    
    verifications = VerificationModel.find_all(mongo.db)
    return ResponseUtils.success(verifications)

@admin_bp.route('/documents', methods=['GET'])
@jwt_required()
def get_all_documents():
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(mongo.db, user_id)
    
    if not current_user or current_user['role'] != 'admin':
        return ResponseUtils.error('Access denied', 403)
    
    documents = DocumentModel.find_all(mongo.db)
    return ResponseUtils.success(documents)

@admin_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(mongo.db, user_id)
    
    if not current_user or current_user['role'] != 'admin':
        return ResponseUtils.error('Access denied', 403)
    
    all_verifications = VerificationModel.find_all(mongo.db)
    
    total = len(all_verifications)
    approved = len([v for v in all_verifications if v['status'] == 'approved'])
    rejected = len([v for v in all_verifications if v['status'] == 'rejected'])
    pending = len([v for v in all_verifications if v['status'] == 'pending'])
    
    risk_counts = {'low': 0, 'medium': 0, 'high': 0}
    for v in all_verifications:
        risk_level = v.get('risk_level', 'medium')
        risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
    
    stats = {
        'total_verifications': total,
        'approved': approved,
        'rejected': rejected,
        'pending': pending,
        'risk_distribution': risk_counts
    }
    
    return ResponseUtils.success(stats)