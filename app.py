
import os
from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db
from flask_mail import Mail



mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy database instance
   

    db.init_app(app)
    mail.init_app(app)
    from models.user import User

    @app.context_processor
    def inject_user():
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            return {"user": user}
        return {"user": None}

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.chatbot import chatbot_bp
    from routes.aptitude import aptitude_bp
    from routes.technical import technical_bp
    from routes.hr import hr_bp
    from routes.companies import companies_bp
    from routes.coding import coding_bp
    from routes.resume import resume_bp
    from routes.mock_interview import mock_bp
    from routes.progress import progress_bp
    from routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(aptitude_bp)
    app.register_blueprint(technical_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(mock_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(profile_bp)

    # Root route for landing page
    @app.route('/')
    def landing():
        if 'user_id' in session:
            return redirect(url_for('dashboard.index'))
        return render_template('landing.html')

    # Global Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Ensure tables are created for local development SQLite fallback
    with app.app_context():
        db.create_all()

    # Seed database only if empty
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
