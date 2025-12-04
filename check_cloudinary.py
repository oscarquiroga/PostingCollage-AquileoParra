#!/usr/bin/env python
"""
Script rápido para verificar que Cloudinary esté correctamente configurado.
Uso: python check_cloudinary.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("\n" + "="*70)
print("✓ VERIFICADOR DE CLOUDINARY CONFIGURACIÓN")
print("="*70 + "\n")

# Verificar variables de entorno
required_vars = [
    'CLOUDINARY_CLOUD_NAME',
    'CLOUDINARY_API_KEY',
    'CLOUDINARY_API_SECRET'
]

missing = []
found = []

for var in required_vars:
    value = os.environ.get(var)
    if value:
        # Mostrar de forma segura
        if 'SECRET' in var or 'KEY' in var:
            display = f"{value[:5]}...{value[-5:]}"
        else:
            display = value
        print(f"  ✅ {var}: {display}")
        found.append(var)
    else:
        print(f"  ❌ {var}: NO ENCONTRADO")
        missing.append(var)

if missing:
    print(f"\n⚠️  FALTA CONFIGURAR: {', '.join(missing)}")
    print("\n📝 Actualiza tu archivo .env con las credenciales de Cloudinary")
    sys.exit(1)
else:
    print("\n✅ TODAS las variables están configuradas correctamente!")

# Intentar importar y configurar
try:
    import cloudinary
    import cloudinary.api
    from django.conf import settings
    
    print("\n" + "-"*70)
    print("Probando conexión con Cloudinary API...")
    print("-"*70)
    
    # Esto verificará si la conexión funciona
    cloudinary.config(
        cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
        api_key=os.environ.get("CLOUDINARY_API_KEY"),
        api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    )
    
    # Intentar usar la API
    result = cloudinary.api.resources(max_results=1)
    print(f"  ✅ Conexión exitosa!")
    print(f"  📊 Total de recursos en Cloudinary: {result.get('total_count', '?')}")
    
except Exception as e:
    print(f"  ❌ Error de conexión: {e}")
    print("\n💡 Posibles problemas:")
    print("   - API Key o API Secret incorrectos")
    print("   - Cloud Name incorrecto")
    print("   - Sin conexión a internet")

print("\n" + "="*70)
print("✓ VERIFICACIÓN COMPLETADA")
print("="*70 + "\n")
