#!/bin/bash
set -euo pipefail

echo "🚀 Starting Dashveider Backend (Local Development)..."

# Crear directorios necesarios
mkdir -p db logs

# Verificar si ya existe la base de datos
if [ -d ./db ] && [ "$(ls -A ./db)" ]; then
    echo "📁 Database directory exists. Starting services..."
    docker compose -f docker-compose.yml up -d
else
    echo "📁 First time setup. Initializing database..."
    docker compose -f docker-compose.yml up -d
    
    echo "⏳ Waiting for backend to be ready..."
    until docker compose -f docker-compose.yml exec -T backend curl -f http://localhost:8000/api/build >/dev/null 2>&1; do
        echo "Backend is not ready - waiting 10s..."
        sleep 10
    done
    
    echo "👤 Creating superuser..."
    docker compose -f docker-compose.yml exec backend poetry run python manage.py createsuperuser
fi

echo "✅ Backend is ready!"
echo "🌐 API available at: http://localhost:8000/api"
echo "📚 API Documentation: http://localhost:8000/api/schema/swagger-ui/"
echo "🔧 Admin Panel: http://localhost:8000/admin"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker compose -f docker-compose.yml logs -f"
echo "  Stop services: docker compose -f docker-compose.yml down"
echo "  Rebuild: docker compose -f docker-compose.yml up --build -d"