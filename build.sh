#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [ -z "$SUPERUSER_PASSWORD" ]; then
    echo "ATENCIÓN: La variable SUPERUSER_PASSWORD no está configurada. Omite la creación del superusuario."
else

    python_script="
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'OscarAdmin'
email = 'oscarquiroga@gmail.com'
password = '$SUPERUSER_PASSWORD'

try:
    # 1. Intentar obtener el usuario. Si ya existe, actualiza la contraseña.
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f'Usuario {username} actualizado con nueva contraseña.')

except User.DoesNotExist:
    # 2. Si el usuario NO existe, créalo.
    User.objects.create_superuser(username, email, password)
    print(f'Usuario {username} creado exitosamente.')

"
    # Ejecutar el script de Python en el shell de Django
    echo "$python_script" | python manage.py shell
fi