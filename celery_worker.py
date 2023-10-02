from socketio_web import app
from app.tasks import celery

celery.init_app(app)
app.app_context().push()