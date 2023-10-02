import os
import click
from flask.cli import with_appcontext
from sqlalchemy.orm.session import Session
from app import create_app, db, bcrypt
from app.models import Permission, Role, User

app = create_app()
session: Session = db.session

def prompt_password():
    password = click.prompt('password', hide_input=True, confirmation_prompt=True)
    while len(password) < 6:
        print('Password must be atleast 6 lengths.')
        password = click.prompt('password', hide_input=True, confirmation_prompt=True)
    return password

@with_appcontext
def init_default_roles_and_permissions():
    default_permissions = [
            Permission(name='permission:create'),
            Permission(name='permission:update'),
            Permission(name='permission:delete'),
            Permission(name='permission:view'),

            Permission(name='role:create'),
            Permission(name='role:update'),
            Permission(name='role:delete'),
            Permission(name='role:view'),

            Permission(name='user:create'),
            Permission(name='user:update'),
            Permission(name='user:delete'),
            Permission(name='user:view'),
            
            Permission(name='device:create'),
            Permission(name='device:update'),
            Permission(name='device:delete'),
            Permission(name='device:view'),
            
            Permission(name='device_data:create'),
            Permission(name='device_data:update'),
            Permission(name='device_data:delete'),
            Permission(name='device_data:view'),
            
            Permission(name='task:create'),
            Permission(name='task:update'),
            Permission(name='task:delete'),
            Permission(name='task:view'),
        ]

    admin = Role.query.filter_by(name='Admin').first()
    permissions = [permission for permission in Permission.query.all()]
    permissions_name = [permission.name for permission in permissions]
    not_in_permissions = [permission for permission in default_permissions if permission.name not in permissions_name]
    
    if not admin:
        admin = Role(name='Admin')
        session.add(admin)
    admin.permissions.extend(not_in_permissions)
        
    staff = Role.query.filter_by(name='Staff').first()
    staff_permissions_name = [
        'device:create',
        'device:update',
        'device:delete',
        'device:view',
        
        'device_data:create',
        'device_data:update',
        'device_data:delete',
        'device_data:view',
        
        'task:create',
        'task:update',
        'task:delete',
        'task:view',
    ]
    staff_permissions = [permission for permission in permissions if permission.name in staff_permissions_name]
    if not staff:
        staff = Role(name='Staff')
        session.add(staff)
    current_staff_permissions = [permission.name for permission in staff.permissions]
    not_in_staff_permissions = [permission for permission in staff_permissions if permission.name not in current_staff_permissions]
    staff.permissions.extend(not_in_staff_permissions)
    print(not_in_staff_permissions)
    session.commit()

@with_appcontext
def register_user(email, password):
    admin = Role.query.filter_by(name='Admin').first()
    if not admin:
        init_default_roles_and_permissions()

    if User.query.filter_by(email=email).first():
        return

    try:
        user = User(email=email, role=admin)
        user.password = password
    except Exception as e:
        print(e)
    session.add(user)
    session.commit()
    
    return user

@with_appcontext
def reset_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    user.password = password
    session.commit()
    
    return user

@app.cli.command('model')
@click.argument('migration_command')
@with_appcontext
def handle_migration(migration_command):
    if migration_command == 'init':
        init_default_roles_and_permissions()
        

@app.cli.command('createuser')
@with_appcontext
def handle_createuser():
    users = User.query.all()

    email = click.prompt('email')
    emails = [user.email for user in users]
    while email in emails:
        print('Email already registered. Try another email')
        email = click.prompt('email')
        
    password = click.prompt('password', hide_input=True, confirmation_prompt=True)
    while len(password) < 6:
        print('Password must be atleast 6 lengths.')
        password = click.prompt('password', hide_input=True, confirmation_prompt=True)
        
    user = register_user(email, password)
    if user:
        print('New user has been created.')


@app.cli.command('reset-password')
@click.argument('email')
@with_appcontext
def handle_reset_password(email):
    users = User.query.all()
    emails = [user.email for user in users]
    
    while email not in emails:
        email = click.prompt('email')
    
    password = prompt_password()
    
    user = reset_password(email, password)
        
    if user:
        print('Success reset password')
        return
    print('User not found')

@app.cli.command('delete-admin')
@with_appcontext
def handle_delete_admin():
    admins = User.query.join(Role).filter(Role.name == 'Admin').all()
    
    for admin in admins:
        print(admin.id, admin.email)
        
    admin_id = click.argument('Choose admin id')
    while admin_id not in [str(admin.id) for admin in admins]:
        print('Wrong admin id')
        admin_id = click.prompt('Choose admin id')
        
    admin = [admin for admin in admins if str(admin.id) == admin_id][0]
    db.session.delete(admin)
    db.session.commit()
    
    print('Admin with id ' + admin_id + ' has been deleted.')

@app.cli.command('install')
@with_appcontext
def install():
    print('Start installing')
    if os.name == 'posix':
        print('Installing for MacOs / Linux')
        os.system('./release.sh')
    elif os.name == 'nt':
        print('Installing for Windows')
        os.system('./release.bat')
    else:
        print('Unknown OS')

    print('Creating Roles and Permissions')
    init_default_roles_and_permissions()
    email = os.getenv('DEFAULT_ADMIN_EMAIL')
    passwd = os.getenv('DEFAULT_ADMIN_PASS')
    
    if not User.query.filter_by(email=email).first():
        user = register_user(email, passwd)
        print(user.email + ' has been created')
        
@app.cli.command('start')
@click.argument('command')
def run(command):
    if command == 'celery':
        os.system('celery -A celery_worker.celery worker -E --loglevel=INFO')
    elif command == 'flask':
        os.system('python run_socket.py')
    elif command == 'flask-gunicorn':
        os.system('gunicorn --bind localhost:5000 --worker-class eventlet -w 1 socketio_web:app --preload')

@app.cli.command('drop-table')
@with_appcontext
def drop_table():
    db.drop_all()
    
@app.cli.command('reset-alembic')
@with_appcontext
def drop_table():
    db.Model.metadata.reflect(db.engine)
    class AlembicVersion(db.Model):
        __table__ = db.Model.metadata.tables['alembic_version']
        
        def __repr__(self) -> str:
            return self.DISTRICT
    AlembicVersion.query.delete()
    db.session.commit()

if __name__ == '__main__':
    app.cli()