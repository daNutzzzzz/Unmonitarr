from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config/config.py')
    
    db.init_app(app)
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    from .tasks import setup_scheduled_tasks
    with app.app_context():
        db.create_all()
        setup_scheduled_tasks(app)
    
    scheduler.start()
    
    return app