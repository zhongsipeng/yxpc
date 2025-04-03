import os
from flask import Flask
from app.config.config import config
from app.extensions import db 
from flasgger import Swagger
from app.config import default_config


def create_app():
    app = Flask(__name__, instance_path=str(config.INSTANCE_PATH))
    app.config.from_object(default_config)
    app.config.from_pyfile(os.path.join(app.instance_path, 'application.cfg'), silent=True)
    app.json.ensure_ascii = False
    
    db.init_app(app)
    Swagger(app)
    
    from app.errors.handlers import register_handlers
    register_handlers(app)  # 集中注册所有处理器
    
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app
