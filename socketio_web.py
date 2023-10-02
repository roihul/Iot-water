from app import create_app
from app.events import socketio
from app.tasks import celery
from app.utils import login_required

my_app = create_app()
ctx = my_app.app_context()
celery.init_app(my_app)
socketio.init_app(my_app, message_queue=my_app.config['REDIS_URL'])
from app import webhook
my_app.register_blueprint(webhook.blue, url_prefix='/hook')
from app.frontend import tasks
tasks.blue.name = 'client.tasks'
my_app.register_blueprint(tasks.blue, url_prefix='/tasks')


app = my_app