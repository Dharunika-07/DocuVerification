from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.document_model import DocumentModel
from models.user_model import UserModel
from utils.file_utils import FileUtils
from utils.response_utils import ResponseUtils
from extensions.db import mongo

document_bp = Blueprint('document', __name__, url_prefix='/api/documents')

@document_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(user_id)
    
    if not current_user:
        return ResponseUtils.error('User not found', 404)
    
    if 'file' not in request.files:
        return ResponseUtils.error('No file provided', 400)
    
    file = request.files['file']
    document_type = request.form.get('document_type', 'general')
    
    if file.filename == '':
        return ResponseUtils.error('No file selected', 400)
    
    file_path, filename = FileUtils.save_file(file)
    
    if not file_path:
        return ResponseUtils.error('Invalid file type', 400)
    
    from services.ocr_service import OCRService
    extracted_text = OCRService.extract_text(file_path)
    
    document_id = DocumentModel.create_document(
        mongo.db,
        str(current_user['_id']),
        filename,
        file_path,
        document_type,
        extracted_text
    )
    
    return ResponseUtils.success(
        {'document_id': str(document_id)},
        'Document uploaded successfully',
        201
    )

@document_bp.route('/my-documents', methods=['GET'])
@jwt_required()
def get_my_documents():
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(user_id)
    
    if not current_user:
        return ResponseUtils.error('User not found', 404)
    
    documents = DocumentModel.find_by_user(mongo.db, str(current_user['_id']))
    return ResponseUtils.success(documents)

@document_bp.route('/<document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    document = DocumentModel.find_by_id(document_id)
    if not document:
        return ResponseUtils.error('Document not found', 404)
    return ResponseUtils.success(document)