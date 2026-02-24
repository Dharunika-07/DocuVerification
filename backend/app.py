# from flask import Flask, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from dotenv import load_dotenv
# import os
# import traceback

# from extensions.db import mongo

# # ------------------------------------------------------------
# # Load environment variables
# # ------------------------------------------------------------
# load_dotenv()

# print("=" * 60)
# print("🔗 Starting VerifyChain API")
# print("=" * 60)

# # ------------------------------------------------------------
# # Create Flask App
# # ------------------------------------------------------------
# app = Flask(__name__)

# # ------------------------------------------------------------
# # Configuration
# # ------------------------------------------------------------
# app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# mongodb_uri = os.getenv("MONGODB_URI")

# if not mongodb_uri:
#     print("❌ MONGODB_URI not found in environment variables")
# else:
#     print("✅ MONGODB_URI loaded")
#     app.config["MONGO_URI"] = mongodb_uri


# # ------------------------------------------------------------
# # Enable CORS
# # ------------------------------------------------------------
# CORS(
#     app,
#     resources={
#         r"/*": {
#             "origins": [
#                 "http://localhost:3000",
#                 "http://localhost:5173",
#                 "https://verifychain-frontend.onrender.com",
#             ]
#         }
#     },
# )

# print("✅ CORS enabled")

# # ------------------------------------------------------------
# # Initialize Extensions
# # ------------------------------------------------------------
# jwt = JWTManager(app)
# print("✅ JWT initialized")

# try:
#     mongo.init_app(app)

#     # Test connection
#     if mongodb_uri:
#         mongo.cx.server_info()
#         print("✅ MongoDB connected successfully")
# except Exception as e:
#     print("❌ MongoDB connection error:", e)
#     traceback.print_exc()


# # ------------------------------------------------------------
# # Health Check
# # ------------------------------------------------------------
# @app.route("/api/health")
# def health():
#     try:
#         mongo.cx.server_info()
#         mongo_status = "connected"
#     except Exception:
#         mongo_status = "disconnected"

#     return jsonify(
#         {
#             "success": True,
#             "message": "VerifyChain API is running",
#             "mongodb": mongo_status,
#         }
#     ), 200

# @app.route('/api/test-tesseract', methods=['GET'])
# def test_tesseract():
#     try:
#         import pytesseract
#         version = pytesseract.get_tesseract_version()
#         return jsonify({
#             'success': True,
#             'tesseract_installed': True,
#             'version': str(version)
#         })
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'tesseract_installed': False,
#             'error': str(e)
#         }), 500


# # ------------------------------------------------------------
# # Root Route
# # ------------------------------------------------------------
# @app.route("/")
# def root():
#     return jsonify(
#         {
#             "name": "VerifyChain API",
#             "version": "2.0",
#             "status": "running",
#         }
#     ), 200


# # ------------------------------------------------------------
# # Register Blueprints
# # ------------------------------------------------------------
# try:
#     from routes.auth_routes import auth_bp
#     from routes.document_routes import document_bp
#     from routes.verification_routes import verification_bp
#     from routes.admin_routes import admin_bp

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(document_bp)
#     app.register_blueprint(verification_bp)
#     app.register_blueprint(admin_bp)

#     print("✅ All blueprints registered")

# except Exception as e:
#     print("❌ Blueprint registration error:", e)
#     traceback.print_exc()


# # ------------------------------------------------------------
# # Global Error Handler
# # ------------------------------------------------------------
# @app.errorhandler(Exception)
# def handle_error(e):
#     print("❌ ERROR:", e)
#     traceback.print_exc()
#     return jsonify({"success": False, "message": str(e)}), 500


# print("=" * 60)
# print("✅ App Ready")
# print("=" * 60)


# # ------------------------------------------------------------
# # Run Local (Render uses gunicorn)
# # ------------------------------------------------------------
# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)




