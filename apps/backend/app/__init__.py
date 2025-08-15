import os
from flask import Flask
from flask_cors import CORS
from .models import db

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app