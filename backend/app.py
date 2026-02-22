# # from flask import Flask
# # from flask_cors import CORS
# # from config import Config
# # from extensions.db import init_db
# # from extensions.jwt import init_jwt
# # from routes.auth_routes import auth_bp
# # from routes.document_routes import document_bp
# # from routes.verification_routes import verification_bp
# # from routes.admin_routes import admin_bp

# # def create_app():
# #     app = Flask(__name__)
# #     app.config.from_object(Config)
    
# #     CORS(app, resources={
# #         r"/api/*": {
# #             "origins": "*",
# #             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
# #             "allow_headers": ["Content-Type", "Authorization"]
# #         }
# #     })
    
# #     init_db(app)
# #     init_jwt(app)
    
# #     app.register_blueprint(auth_bp)
# #     app.register_blueprint(document_bp)
# #     app.register_blueprint(verification_bp)
# #     app.register_blueprint(admin_bp)
    
# #     @app.errorhandler(500)
# #     def handle_500(e):
# #         return {'success': False, 'message': str(e)}, 500
    
# #     @app.errorhandler(Exception)
# #     def handle_exception(e):
# #         print(f"Unhandled exception: {e}")
# #         return {'success': False, 'message': 'Internal server error'}, 500
    
# #     return app

# # if __name__ == '__main__':
# #     app = create_app()
# #     app.run(debug=True, host='0.0.0.0', port=5000)


# #After running at 11:00pm
# from flask import Flask
# from flask_cors import CORS
# from config import Config
# from extensions.db import init_db
# from extensions.jwt import init_jwt
# from routes.auth_routes import auth_bp
# from routes.document_routes import document_bp
# from routes.verification_routes import verification_bp
# from routes.admin_routes import admin_bp

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
    
#     CORS(app, resources={
#         r"/api/*": {
#             "origins": "*",
#             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#             "allow_headers": ["Content-Type", "Authorization"]
#         }
#     })
    
#     init_db(app)
#     init_jwt(app)
    
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(document_bp)
#     app.register_blueprint(verification_bp)
#     app.register_blueprint(admin_bp)
    
#     @app.errorhandler(404)
#     def handle_404(e):
#         return {'success': False, 'message': 'Endpoint not found'}, 404
    
#     @app.errorhandler(500)
#     def handle_500(e):
#         return {'success': False, 'message': str(e)}, 500
    
#     @app.errorhandler(Exception)
#     def handle_exception(e):
#         print(f"Unhandled exception: {e}")
#         import traceback
#         traceback.print_exc()
#         return {'success': False, 'message': 'Internal server error'}, 500
    
#     @app.route('/api/health', methods=['GET'])
#     def health_check():
#         return {'success': True, 'message': 'API is running'}, 200
    
#     return app

# if __name__ == '__main__':
#     app = create_app()
#     print("Registered routes:")
#     for rule in app.url_map.iter_rules():
#         print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
#     app.run(debug=True, host='0.0.0.0', port=5000)


#for render
from flask import Flask
from flask_cors import CORS
from extensions.db import init_db
from extensions.jwt import init_jwt
from routes.auth_routes import auth_bp
from routes.document_routes import document_bp
from routes.verification_routes import verification_bp
from routes.admin_routes import admin_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # CORS configuration - allow all origins for now, configure specific domains in production
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
    if allowed_origins == '*':
        CORS(app, resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": False
            }
        })
    else:
        CORS(app, resources={
            r"/api/*": {
                "origins": allowed_origins.split(','),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        })
    
    # Initialize extensions
    init_db(app)
    init_jwt(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(verification_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def handle_404(e):
        return {'success': False, 'message': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def handle_500(e):
        return {'success': False, 'message': 'Internal server error'}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"Unhandled exception: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'message': 'Internal server error'}, 500
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {
            'success': True, 
            'message': 'VerifyChain API is running',
            'status': 'healthy',
            'version': '2.0'
        }, 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return {
            'name': 'VerifyChain API',
            'version': '2.0',
            'status': 'running',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'documents': '/api/documents',
                'verifications': '/api/verifications',
                'admin': '/api/admin'
            },
            'documentation': 'https://github.com/your-repo/verifychain'
        }, 200
    
    return app

# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    # Print registered routes for debugging
    print("\n" + "="*60)
    print("🔗 VerifyChain API - Document Verification Platform")
    print("="*60)
    print("\n📋 Registered Routes:")
    print("-" * 60)
    
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            print(f"  {rule.endpoint:30s} {rule.rule:35s} [{methods}]")
    
    print("-" * 60)
    print(f"\n✅ Server Configuration:")
    print(f"   PORT: {os.getenv('PORT', 5000)}")
    print(f"   ENV: {os.getenv('FLASK_ENV', 'development')}")
    print(f"   MONGODB: {'Connected' if os.getenv('MONGODB_URI') else 'Not configured'}")
    print(f"   UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
    print("="*60 + "\n")
    
    # Run with environment-based configuration
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print(f"🚀 Starting server on http://0.0.0.0:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=debug)