# Guía de Deploy en Render con Cloudinary

## Problema Identificado ✅

Tu aplicación está usando `FileSystemStorage` en lugar de `MediaCloudinaryStorage` porque las variables de entorno de Cloudinary no se están leyendo correctamente en Render.

## Solución - Pasos a Seguir:

### 1. Verifica tu archivo `.env` local
El archivo `.env` debe tener estas variables (YA CONFIGURADAS):
```env
CLOUDINARY_CLOUD_NAME=doyltixiz
CLOUDINARY_API_KEY=486178594691163
CLOUDINARY_API_SECRET=Pbfm44GzZac-iKVR8Vhw-Ar5egU
DEBUG=False
```

### 2. Configurar Variables en Render Dashboard

**IMPORTANTE**: En Render, las variables `.env` locales NO se sincronizan automáticamente.

1. Ve a tu servicio en [https://dashboard.render.com](https://dashboard.render.com)
2. Haz clic en tu aplicación "aquileoparra-periodico-escolar"
3. Ve a la sección **"Environment"** (Entorno)
4. Haz clic en **"Add Environment Variable"** para cada una:

**Variable 1:**
```
Name:  CLOUDINARY_CLOUD_NAME
Value: doyltixiz
```

**Variable 2:**
```
Name:  CLOUDINARY_API_KEY
Value: 486178594691163
```

**Variable 3:**
```
Name:  CLOUDINARY_API_SECRET
Value: Pbfm44GzZac-iKVR8Vhw-Ar5egU
```

**Variable 4 (si no existe):**
```
Name:  DEBUG
Value: False
```

**Variable 5 (si no existe):**
```
Name:  SECRET_KEY
Value: [Tu SECRET_KEY actual]
```

### 3. Después de Agregar Variables

1. Haz clic en **"Save"**
2. Render automáticamente redeployará tu aplicación
3. Espera a que termine el deploy (2-3 minutos)

### 4. Verificar que Funciona

Una vez redeployado:
1. Ve a tu sitio: https://aquileoparra-periodico-escolar.onrender.com/
2. Intenta crear un nuevo post con imagen
3. Verifica en tu Dashboard de Cloudinary que aparezca el archivo

## Cómo Verificar el Problema

Si aún ves el error `FileSystemStorage`, ejecuta el script de diagnóstico:

```bash
python diagnose.py
```

Este te mostrará:
- ✅ Qué variables están configuradas
- ✅ Si Cloudinary está conectado
- ❌ Qué está faltando

## Cambios Realizados en el Código

✅ `settings.py`: Ahora carga correctamente `.env` con `python-dotenv`  
✅ `settings.py`: Cloudinary se configura con las credenciales de entorno  
✅ `Publicates/views.py`: Removidos prints de debug que causaban errores  
✅ Almacenamiento configurado a `MediaCloudinaryStorage`

## Si Sigue Sin Funcionar

1. **Borra el caché de Render**: 
   - En el Dashboard, ve a "Settings"
   - Haz clic en "Clear Build Cache"
   - Redeploy

2. **Comprueba los logs**:
   - En Render Dashboard, abre los "Logs"
   - Busca errores de Cloudinary

3. **Reinicia el servicio**:
   - En Render, ve a "Settings" → "Restart"

## Referencia Rápida - Variables Render

| Variable | Valor |
|----------|-------|
| CLOUDINARY_CLOUD_NAME | doyltixiz |
| CLOUDINARY_API_KEY | 486178594691163 |
| CLOUDINARY_API_SECRET | Pbfm44GzZac-iKVR8Vhw-Ar5egU |
| DEBUG | False |
| DATABASE_URL | [Tu DB PostgreSQL URL] |
| SECRET_KEY | [Tu SECRET_KEY] |