"""
VerifyChain API - Production Ready for Render
Includes: CORS fix, MongoDB connection, Tesseract support
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import traceback

print("=" * 60)
print("🔗 Starting VerifyChain API")
print("=" * 60)

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ============================================================
# CORS Configuration - CRITICAL FIX
# ============================================================
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')

if allowed_origins == '*':
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    print("✅ CORS enabled: ALL ORIGINS")
else:
    origins_list = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, resources={
        r"/*": {
            "origins": origins_list,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    print(f"✅ CORS enabled: {origins_list}")

# JWT
jwt = JWTManager(app)
print("✅ JWT initialized")

# ============================================================
# MongoDB Connection
# ============================================================
mongo_client = None
mongo = None

mongodb_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")

if mongodb_uri:
    print(f"📡 Connecting to MongoDB...")
    try:
        mongo_client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=30000)
        mongo_client.server_info()
        db = mongo_client.get_database()
        
        class MongoDB:
            def __init__(self, database):
                self.db = database
        
        mongo = MongoDB(db)
        print(f"✅ MongoDB connected: {db.name}")
        
    except Exception as e:
        print(f"❌ MongoDB failed: {e}")
        mongo = None
else:
    print("❌ MONGODB_URI not set")

# Create uploads
try:
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"✅ Uploads: {uploads_dir}")
except Exception as e:
    print(f"⚠️  Uploads error: {e}")

# Tesseract
try:
    import pytesseract
    tesseract_cmd = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')
    if os.path.exists(tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract: v{version}")
    else:
        print(f"⚠️  Tesseract not found")
except Exception as e:
    print(f"⚠️  Tesseract error: {e}")

# ============================================================
# Routes
# ============================================================
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'VerifyChain API running',
        'version': '2.0',
        'mongodb': 'connected' if mongo else 'disconnected'
    }), 200

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'name': 'VerifyChain API',
        'version': '2.0',
        'status': 'running'
    }), 200

@app.route('/api/test-tesseract', methods=['GET'])
def test_tesseract():
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        return jsonify({
            'success': True,
            'tesseract_installed': True,
            'version': str(version)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
# Add this to your app.py for debugging

@app.route('/api/debug-document/<document_id>', methods=['GET'])
def debug_document(document_id):
    """Debug endpoint to see what's stored for a document"""
    try:
        from bson import ObjectId
        import sys
        
        mongo = sys.modules.get('extensions').mongo
        if not mongo:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get document
        doc = mongo.db.documents.find_one({'_id': ObjectId(document_id)})
        if not doc:
            return jsonify({'error': 'Document not found'}), 404
        
        # Get verification
        verification = mongo.db.verifications.find_one({'document_id': ObjectId(document_id)})
        
        return jsonify({
            'document': {
                'id': str(doc['_id']),
                'filename': doc.get('filename'),
                'document_type': doc.get('document_type'),
                'file_path': doc.get('file_path'),
                'file_exists': os.path.exists(doc.get('file_path', '')) if doc.get('file_path') else False,
                'uploaded_at': str(doc.get('uploaded_at'))
            },
            'verification': {
                'extracted_text_length': len(verification.get('extracted_text', '')) if verification else 0,
                'extracted_text_preview': verification.get('extracted_text', '')[:500] if verification else None,
                'ai_decision': verification.get('ai_decision'),
                'fraud_indicators_count': len(verification.get('fraud_indicators', [])) if verification else 0
            } if verification else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# Register Blueprints
# ============================================================
try:
    print("\n📦 Loading blueprints...")
    
    import sys
    from types import SimpleNamespace
    
    extensions = SimpleNamespace()
    extensions.mongo = mongo
    sys.modules['extensions'] = extensions
    
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    print("  ✅ auth_routes")
    
    from routes.document_routes import document_bp
    app.register_blueprint(document_bp)
    print("  ✅ document_routes")
    
    from routes.verification_routes import verification_bp
    app.register_blueprint(verification_bp)
    print("  ✅ verification_routes")
    
    from routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
    print("  ✅ admin_routes")
    
    print("✅ All blueprints registered\n")
    
except Exception as e:
    print(f"⚠️  Blueprint error: {e}")
    traceback.print_exc()

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'message': 'Server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"❌ Exception: {e}")
    traceback.print_exc()
    return jsonify({'success': False, 'message': str(e)}), 500

# Print routes
print("📋 Registered routes:")
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        print(f"  {rule.rule:45s} [{methods}]")

print("\n" + "=" * 60)
print(f"✅ Ready on port {os.getenv('PORT', 5000)}")
print("=" * 60 + "\n")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)