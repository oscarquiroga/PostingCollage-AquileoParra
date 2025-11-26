#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [ -z "$SUPERUSER_PASSWORD" ]; then
    echo "ATENCIÓN: La variable SUPERUSER_PASSWORD no está configurada. Omite la creación del superusuario."
else

    python manage.py createsuperuser --noinput \
        --username oscaradmin \
        --email oscarquiroga@gmail.com
    

    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.get(username='OscarAdmin').set_password('$SUPERUSER_PASSWORD'); User.objects.get(username='OscarAdmin').save()" | python manage.py shell
fi