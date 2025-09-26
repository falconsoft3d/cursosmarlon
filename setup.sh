#!/bin/bash

# Script de instalación y configuración para CursosMarlon

echo "🚀 Configurando proyecto CursosMarlon..."

# Crear directorio de media
mkdir -p media/avatars
mkdir -p media/courses/thumbnails
mkdir -p media/courses/previews
mkdir -p media/courses/lessons

echo "✅ Directorios de media creados"

# Configurar variables de entorno
echo "📝 Configurando variables de entorno..."
echo "Por favor configura las siguientes variables en tu archivo .env:"
echo ""
echo "STRIPE_PUBLIC_KEY=tu_stripe_public_key"
echo "STRIPE_SECRET_KEY=tu_stripe_secret_key"
echo "PAYPAL_CLIENT_ID=tu_paypal_client_id" 
echo "PAYPAL_CLIENT_SECRET=tu_paypal_client_secret"
echo "EMAIL_HOST_USER=tu_email@gmail.com"
echo "EMAIL_HOST_PASSWORD=tu_app_password"
echo ""

# Recopilar archivos estáticos
echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🎉 ¡Configuración completada!"
echo ""
echo "Para iniciar el servidor de desarrollo:"
echo "python manage.py runserver"
echo ""
echo "Para acceder al panel de administración:"
echo "http://127.0.0.1:8000/admin/"
echo "Usuario: admin@cursosmarlon.com"
echo "Contraseña: admin123"