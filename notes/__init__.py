from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import config

db = SQLAlchemy()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__)

    # Configuration
    app.config.from_object(config.Config)

    # Init SQLAlchemy
    db.init_app(app)

    with app.app_context():
        from . import webapp

        # Register Blueprints
        app.register_blueprint(webapp.webapp_bp)

        # Create DB
        db.create_all()

        # Route the root location
        @app.route('/')
        def root():
            return redirect(url_for('webapp.index'))

        return app
