# 🎓 CursosMarlon - Plataforma de Cursos Online

Una plataforma completa para vender y gestionar cursos online desarrollada con Django.

## 📋 Características

- **Gestión de Cursos**: Creación, edición y organización de cursos con módulos y lecciones
- **Sistema de Usuarios**: Registro, autenticación y perfiles de estudiantes e instructores
- **Carrito de Compras**: Sistema completo de e-commerce para cursos
- **Pagos Integrados**: Soporte para Stripe y PayPal
- **Reproductor de Video**: Sistema para visualizar lecciones en video
- **Sistema de Reseñas**: Calificaciones y comentarios de estudiantes
- **Panel de Administración**: Interface completa para gestionar la plataforma
- **Responsive**: Diseño adaptable a dispositivos móviles

## 🚀 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/falconsoft3d/cursosmarlon.git
cd cursosmarlon
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones:**
```bash
python manage.py migrate
```

6. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

7. **Ejecutar el servidor:**
```bash
python manage.py runserver
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=sqlite:///db.sqlite3

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# PayPal
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_client_secret
PAYPAL_MODE=sandbox

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password

# Redis (para Celery)
REDIS_URL=redis://localhost:6379/0
```

## 📱 Estructura del Proyecto

```
cursosmarlon/
├── cursosmarlon/          # Configuración principal del proyecto
├── cursos/                # App principal de cursos
├── users/                 # Gestión de usuarios
├── payments/              # Sistema de pagos
├── templates/             # Templates HTML
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── media/                # Archivos subidos por usuarios
├── requirements.txt      # Dependencias Python
└── README.md
```

## 🎯 Funcionalidades Principales


### 👤 Usuarios (Estudiantes)
- Registro y autenticación
- Explorar catálogo de cursos
- Añadir cursos al carrito y realizar pagos
- Acceder a la zona "Mis Cursos" donde ve los cursos comprados y puede continuar aprendiendo desde ahí
- Seguimiento de progreso y dejar reseñas

### 🧑‍🏫 Instructores
- Acceso a un dashboard privado donde pueden:
	- Subir y gestionar cursos
	- Subir clases/lecciones en video
	- Configurar formas de pago
	- Ver estadísticas de ventas y estudiantes inscritos

### 🛡️ Administradores
- Panel de administración completo
- Gestión de usuarios, roles, pagos y órdenes
- Configuración de cupones de descuento
- Estadísticas y reportes

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2+, Django REST Framework
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Frontend**: Bootstrap 5, JavaScript
- **Pagos**: Stripe, PayPal
- **Tareas Asíncronas**: Celery + Redis
- **Almacenamiento**: Whitenoise (archivos estáticos)
- **Deploy**: Heroku, Docker

## 🔧 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones  
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test

# Ejecutar worker de Celery
celery -A cursosmarlon worker --loglevel=info
```

## 📊 Modelos Principales

- **User**: Usuario personalizado con campos adicionales
- **Course**: Curso con información completa
- **Module**: Módulos de un curso
- **Lesson**: Lecciones dentro de los módulos
- **Enrollment**: Inscripciones de estudiantes
- **Payment**: Registro de pagos realizados
- **Cart**: Carrito de compras
- **Review**: Reseñas y calificaciones

## 🚀 Deploy en Producción

### Heroku
```bash
# Instalar Heroku CLI
heroku create tu-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Docker
```bash
docker build -t cursosmarlon .
docker run -p 8000:8000 cursosmarlon
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

**Marlon Falcón**
- Email: info@cursosmarlon.com
- GitHub: [@falconsoft3d](https://github.com/falconsoft3d)
- LinkedIn: [Marlon Falcón](https://linkedin.com/in/marlon-falcon)

## 🎉 Credenciales de Prueba
instructor@cursosmarlon.com

**Admin Panel:**
- URL: http://127.0.0.1:8000
- Usuario: admin@cursosmarlon.com
- Contraseña: admin123

**Dashboard Instructor:**
- URL: http://127.0.0.1:8000
- Usuario: demo
- Contraseña: demo


---es
