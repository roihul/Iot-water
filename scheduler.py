from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from app import create_app, db
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = create_app()
scheduler = BlockingScheduler()

from app.models import DeviceDataItem, BackgroundTask

logger.info('Running')
@scheduler.scheduled_job('cron', id='task', minute=0, hour=0)
def _():
    with app.app_context():
        logger.info('Scheduled Reset Data')
        now = datetime.utcnow()
        a_minute_ago = now - timedelta(days=3)
        DeviceDataItem.query.filter(DeviceDataItem.created_at < a_minute_ago).delete()
        BackgroundTask.query.filter(BackgroundTask.created_at < a_minute_ago).delete()
        db.session.commit()
    
scheduler.start()
