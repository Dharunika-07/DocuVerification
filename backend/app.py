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
    
#     @app.errorhandler(500)
#     def handle_500(e):
#         return {'success': False, 'message': str(e)}, 500
    
#     @app.errorhandler(Exception)
#     def handle_exception(e):
#         print(f"Unhandled exception: {e}")
#         return {'success': False, 'message': 'Internal server error'}, 500
    
#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True, host='0.0.0.0', port=5000)


#After running at 11:00pm
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions.db import init_db
from extensions.jwt import init_jwt
from routes.auth_routes import auth_bp
from routes.document_routes import document_bp
from routes.verification_routes import verification_bp
from routes.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    init_db(app)
    init_jwt(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(verification_bp)
    app.register_blueprint(admin_bp)
    
    @app.errorhandler(404)
    def handle_404(e):
        return {'success': False, 'message': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def handle_500(e):
        return {'success': False, 'message': str(e)}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"Unhandled exception: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'message': 'Internal server error'}, 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'success': True, 'message': 'API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
    app.run(debug=True, host='0.0.0.0', port=5000)