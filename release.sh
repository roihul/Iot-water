rm -rf ./migrations
python manage.py reset-alembic
flask db init
cp ./script.py.mako ./migrations/script.py.mako
flask db migrate
flask db upgrade