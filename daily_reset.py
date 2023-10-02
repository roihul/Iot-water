from datetime import datetime, timedelta
from app import create_app, db

app = create_app()

from app.models import DeviceDataItem, BackgroundTask

with app.app_context():
    now = datetime.utcnow()
    delay = now - timedelta(days=3)
    DeviceDataItem.query.filter(DeviceDataItem.created_at < delay).delete()
    BackgroundTask.query.filter(BackgroundTask.created_at < delay).delete()
    db.session.commit()
    