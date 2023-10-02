rmdir /s /q .\migrations
python manage.py reset-alembic
flask db init
copy .\script.py.mako .\migrations\script.py.mako
flask db migrate
flask db upgrade