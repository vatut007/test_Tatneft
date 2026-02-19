#!/usr/bin/env sh

set -e

python manage.py migrate
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser with username: $DJANGO_SUPERUSER_USERNAME"

python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print("Superuser created successfully")
else:
    print("Superuser already exists")
EOF
else
    echo "Superuser environment variables not set, skipping superuser creation"
fi

exec "$@"