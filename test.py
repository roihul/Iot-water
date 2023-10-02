from app import create_app
from app.models import Device, User

ctx = create_app().app_context()
ctx.push()
device: Device = Device.query.first()
user: User = device.shared_users[0]
print(user.avg_water_level)

ctx.pop()