#!/bin/bash
set -euo pipefail

echo "🚀 Starting Dashveider Backend (AWS Production)..."

# Verificar variables de entorno requeridas
required_vars=("DJANGO_SECRET_KEY" "POSTGRES_NAME" "POSTGRES_USER" "POSTGRES_PASSWORD" "DB_HOST")
for var in "${required_vars[@]}"; do
    if [ -z "${!var:-}" ]; then
        echo "❌ Error: $var environment variable is required"
        exit 1
    fi
done

# Crear directorios necesarios
mkdir -p db

echo "📦 Pulling latest images..."
docker compose -f docker-compose.aws.yml pull

echo "🚀 Starting services..."
docker compose -f docker-compose.aws.yml up -d

echo "⏳ Waiting for backend to be ready..."
until docker compose -f docker-compose.aws.yml exec -T backend curl -f http://localhost:8000/api/build >/dev/null 2>&1; do
    echo "Backend is not ready - waiting 15s..."
    sleep 15
done

echo "✅ Backend is ready!"
echo "🌐 API available at: ${DASHVEIDER_URL:-https://your-domain.com}/api"
echo "�� API Documentation: ${DASHVEIDER_URL:-https://your-domain.com}/api/schema/swagger-ui/"