# # # ============================================================
# # # VerifyChain API - Production Ready Version
# # # ============================================================

# # from flask import Flask, jsonify
# # from flask_cors import CORS
# # from flask_jwt_extended import JWTManager
# # from pymongo import MongoClient
# # from dotenv import load_dotenv
# # import os
# # import traceback

# # print("=" * 60)
# # print("🔗 Starting VerifyChain API")
# # print("=" * 60)

# # # ------------------------------------------------------------
# # # Load environment variables (.env for local)
# # # ------------------------------------------------------------
# # load_dotenv()

# # # ------------------------------------------------------------
# # # Create Flask App
# # # ------------------------------------------------------------
# # app = Flask(__name__)

# # # ------------------------------------------------------------
# # # Basic Configuration
# # # ------------------------------------------------------------
# # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
# # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# # # ------------------------------------------------------------
# # # Enable CORS
# # # ------------------------------------------------------------
# # CORS(app, resources={
# #     r"/*": {
# #         "origins": [
# #             "http://localhost:3000",
# #             "http://localhost:5173",
# #             "https://verifychain-frontend.onrender.com"
# #         ]
# #     }
# # })
# # print("✅ CORS enabled")

# # # ------------------------------------------------------------
# # # Initialize JWT
# # # ------------------------------------------------------------
# # jwt = JWTManager(app)
# # print("✅ JWT initialized")

# # # ------------------------------------------------------------
# # # MongoDB Connection
# # # ------------------------------------------------------------
# # mongo_client = None
# # db = None

# # # Try both MONGODB_URI and MONGO_URI (for compatibility)
# # print("DEBUG ENV VAR:", os.environ.get("MONGODB_URI"))
# # mongodb_uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")
# # print(f"MONGODB_URI from env: {mongodb_uri is not None}")

# # if mongodb_uri:
# #     print(f"Attempting to connect to MongoDB...")
# #     print(f"Connection string: {mongodb_uri[:30]}...{mongodb_uri[-20:]}")  # Show partial string for debugging
# #     try:
# #         # Increase timeout to 30 seconds
# #         mongo_client = MongoClient(
# #             mongodb_uri, 
# #             serverSelectionTimeoutMS=30000,
# #             connectTimeoutMS=30000,
# #             socketTimeoutMS=30000
# #         )
# #         # Force connection attempt
# #         mongo_client.server_info()
# #         db = mongo_client.get_database()
# #         print(f"✅ MongoDB connected successfully to database: {db.name}")
# #     except Exception as e:
# #         print(f"❌ MongoDB connection error: {e}")
# #         print(f"Full error: {traceback.format_exc()}")
# # else:
# #     print("❌ MONGODB_URI is not set in environment variables")

# # # ------------------------------------------------------------
# # # Create uploads directory
# # # ------------------------------------------------------------
# # try:
# #     uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
# #     os.makedirs(uploads_dir, exist_ok=True)
# #     print(f"✅ Uploads directory: {uploads_dir}")
# # except Exception as e:
# #     print(f"⚠️  Could not create uploads directory: {e}")

# # # ------------------------------------------------------------
# # # Health Check
# # # ------------------------------------------------------------
# # @app.route('/api/health', methods=['GET'])
# # def health_check():
# #     return jsonify({
# #         'success': True,
# #         'status': 'healthy',
# #         'message': 'VerifyChain API is running',
# #         'version': '2.0',
# #         'mongodb': 'connected' if db is not None else 'disconnected'
# #     }), 200

# # # ------------------------------------------------------------
# # # Root Route
# # # ------------------------------------------------------------
# # @app.route('/', methods=['GET'])
# # def root():
# #     return jsonify({
# #         'name': 'VerifyChain API',
# #         'version': '2.0',
# #         'status': 'running'
# #     }), 200

# # # ------------------------------------------------------------
# # # Register Blueprints
# # # ------------------------------------------------------------
# # try:
# #     print("\n📦 Loading blueprints...")

# #     from routes.auth_routes import auth_bp
# #     app.register_blueprint(auth_bp)
# #     print("  ✅ auth_routes")

# #     from routes.document_routes import document_bp
# #     app.register_blueprint(document_bp)
# #     print("  ✅ document_routes")

# #     from routes.verification_routes import verification_bp
# #     app.register_blueprint(verification_bp)
# #     print("  ✅ verification_routes")

# #     from routes.admin_routes import admin_bp
# #     app.register_blueprint(admin_bp)
# #     print("  ✅ admin_routes")

