# 🚀 Guía de Instalación y Configuración - CursosMarlon

## ✅ Estado del Proyecto

El proyecto Django para vender cursos online ha sido creado exitosamente con las siguientes características:

### 🎯 Funcionalidades Implementadas

- ✅ **Sistema de Usuarios**: Registro, login, perfiles personalizados
- ✅ **Gestión de Cursos**: Categorías, cursos, módulos y lecciones
- ✅ **E-commerce**: Carrito de compras, sistema de pagos con Stripe/PayPal
- ✅ **Panel de Administración**: Interface completa para gestionar contenido
- ✅ **Templates Responsive**: Diseño moderno con Bootstrap 5
- ✅ **API REST**: Endpoints para funcionalidades AJAX
- ✅ **Datos de Ejemplo**: Cursos y categorías precargados

### 🏗️ Arquitectura del Proyecto

```
cursosmarlon/
├── cursosmarlon/           # Configuración principal
│   ├── settings.py        # Configuración Django
│   ├── urls.py           # URLs principales
│   └── celery.py         # Configuración Celery
├── cursos/               # App principal de cursos
│   ├── models.py         # Modelos de cursos, categorías, etc.
│   ├── views.py          # Vistas del frontend
│   ├── admin.py          # Panel de administración
│   └── urls.py           # URLs de cursos
├── users/                # Gestión de usuarios
│   ├── models.py         # Usuario personalizado
│   ├── views.py          # Registro, login, perfil
│   └── urls.py           # URLs de usuarios
├── payments/             # Sistema de pagos
│   ├── models.py         # Carrito, órdenes, pagos
│   ├── views.py          # Procesamiento de pagos
│   └── urls.py           # URLs de pagos
├── templates/            # Templates HTML
├── static/              # Archivos estáticos (CSS, JS)
├── media/               # Archivos subidos por usuarios
├── requirements.txt     # Dependencias Python
└── README.md           # Documentación principal
```

## 🚀 Cómo usar el proyecto

### 1. Servidor de Desarrollo

```bash
# Activar entorno virtual
cd /Users/marlonfalcon/Documents/Projects/cursosmarlon
source .venv/bin/activate

# Iniciar servidor
python manage.py runserver
```

### 2. Acceder a la plataforma

- **Sitio web**: http://127.0.0.1:8000/
- **Panel Admin**: http://127.0.0.1:8000/admin/

### 3. Credenciales creadas

#### Superusuario (Admin)
- Email: `admin@cursosmarlon.com`
- Contraseña: `admin123`

#### Instructor
- Email: `instructor@cursosmarlon.com`
- Contraseña: `instructor123`

## 📋 URLs Principales

### Frontend
- `/` - Página principal
- `/cursos/` - Lista de cursos
- `/curso/<slug>/` - Detalle del curso
- `/users/registro/` - Registro de usuario
- `/users/login/` - Iniciar sesión
- `/users/dashboard/` - Dashboard del usuario
- `/payments/carrito/` - Carrito de compras

### Panel de Administración
- `/admin/` - Panel completo de administración
- Gestión de usuarios, cursos, categorías, pagos, etc.

## 🛠️ Configuración Adicional

### Variables de Entorno (.env)

```env
# Desarrollo
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production

# Base de Datos
DATABASE_URL=sqlite:///db.sqlite3

# Pagos
STRIPE_PUBLIC_KEY=pk_test_tu_clave_publica
STRIPE_SECRET_KEY=sk_test_tu_clave_secreta
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_client_secret

# Email
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

# Redis (para Celery)
REDIS_URL=redis://localhost:6379/0
```

### Configurar Pagos

#### Stripe
1. Crear cuenta en https://stripe.com/
2. Obtener claves de prueba desde el dashboard
3. Añadir claves al archivo `.env`

#### PayPal
1. Crear cuenta en https://developer.paypal.com/
2. Crear una aplicación para obtener credenciales
3. Configurar modo sandbox para pruebas

