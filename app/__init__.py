import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    CORS(app, origins=os.environ.get("FRONTEND_URL", "*"))
    JWTManager(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app
app = create_app()