# #     print("✅ All blueprints registered\n")

# # except Exception as e:
# #     print(f"⚠️  Blueprint registration error: {e}")
# #     traceback.print_exc()

# # # ------------------------------------------------------------
# # # Error Handlers
# # # ------------------------------------------------------------
# # @app.errorhandler(404)
# # def not_found(e):
# #     return jsonify({'success': False, 'message': 'Endpoint not found'}), 404


# # @app.errorhandler(500)
# # def internal_error(e):
# #     return jsonify({'success': False, 'message': 'Internal server error'}), 500


# # @app.errorhandler(Exception)
# # def handle_exception(e):
# #     print(f"❌ Unhandled exception: {e}")
# #     traceback.print_exc()
# #     return jsonify({'success': False, 'message': str(e)}), 500


# # # ------------------------------------------------------------
# # # Print Registered Routes
# # # ------------------------------------------------------------
# # print("📋 Registered routes:")
# # for rule in app.url_map.iter_rules():
# #     if rule.endpoint != 'static':
# #         methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
# #         print(f"  {rule.rule:40s} [{methods}]")

# # print("\n" + "=" * 60)
# # print(f"✅ App ready on port {os.getenv('PORT', 5000)}")
# # print("=" * 60 + "\n")


# # # ------------------------------------------------------------
# # # Run App
# # # ------------------------------------------------------------
# # if __name__ == '__main__':
# #     port = int(os.getenv('PORT', 5000))
# #     app.run(host='0.0.0.0', port=port, debug=False)



# # ============================================================
# # VerifyChain API - Production Ready Version
# # ============================================================

# from flask import Flask, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from dotenv import load_dotenv
# import os
# import traceback

# # Load environment variables
# load_dotenv()

# print("=" * 60)
# print("🔗 Starting VerifyChain API")
# print("=" * 60)

# # ------------------------------------------------------------
# # Create Flask App
# # ------------------------------------------------------------
# app = Flask(__name__)

# # ------------------------------------------------------------
# # Basic Configuration
# # ------------------------------------------------------------
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# # MongoDB URI from environment
# mongodb_uri = os.getenv("MONGODB_URI")

# if not mongodb_uri:
#     print("❌ MONGODB_URI is not set in environment variables")
# else:
#     app.config["MONGODB_URI"] = mongodb_uri
#     print("✅ MONGODB_URI loaded from environment")

# # ------------------------------------------------------------
# # Enable CORS
# # ------------------------------------------------------------
# CORS(app, resources={
#     r"/*": {
#         "origins": [
#             "http://localhost:3000",
#             "http://localhost:5173",
#             "https://verifychain-frontend.onrender.com"
#         ]
#     }
# })
# print("✅ CORS enabled")

# # ------------------------------------------------------------
# # Initialize JWT
# # ------------------------------------------------------------
# jwt = JWTManager(app)
# print("✅ JWT initialized")

# # ------------------------------------------------------------
# # Initialize MongoDB (Flask-PyMongo)
# # ------------------------------------------------------------
# try:
#     from extensions.db import init_db, mongo
#     init_db(app)

#     # Test connection
#     mongo.cx.server_info()
#     print("✅ MongoDB connected successfully")

# except Exception as e:
#     print(f"❌ MongoDB connection error: {e}")
#     print(traceback.format_exc())

# # ------------------------------------------------------------
# # Create uploads directory
# # ------------------------------------------------------------
# try:
#     uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
#     os.makedirs(uploads_dir, exist_ok=True)
#     print(f"✅ Uploads directory: {uploads_dir}")
# except Exception as e:
#     print(f"⚠️ Could not create uploads directory: {e}")

# # ------------------------------------------------------------
# # Health Check
# # ------------------------------------------------------------
# @app.route('/api/health', methods=['GET'])
# def health_check():
#     from extensions.db import mongo
#     return jsonify({
#         'success': True,
#         'status': 'healthy',
#         'message': 'VerifyChain API is running',
#         'version': '2.0',
#         'mongodb': 'connected' if mongo.db is not None else 'disconnected'
#     }), 200


# # ------------------------------------------------------------
# # Root Route
# # ------------------------------------------------------------
# @app.route('/', methods=['GET'])
# def root():
#     return jsonify({
#         'name': 'VerifyChain API',
#         'version': '2.0',
#         'status': 'running'
#     }), 200


