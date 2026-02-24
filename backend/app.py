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
            'tesseract_installed': False,
            'error': str(e)
        }), 500


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