import logging
import mimetypes
from flask import Flask

def create_app():
    from app.config import (
        TEMPLATE_DIR, STATIC_DIR, SECRET_KEY, LOG_FILE,
        LOG_LEVEL
    )
    
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    
    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
        static_url_path='/static'
    )
    
    app.secret_key = SECRET_KEY
    
    # Inject a dummy csrf_token to prevent Jinja2 UndefinedError in templates
    app.jinja_env.globals['csrf_token'] = lambda: ""
    
    logging.basicConfig(
        filename=LOG_FILE,
        level=LOG_LEVEL,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    
    with app.app_context():
        from app.routes import register_routes
        from app.models import init_db, close_connection
        
        init_db()
        register_routes(app)
        app.teardown_appcontext(close_connection)
    
    return app
