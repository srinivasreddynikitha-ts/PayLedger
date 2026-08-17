from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    # Import models so SQLAlchemy registers them
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
         return db.session.get(User, int(user_id))
    
    from app.auth import auth
    app.register_blueprint(auth)

    from app.main import main
    app.register_blueprint(main) 

    from app.admin.routes import admin
    app.register_blueprint(admin)

    @app.route("/")
    def home():
        return "<h1>Welcome to PayLedger</h1>"

    @app.route("/test-db")
    def test_db():
        try:
            db.session.execute(db.text("SELECT 1"))
            return "<h1>Database connection successful!</h1>"
        except Exception as e:
            return f"<h1>Database connection failed</h1><p>{e}</p>"

    return app