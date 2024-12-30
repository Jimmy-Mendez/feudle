from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Import and register blueprints/routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Additional initialization can go here (like Flask-Login, Flask-Migrate, etc.)

    return app


