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

verification_bp = Blueprint(
    "verification",
    __name__,
    url_prefix="/api/verifications"
)


# ============================================================
# VERIFY DOCUMENT
# ============================================================

@verification_bp.route("/verify/<document_id>", methods=["POST"])
@jwt_required()
def verify_document(document_id):
    user_id = get_jwt_identity()

    current_user = UserModel.find_by_id(user_id)
    if not current_user:
        return ResponseUtils.error("User not found", 404)

    document = DocumentModel.find_by_id(document_id)
    if not document:
        return ResponseUtils.error("Document not found", 404)

    if str(document["user_id"]) != str(current_user["_id"]):
        return ResponseUtils.error("Access denied", 403)

    # ============================================================
    # IMAGE FORENSICS
    # ============================================================

    fraud_indicators = []
    forensic_score = 0

    try:
        forensics_result = ImageForensicsService.analyze_image(
            document["file_path"]
        )

        forensic_score = (
            forensics_result.get("metadata_score", 0)
            + forensics_result.get("quality_score", 0)
            + forensics_result.get("manipulation_score", 0)
            + forensics_result.get("face_score", 0)
        )

        for key in [
            "metadata_indicators",
            "quality_indicators",
            "manipulation_indicators",
            "face_indicators",
        ]:
            if forensics_result.get(key):
                fraud_indicators.extend(forensics_result[key])

    except Exception:
        forensic_score = 0
        forensics_result = {"is_suspicious": False}

    # ============================================================
    # AI DETECTION
    # ============================================================

    try:
        ai_detection = AIDetectionService.detect_ai_generated(
            document["file_path"]
        )

        if ai_detection.get("is_likely_ai"):
            fraud_indicators.append(
                "CRITICAL: Document appears AI-generated"
            )
            fraud_indicators.extend(ai_detection.get("ai_indicators", []))
            forensic_score += ai_detection.get("ai_score", 0)

    except Exception:
        ai_detection = {
            "is_likely_ai": False,
            "ai_score": 0,
            "ai_indicators": [],
        }

    # ============================================================
    # DATE & NUMBER VALIDATION
    # ============================================================

    try:
        date_validation = DocumentValidationService.validate_document_dates(
            document["extracted_text"],
            document["document_type"],
        )
    except Exception:
        date_validation = {"is_valid": True, "date_issues": []}

    try:
        number_validation = DocumentValidationService.validate_document_numbers(
            document["extracted_text"],
            document["document_type"],
        )
    except Exception:
        number_validation = {"is_valid": True, "number_issues": []}

    # ============================================================
    # GEMINI VERIFICATION
    # ============================================================

    gemini_service = GeminiService()

    gemini_response = gemini_service.verify_document(
        document["extracted_text"],
        document["document_type"],
    )

    risk_score, risk_level, ai_fraud_indicators = (
        FraudDetectionService.calculate_risk_score(
            document["extracted_text"],
            gemini_response,
        )
    )

    fraud_indicators.extend(ai_fraud_indicators)

    risk_score += min(forensic_score, 60)

    if not date_validation.get("is_valid", True):
        risk_score += 50

    if not number_validation.get("is_valid", True):
        risk_score += 40

    if ai_detection.get("is_likely_ai"):
        risk_score += 30

    risk_score = min(risk_score, 100)

    if risk_score < 30:
        risk_level = "low"
    elif risk_score < 70:
        risk_level = "medium"
    else:
        risk_level = "high"

    auto_decision = FraudDetectionService.auto_decision(
        risk_score, risk_level
    )

    # ============================================================
    # EMBEDDING + DUPLICATE CHECK
    # ============================================================

    embedding = EmbeddingService.generate_embedding(
        document["extracted_text"]
    )

    duplicates = EmbeddingService.find_duplicates(embedding)

    # ============================================================
    # SAVE VERIFICATION
    # ============================================================

    verification_id = VerificationModel.create_verification(
        document_id,
        str(current_user["_id"]),
        risk_score,
        risk_level,
        gemini_response,
        fraud_indicators,
        auto_decision,
        gemini_response,
        embedding,
    )

    DocumentModel.update_status(document_id, auto_decision)

    return ResponseUtils.success(
        {
            "verification_id": str(verification_id),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "auto_decision": auto_decision,
            "fraud_indicators": fraud_indicators,
        },
        "Document verified successfully",
        201,
    )


# ============================================================
# MY VERIFICATIONS
# ============================================================

@verification_bp.route("/my-verifications", methods=["GET"])
@jwt_required()
def get_my_verifications():
    user_id = get_jwt_identity()
    current_user = UserModel.find_by_id(user_id)

    if not current_user:
        return ResponseUtils.error("User not found", 404)

    verifications = VerificationModel.find_by_user(
        str(current_user["_id"])
    )

    return ResponseUtils.success(verifications)