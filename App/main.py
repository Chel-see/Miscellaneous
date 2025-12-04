import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from App.database import init_db
from App.config import load_config

from flask import jsonify

from App.controllers import (
    setup_jwt,
    add_auth_context
)
### NOTE to TECHTONIC MEMBERS: Uncomment this before submission ###
#from App.views import views #setup_admin


### NOTE to TECHTONIC MEMBERS: Uncomment this before submission ###
def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    
    # Load config
    load_config(app, overrides)
    
    # CORS
    CORS(app)
    
    # Auth / JWT
    add_auth_context(app)
    
    # Uploads
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    
    # **REGISTER ALL BLUEPRINTS**
    from App.views import views
    for view in views:
        app.register_blueprint(view)
    
    # Database
    init_db(app)
    
    # JWT setup
    jwt = setup_jwt(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return jsonify({"error": error}), 401  # Use JSON for API
    
    return app