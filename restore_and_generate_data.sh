#!/usr/bin/env bash

echo "Restoring database to initial state..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3

echo "Making first migration..."
python manage.py makemigrations
python manage.py migrate --run-syncdb

echo ""
echo "Generating initial data..."
python manage.py shell < createData.py

echo "from airport.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'adminadmin', first_name='Super', last_name='User')" | python manage.py shell
echo "Created superuser, username: admin, password: adminadmin"

echo "Database is ready"