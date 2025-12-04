# Configuración de Cloudinary en Django - PostingCollage

## ✅ Pasos Completados

### 1. **Dependencias Instaladas**
Ya están en `requirements.txt`:
- `cloudinary`
- `django-cloudinary-storage`
- `pillow`
- `django-ckeditor-5`

### 2. **Configuración en settings.py**
- ✅ Importados módulos de Cloudinary
- ✅ Agregado `cloudinary` y `cloudinary_storage` a `INSTALLED_APPS`
- ✅ Configurado `DEFAULT_FILE_STORAGE` a usar Cloudinary
- ✅ Configurado `CKEDITOR_5_FILE_STORAGE` para usar Cloudinary en el editor

### 3. **Variables de Entorno**
Se creó archivo `.env` en la raíz del proyecto. **IMPORTANTE: Actualiza con tus credenciales reales:**

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4. **Modelos Actualizados**
En `ValidatePosts/models.py`:
- ✅ Campo `imgs` usa `CloudinaryField` para imágenes
- ✅ Campo `attachment` usa `CloudinaryField` para archivos
- ✅ Las imágenes se guardan en carpeta `posts/images`
- ✅ Los archivos se guardan en carpeta `posts/files`

### 5. **Formularios Actualizados**
En `ValidatePosts/forms.py`:
- ✅ `PostForm` actualizado para soportar carga de archivos con Cloudinary
- ✅ Agregado campo `video_url` para enlaces de videos
- ✅ Mejorados widgets de formulario

---

## 🚀 Próximos Pasos

### 1. **Obtén tus Credenciales de Cloudinary**
1. Ve a [https://cloudinary.com](https://cloudinary.com)
2. Crea una cuenta gratuita
3. Ve a tu Dashboard
4. Copia:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

### 2. **Actualiza el archivo `.env`**
```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name_aqui
CLOUDINARY_API_KEY=tu_api_key_aqui
CLOUDINARY_API_SECRET=tu_api_secret_aqui
```

### 3. **Verifica la Configuración**
Abre Python shell y prueba:
```bash
python manage.py shell
>>> import cloudinary
>>> cloudinary.api.resources()  # Si funciona, ¡está configurado!
```

### 4. **Prueba la Carga de Archivos**
- Crea un nuevo post en la app
- Intenta subir una imagen
- Verifica que aparezca en tu Dashboard de Cloudinary

---

## 📁 Estructura de Carpetas en Cloudinary

Las imágenes se organizarán automáticamente en:
- **posts/images/** - Imágenes de posts
- **posts/files/** - Archivos adjuntos (PDF, DOC, etc.)

---

## 🔒 Seguridad

**⚠️ IMPORTANTE:**
- **Nunca** compartas tu `.env` file
- **Nunca** hagas commit de `.env` a git
- El `.env` ya está en `.gitignore` (si no, agrégalo)

Asegúrate de que `.gitignore` contenga:
```
.env
*.pyc
__pycache__/
*.sqlite3
media/
```

---

## 🐛 Troubleshooting

### Error: "Cloudinary credentials not found"
- Verifica que `.env` esté en la raíz del proyecto
- Verifica que hayas actualizado las credenciales en `.env`
- Reinicia el servidor Django

### Las imágenes no se suben
- Verifica que `pillow` esté instalado: `pip install pillow`
- Comprueba los permisos en Cloudinary Dashboard

### Error en formulario
- Asegúrate de usar `forms.ImageField()` para imágenes
- Asegúrate de usar `forms.FileField()` para archivos

---

## 📝 Ejemplo de Uso en Template

En tus templates HTML, puedes mostrar las imágenes así:

```html
{% if post.imgs %}
    <img src="{{ post.imgs.url }}" alt="{{ post.title }}" class="img-fluid">
{% endif %}

{% if post.attachment %}
    <a href="{{ post.attachment.url }}" download>Descargar archivo</a>
{% endif %}
```

---

## ✨ Ventajas de Usar Cloudinary

✅ No necesitas servidor dedicado para almacenar imágenes  
✅ Optimización automática de imágenes  
✅ CDN global para cargas rápidas  
✅ Transformaciones de imagen en la nube  
✅ Almacenamiento ilimitado en plan gratuito (con límites)  
✅ Gestión fácil desde Dashboard  

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de Django: `python manage.py runserver`
2. Comprueba el Dashboard de Cloudinary
3. Consulta la documentación oficial: https://cloudinary.com/documentation/django_integration
