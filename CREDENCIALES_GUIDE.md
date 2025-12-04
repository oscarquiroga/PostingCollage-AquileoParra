# 🔑 Guía: Qué Credenciales Usar - API Key de Cloudinary

## 📊 Tus API Keys Disponibles

| Nombre | Fecha | API Key | Recomendación |
|--------|-------|---------|----------------|
| **db-posts** | Dec 03, 2025 | 466475685649443 | ✅ **USAR ESTA** |
| Root | Dec 02, 2025 | 486178594691163 | ⚠️ Regenerar después |

---

## ✅ RESPUESTA: Usa `db-posts` (No Root)

### Por qué `db-posts` es mejor:

1. **Más nueva** - Creada específicamente para esta app
2. **Más segura** - Tiene permisos limitados
3. **Mejor práctica** - No usar Root en producción

### Por qué NO usar Root:

1. **Permisos amplios** - Root tiene acceso a todo
2. **Posible exposición** - El valor anterior (486178594691163) ya fue compartido
3. **Mala práctica** - Usar Root en producción es peligroso

### Acción para Root (IMPORTANTE):

Si el API Key de Root está expuesto (en GitHub, etc.):
1. Ve a Cloudinary Dashboard
2. Haz clic en el ícono **⋮** (tres puntos) al lado de "Root"
3. Selecciona **"Regenerate"**
4. Confirma

Esto invalidará el viejo API Key y generará uno nuevo.

---

## 📌 ¿Qué es CLOUDINARY_URL?

Es una **URL única** que contiene todas tus credenciales:

```
cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

**Ejemplo:**
```
cloudinary://466475685649443:TU_API_SECRET_AQUI@doyltixiz
```

### Ventajas:
- ✅ Una sola variable en lugar de 3
- ✅ Más fácil de manejar
- ✅ Estándar de la industria

---

## ⚙️ CÓMO CONFIGURAR EN RENDER

### Opción A: Usar CLOUDINARY_URL (RECOMENDADO)

1. Ve a https://dashboard.render.com
2. Selecciona tu app: `aquileoparra-periodico-escolar`
3. Ve a **Environment**
4. Agrega **UNA SOLA variable**:

```
Name:  CLOUDINARY_URL
Value: cloudinary://466475685649443:TU_API_SECRET@doyltixiz
```

**¿Dónde obtener el API_SECRET?**
- Ve a tu Cloudinary Dashboard
- En la tabla, haz clic en la fila "db-posts"
- O haz clic en el ícono 👁️ (ojo) para ver el secreto completo

5. Haz clic en **Save**
6. Render automáticamente redeployará

---

### Opción B: Usar 3 Variables Separadas (alternativa)

Si prefieres no usar CLOUDINARY_URL:

```
Name:  CLOUDINARY_CLOUD_NAME
Value: doyltixiz

Name:  CLOUDINARY_API_KEY
Value: 466475685649443

Name:  CLOUDINARY_API_SECRET
Value: [Tu API Secret aquí]
```

---

## 🔍 PASO A PASO: Obtener tu API Secret

1. **Abre tu Cloudinary Dashboard**: https://cloudinary.com/console
2. **Mira la tabla de API Keys**
3. **Para "db-posts"**:
   - Busca la columna **"API Secret"** (muestra asteriscos)
   - Haz clic en el ícono **👁️** (ojo) para revelar
   - O haz clic en los **asteriscos** directamente
4. **Copia el valor completo**
5. **Úsalo en CLOUDINARY_URL o como CLOUDINARY_API_SECRET**

---

## ✨ Resumen Rápido

| Item | Valor |
|------|-------|
| Cloud Name | `doyltixiz` |
| API Key a usar | `466475685649443` (db-posts) |
| API Secret | **Obtener de Cloudinary Dashboard** |
| Formato CLOUDINARY_URL | `cloudinary://466475685649443:SECRET@doyltixiz` |

---

## 🚀 Próximos Pasos

1. ✅ Decidir: ¿CLOUDINARY_URL o 3 variables?
2. 📋 Obtener el API Secret de "db-posts"
3. 🔧 Agregar variable(s) a Render Environment
4. ⏳ Esperar redeploy (2-3 minutos)
5. ✔️ Verificar que funcione en tu sitio

---

## ⚠️ SEGURIDAD

**IMPORTANTE:**
- **Nunca** compartas tu API Secret públicamente
- **Nunca** hagas commit del `.env` a Git
- El archivo `.env` debe estar en `.gitignore`
- Si alguien ve tu Secret, regenera la API Key

---

## 🔐 Si el Secret de Root fue Expuesto

**HAZLO AHORA:**
1. Cloudinary Dashboard
2. Busca "Root" en la tabla
3. Haz clic en **⋮** → **Regenerate**
4. Confirma que sí

Esto invalidará el viejo secret y generará uno nuevo.
