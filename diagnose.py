#!/usr/bin/env python
"""
Script de diagnóstico para verificar la configuración de Cloudinary en Render.
Ejecútar: python diagnose.py
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("DIAGNÓSTICO DE CONFIGURACIÓN - CLOUDINARY")
print("=" * 60)

# 1. Verificar variables de entorno
print("\n1️⃣  VARIABLES DE ENTORNO:")
print("-" * 60)

env_vars = {
    'CLOUDINARY_CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'CLOUDINARY_API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'CLOUDINARY_API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'DEBUG': os.environ.get('DEBUG'),
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'NO CONFIGURADO'),
}

for key, value in env_vars.items():
    if value:
        if 'SECRET' in key or 'KEY' in key:
            display = f"{'*' * len(str(value)[:10])}"
        else:
            display = value
        print(f"✅ {key}: {display}")
    else:
        print(f"❌ {key}: NO CONFIGURADO")

# 2. Verificar configuración de Django
print("\n2️⃣  CONFIGURACIÓN DE DJANGO:")
print("-" * 60)

try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postingcollage.settings')
    django.setup()
    
    from django.conf import settings
    
    print(f"✅ Django version: {django.get_version()}")
    print(f"✅ DEBUG mode: {settings.DEBUG}")
    print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    # Verificar que Cloudinary está configurado
    import cloudinary
    if cloudinary.config().cloud_name:
        print(f"✅ Cloudinary configurado para: {cloudinary.config().cloud_name}")
    else:
        print(f"❌ Cloudinary NO está configurado (falta CLOUDINARY_CLOUD_NAME)")
    
except Exception as e:
    print(f"❌ Error al cargar Django: {e}")

# 3. Verificar que cloudinary está instalado
print("\n3️⃣  PAQUETES INSTALADOS:")
print("-" * 60)

try:
    import cloudinary
    import cloudinary_storage
    print(f"✅ cloudinary: {cloudinary.__version__}")
    print(f"✅ cloudinary_storage: {cloudinary_storage.__version__}")
except ImportError as e:
    print(f"❌ Paquete faltante: {e}")

# 4. Test de conexión a Cloudinary
print("\n4️⃣  TEST DE CONEXIÓN A CLOUDINARY:")
print("-" * 60)

try:
    import cloudinary.api
    result = cloudinary.api.resources(max_results=1)
    print(f"✅ Conexión exitosa a Cloudinary API")
    print(f"   Total recursos: {result.get('total_count', 'desconocido')}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
