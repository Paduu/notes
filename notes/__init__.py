from flask import Flask, redirect, url_for
from .config import Config
from .database import init_db, db_session

def create_app():
    """Construct the core app object."""
    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)

    with app.app_context():
        from . import webapp

        # Register Blueprints
        app.register_blueprint(webapp.webapp_bp)

        init_db()

        # Route the root location
        @app.route('/')
        def root():
            return redirect(url_for('webapp.index'))

        # close db sessions
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

        return app
