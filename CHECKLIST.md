# ✅ CHECKLIST - Configuración Cloudinary para Render

## LOCAL (Tu computadora)

- [ ] Archivo `.env` actualizado con credenciales de Cloudinary
  ```
  CLOUDINARY_CLOUD_NAME=doyltixiz
  CLOUDINARY_API_KEY=486178594691163
  CLOUDINARY_API_SECRET=Pbfm44GzZac-iKVR8Vhw-Ar5egU
  DEBUG=False
  ```

- [ ] Ejecutar script de verificación:
  ```bash
  python check_cloudinary.py
  ```
  Debe mostrar: ✅ Todas las variables están configuradas correctamente!

- [ ] Probar localmente (opcional):
  ```bash
  python manage.py runserver
  # Ir a http://localhost:8000 y crear un post con imagen
  ```

## RENDER (Producción)

- [ ] **IMPORTANTE**: Ir a https://dashboard.render.com

- [ ] Seleccionar servicio: `aquileoparra-periodico-escolar`

- [ ] Ir a **"Environment"** (o Settings → Environment)

- [ ] Agregar variables de entorno (una por una):
  
  | Nombre | Valor |
  |--------|-------|
  | `CLOUDINARY_CLOUD_NAME` | `doyltixiz` |
  | `CLOUDINARY_API_KEY` | `486178594691163` |
  | `CLOUDINARY_API_SECRET` | `Pbfm44GzZac-iKVR8Vhw-Ar5egU` |
  | `DEBUG` | `False` |
  | `SECRET_KEY` | *(Tu valor actual)* |

- [ ] Hacer clic en **"Save"** después de agregar cada variable

- [ ] Esperar a que Render automáticamente haga el redeploy (2-3 minutos)

- [ ] Verificar en el dashboard que el deploy fue exitoso (estado "Live")

## VERIFICACIÓN FINAL

- [ ] Ir a https://aquileoparra-periodico-escolar.onrender.com/

- [ ] Iniciar sesión con tu cuenta

- [ ] Ir a "Crear Post" (o similar)

- [ ] Subir una imagen y crear el post

- [ ] Ir a https://cloudinary.com/console/resources/images

  - [ ] Verificar que la imagen aparezca en Cloudinary

- [ ] Si todo está bien:
  - ✅ Imagen se subió a Cloudinary
  - ✅ No hay error 500
  - ✅ Proyecto completamente funcionando

## SI ALGO NO FUNCIONA

### 1. Error 500 Persist
```bash
# En tu terminal local:
python diagnose.py

# Te mostrará exactamente qué está mal
```

### 2. Render no reconoce las variables
- En Render Dashboard: Settings → Clear Build Cache
- Luego Deploy nuevamente

### 3. Las imágenes no aparecen en Cloudinary
- Verificar que `DEBUG=False` en Render
- Verificar que `DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"` en settings.py

### 4. Ver logs en Render
- En tu servicio: "Logs"
- Busca mensajes de error de Cloudinary o Django

## VARIABLES DE ENTORNO - REFERENCIA

Tu configuración local (`.env`):
```
SECRET_KEY=your_secret_key_here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/postingcollage
CLOUDINARY_CLOUD_NAME=doyltixiz
CLOUDINARY_API_KEY=486178594691163
CLOUDINARY_API_SECRET=Pbfm44GzZac-iKVR8Vhw-Ar5egU
EMAIL_HOST_USER=xazadox@gmail.com
EMAIL_HOST_PASSWORD=zhvh fave ipcg bweo
RENDER_EXTERNAL_HOSTNAME=https://aquileoparra-periodico-escolar.onrender.com/
```

## PASOS RÁPIDOS (Resumen)

1. ✅ Código ya está actualizado (settings.py, views.py, etc.)
2. ⏳ **NECESARIO**: Agregar variables a Render Environment
3. 🔄 Render automáticamente redeployará
4. ✅ Verificar que funcione

---

**¡Listo! El 90% ya está hecho. Solo falta agregar las variables a Render y ya estaría todo funcionando.**