# # ------------------------------------------------------------
# # Register Blueprints
# # ------------------------------------------------------------
# try:
#     print("\n📦 Loading blueprints...")

#     from routes.auth_routes import auth_bp
#     app.register_blueprint(auth_bp)
#     print("  ✅ auth_routes")

#     from routes.document_routes import document_bp
#     app.register_blueprint(document_bp)
#     print("  ✅ document_routes")

#     from routes.verification_routes import verification_bp
#     app.register_blueprint(verification_bp)
#     print("  ✅ verification_routes")

#     from routes.admin_routes import admin_bp
#     app.register_blueprint(admin_bp)
#     print("  ✅ admin_routes")

#     print("✅ All blueprints registered\n")

# except Exception as e:
#     print(f"⚠️ Blueprint registration error: {e}")
#     traceback.print_exc()


# # ------------------------------------------------------------
# # Error Handlers
# # ------------------------------------------------------------
# @app.errorhandler(404)
# def not_found(e):
#     return jsonify({'success': False, 'message': 'Endpoint not found'}), 404


# @app.errorhandler(500)
# def internal_error(e):
#     return jsonify({'success': False, 'message': 'Internal server error'}), 500


# @app.errorhandler(Exception)
# def handle_exception(e):
#     print(f"❌ Unhandled exception: {e}")
#     traceback.print_exc()
#     return jsonify({'success': False, 'message': str(e)}), 500


# # ------------------------------------------------------------
# # Print Registered Routes
# # ------------------------------------------------------------
# print("📋 Registered routes:")
# for rule in app.url_map.iter_rules():
#     if rule.endpoint != 'static':
#         methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
#         print(f"  {rule.rule:40s} [{methods}]")

# print("\n" + "=" * 60)
# print(f"✅ App ready on port {os.getenv('PORT', 5000)}")
# print("=" * 60 + "\n")


# # ------------------------------------------------------------
# # Run App (Local Development)
# # ------------------------------------------------------------
# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)




# ============================================================
# VerifyChain API - Clean Production Version
# ============================================================

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import traceback

from extensions.db import mongo

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()

print("=" * 60)
print("🔗 Starting VerifyChain API")
print("=" * 60)

# ------------------------------------------------------------
# Create Flask App
# ------------------------------------------------------------
app = Flask(__name__)

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    print("❌ MONGODB_URI not found in environment variables")
else:
    print("✅ MONGODB_URI loaded")
    app.config["MONGO_URI"] = mongodb_uri


# ------------------------------------------------------------
# Enable CORS
# ------------------------------------------------------------
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "http://localhost:5173",
                "https://verifychain-frontend.onrender.com",
            ]
        }
    },
)

print("✅ CORS enabled")

# ------------------------------------------------------------
# Initialize Extensions
# ------------------------------------------------------------
jwt = JWTManager(app)
print("✅ JWT initialized")

try:
    mongo.init_app(app)

    # Test connection
    if mongodb_uri:
        mongo.cx.server_info()
        print("✅ MongoDB connected successfully")
except Exception as e:
    print("❌ MongoDB connection error:", e)
    traceback.print_exc()


# ------------------------------------------------------------
# Health Check
# ------------------------------------------------------------
@app.route("/api/health")
def health():
    try:
        mongo.cx.server_info()
        mongo_status = "connected"
    except Exception:
        mongo_status = "disconnected"

    return jsonify(
        {
            "success": True,
            "message": "VerifyChain API is running",
            "mongodb": mongo_status,
        }
    ), 200


# ------------------------------------------------------------
# Root Route
# ------------------------------------------------------------
@app.route("/")
def root():
    return jsonify(
        {
            "name": "VerifyChain API",
            "version": "2.0",
            "status": "running",
        }
    ), 200


# ------------------------------------------------------------
# Register Blueprints
# ------------------------------------------------------------
try:
    from routes.auth_routes import auth_bp
    from routes.document_routes import document_bp
    from routes.verification_routes import verification_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(verification_bp)
    app.register_blueprint(admin_bp)

    print("✅ All blueprints registered")

except Exception as e:
    print("❌ Blueprint registration error:", e)
    traceback.print_exc()


# ------------------------------------------------------------
# Global Error Handler
# ------------------------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
    print("❌ ERROR:", e)
    traceback.print_exc()
    return jsonify({"success": False, "message": str(e)}), 500


print("=" * 60)
print("✅ App Ready")
print("=" * 60)


# ------------------------------------------------------------
# Run Local (Render uses gunicorn)
# ------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)