### Configurar Email

#### Gmail
1. Activar autenticación de 2 factores
2. Generar contraseña de aplicación
3. Usar email y contraseña de aplicación en `.env`

## 📦 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de ejemplo
python manage.py create_sample_data

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test

# Shell de Django
python manage.py shell
```

## 🔄 Tareas Asíncronas (Celery)

Para usar funcionalidades asíncronas como envío de emails:

```bash
# Terminal 1: Redis Server
redis-server

# Terminal 2: Celery Worker
celery -A cursosmarlon worker --loglevel=info

# Terminal 3: Django Server
python manage.py runserver
```

## 🚀 Despliegue en Producción

### Heroku

1. **Preparar para Heroku:**
```bash
# Instalar Heroku CLI
brew install heroku/brew/heroku

# Login en Heroku
heroku login

# Crear app
heroku create tu-app-cursosmarlon
```

2. **Configurar variables:**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=tu-secret-key-produccion
heroku config:set STRIPE_PUBLIC_KEY=pk_live_...
heroku config:set STRIPE_SECRET_KEY=sk_live_...
```

3. **Deploy:**
```bash
git add .
git commit -m "Deploy inicial"
git push heroku main

# Ejecutar migraciones en producción
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Docker

```dockerfile
# Dockerfile incluido en el proyecto
docker build -t cursosmarlon .
docker run -p 8000:8000 cursosmarlon
```

## 📊 Base de Datos

### Modelos Principales

- **User**: Usuario personalizado con campos adicionales
- **Category**: Categorías de cursos
- **Course**: Información completa del curso
- **Module**: Módulos dentro de un curso
- **Lesson**: Lecciones individuales
- **Enrollment**: Inscripciones de estudiantes
- **Payment**: Registro de pagos
- **Cart**: Carrito de compras
- **Order**: Órdenes de compra

### Datos de Ejemplo Incluidos

- 5 categorías (Desarrollo Web, IA, Bases de Datos, DevOps, Programación)
- 5 cursos completos con módulos y lecciones
- Usuario instructor configurado
- Cursos con precios y descuentos

## 🎨 Personalización

### Cambiar Colores
Editar `/static/css/style.css` y modificar las variables CSS:

```css
:root {
    --primary-color: #3b82f6;  /* Cambiar color principal */
    --secondary-color: #64748b;
    /* ... más colores */
}
```

### Añadir Nuevas Funcionalidades
1. Crear nuevas vistas en `views.py`
2. Añadir URLs en `urls.py`
3. Crear templates en `/templates/`
4. Actualizar modelos si es necesario

## 🐛 Problemas Comunes

### Error de Templates
- Verificar que los templates están en `templates/`
- Comprobar configuración de DIRS en settings.py

### Error de Media Files
- Verificar configuración de MEDIA_URL y MEDIA_ROOT
- Crear directorios de media necesarios

### Error de Base de Datos
- Ejecutar `python manage.py migrate`
- Verificar configuración de base de datos

## 📞 Soporte

Si necesitas ayuda o tienes preguntas:

1. Revisar la documentación en `README.md`
2. Verificar logs del servidor
3. Consultar documentación oficial de Django
4. Contactar al desarrollador: info@cursosmarlon.com

## 🎉 ¡Felicitaciones!

Has creado exitosamente una plataforma completa para vender cursos online con Django. El proyecto incluye todas las funcionalidades necesarias para empezar a vender cursos de inmediato.

### Próximos Pasos Recomendados:

1. ✅ Configurar pagos en modo producción
2. ✅ Personalizar diseño y colores
3. ✅ Añadir más contenido de cursos
4. ✅ Configurar dominio personalizado
5. ✅ Implementar certificados de finalización
6. ✅ Añadir sistema de cupones avanzado
7. ✅ Integrar analytics y métricas

¡Tu plataforma está lista para funcionar! 🚀