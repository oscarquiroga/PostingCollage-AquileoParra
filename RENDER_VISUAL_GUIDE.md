# GUÍA VISUAL - Configurar Variables en Render

## 🎯 Objetivo
Agregar las credenciales de Cloudinary a tu servicio en Render para que use almacenamiento en la nube.

## 📍 Ubicación: Dashboard de Render

### URL: https://dashboard.render.com

## 🔴 PASO 1: Selecciona tu Servicio

En tu dashboard, verás un listado de servicios. Busca y haz clic en:
```
aquileoparra-periodico-escolar
```

## 🟡 PASO 2: Ve a Environment

Una vez dentro del servicio, en el menú lateral izquierdo:
- Busca: **"Environment"** o **"Settings"** → **"Environment"**
- Si no lo ves, haz clic en el nombre del servicio

Debería verse algo como esto:
```
┌─────────────────────────────────────────┐
│ Settings                                 │
│ ├─ General                              │
│ ├─ Environment        ← AQUÍ            │
│ ├─ Build & Deploy                       │
│ └─ ...                                  │
└─────────────────────────────────────────┘
```

## 🟢 PASO 3: Agregar Variables

Dentro de Environment, verás un botón o sección para agregar variables.

Busca algo como:
- "Add Environment Variable"
- "New Environment Variable"
- O un icono "+"

## 🔵 PASO 4: Agregar PRIMERA Variable

Haz clic en "Add Environment Variable" y rellena:

```
Name:  CLOUDINARY_CLOUD_NAME
Value: doyltixiz

[Save Button]
```

Haz clic en **Save**

## 🟣 PASO 5: Agregar SEGUNDA Variable

Repite el proceso:

```
Name:  CLOUDINARY_API_KEY
Value: 486178594691163

[Save Button]
```

Haz clic en **Save**

## 🟠 PASO 6: Agregar TERCERA Variable

```
Name:  CLOUDINARY_API_SECRET
Value: Pbfm44GzZac-iKVR8Vhw-Ar5egU

[Save Button]
```

Haz clic en **Save**

## 🟤 PASO 7: Agregar CUARTA Variable (IMPORTANTE)

```
Name:  DEBUG
Value: False

[Save Button]
```

Haz clic en **Save**

## ⏳ PASO 8: Esperar Redeploy

Después de guardar la última variable, Render automáticamente:
1. Detecta los cambios
2. Inicia un nuevo Deploy
3. Redeploya tu aplicación (2-3 minutos)

Verás algo como:
```
Status: Building... → Complete → Live
```

## ✅ PASO 9: Verificar

Una vez que dice "Live", ve a tu sitio:
```
https://aquileoparra-periodico-escolar.onrender.com/
```

1. Inicia sesión
2. Crea un nuevo Post
3. Sube una imagen
4. Crea el post

## 📊 VERIFICAR EN CLOUDINARY

1. Ve a https://cloudinary.com/console/resources/images
2. Si la imagen aparece aquí → ✅ ¡Funciona!

## 📝 REFERENCIA RÁPIDA

| Variable | Valor |
|----------|-------|
| `CLOUDINARY_CLOUD_NAME` | `doyltixiz` |
| `CLOUDINARY_API_KEY` | `486178594691163` |
| `CLOUDINARY_API_SECRET` | `Pbfm44GzZac-iKVR8Vhw-Ar5egU` |
| `DEBUG` | `False` |

## 🆘 ¿Qué si algo sale mal?

### Opción 1: Clear Build Cache
1. En Render: Settings → Build & Deploy
2. "Clear Build Cache"
3. Deploy nuevamente

### Opción 2: Revisar Logs
1. En Render Dashboard
2. Abre la sección "Logs"
3. Busca mensajes de error

### Opción 3: Reiniciar Servicio
1. En Render: Settings
2. "Restart"

---

**¡Ya está! El 90% está hecho. Solo falta esto y tu app funcionará perfectamente con Cloudinary. 🚀**
