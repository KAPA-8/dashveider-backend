# CISO Assistant Community - Backend

A comprehensive Django-based backend based on the CISO Assistant Community platform, providing security management, compliance assessment, and risk management capabilities.

## 🚀 Quick Start

This project supports both local development and AWS production deployment using Docker containers.

### Prerequisites

- **Docker** (20.10+)
- **Docker Compose** (2.0+)
- **Git**

For AWS deployment, you'll also need:

- AWS CLI configured
- Access to the container registry: `ghcr.io/intuitem/ciso-assistant-community/backend:latest`

## 🏠 Local Development

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ciso-assistant-community/backend
```

### 2. Start Development Environment

The easiest way to get started is using the provided script:

```bash
chmod +x docker-compose.sh
./docker-compose.sh
```

This script will:

- Create necessary directories (`db/`, `logs/`)
- Start the backend and Huey worker services
- Wait for the backend to be ready
- Create a superuser account (first time only)

### 3. Access the Application

Once running, you can access:

- **API**: http://localhost:8000/api
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui/
- **Admin Panel**: http://localhost:8000/admin

### 4. Development Commands

```bash
# View logs
docker compose -f docker-compose.yml logs -f

# Stop services
docker compose -f docker-compose.yml down

# Rebuild and restart
docker compose -f docker-compose.yml up --build -d

# Access backend container
docker compose -f docker-compose.yml exec backend bash

# Run Django commands
docker compose -f docker-compose.yml exec backend poetry run python manage.py <command>
```

### 5. Environment Configuration

The local development environment uses these default settings:

- **Database**: SQLite (stored in `./db/`)
- **Debug Mode**: Enabled
- **Log Level**: INFO
- **Mail Debug**: Enabled
- **Auth Token TTL**: 7200 seconds

## ☁️ AWS Production Deployment

### 1. Environment Setup

Create a `.env` file with the following required variables:

```bash
# Required Variables
DJANGO_SECRET_KEY=your-secret-key-here
POSTGRES_NAME=your-database-name
POSTGRES_USER=your-database-user
POSTGRES_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=5432

# Optional Variables
ALLOWED_HOSTS=your-domain.com
DASHVEIDER_URL=https://your-domain.com
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
AWS_S3_ENDPOINT_URL=https://s3.amazonaws.com
```

### 2. Deploy to AWS

```bash
chmod +x docker-compose-aws.sh
./docker-compose-aws.sh
```

This script will:

- Validate required environment variables
- Pull the latest production images
- Start the production services
- Wait for the backend to be ready

### 3. Production Features

The AWS deployment includes:

- **PostgreSQL Database**: Production-ready database
- **S3 Storage**: File storage for documents and media
- **Health Checks**: Automated service monitoring
- **Auto-restart**: Services restart automatically on failure
- **Optimized Workers**: 4 Huey workers for background tasks

## 🏗️ Architecture

### Services

- **Backend**: Django REST API server (Port 8000)
- **Huey**: Background task processor for async operations

### Key Components

- **Core**: Base models, permissions, and utilities
- **IAM**: Identity and Access Management
- **Library**: Compliance libraries and frameworks
- **Risk Management**: Risk assessment and scenario management
- **Compliance**: Policy and control management
- **Privacy**: GDPR and privacy compliance
- **Resilience**: Business continuity planning
- **TPRM**: Third-party risk management

## 🛠️ Development

### Project Structure

```
backend/
├── ciso_assistant/          # Django project settings
├── core/                    # Core models and utilities
├── iam/                     # Identity and access management
├── library/                 # Compliance libraries
├── ebios_rm/               # Risk management
├── privacy/                 # Privacy compliance
├── resilience/              # Business resilience
├── tprm/                    # Third-party risk management
├── app_tests/              # Test suite
├── docker-compose.yml      # Local development
├── docker-compose.aws.yml  # AWS production
├── docker-compose.sh       # Local startup script
└── docker-compose-aws.sh   # AWS startup script
```

### Technology Stack

- **Framework**: Django 5.1.10 with Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Task Queue**: Huey
- **Storage**: Local files (dev) / AWS S3 (prod)
- **Authentication**: Django REST Knox
- **Documentation**: DRF Spectacular (OpenAPI/Swagger)
- **Monitoring**: Prometheus metrics

### Testing

```bash
# Run all tests
docker compose -f docker-compose.yml exec backend poetry run pytest

# Run specific test module
docker compose -f docker-compose.yml exec backend poetry run pytest app_tests/api/test_api_users.py

# Run with coverage
docker compose -f docker-compose.yml exec backend poetry run pytest --cov=core
```

## 🔧 Configuration

### Environment Variables

| Variable                  | Description                | Default (Local)       | Required (AWS) |
| ------------------------- | -------------------------- | --------------------- | -------------- |
| `DJANGO_SECRET_KEY`       | Django secret key          | Auto-generated        | ✅             |
| `ALLOWED_HOSTS`           | Allowed hostnames          | localhost,127.0.0.1   | ✅             |
| `DASHVEIDER_URL`          | Application URL            | http://localhost:8000 | ✅             |
| `DJANGO_DEBUG`            | Debug mode                 | True                  | False          |
| `LOG_LEVEL`               | Logging level              | INFO                  | WARNING        |
| `AUTH_TOKEN_TTL`          | Token expiration (seconds) | 7200                  | 7200           |
| `POSTGRES_NAME`           | Database name              | -                     | ✅             |
| `POSTGRES_USER`           | Database user              | -                     | ✅             |
| `POSTGRES_PASSWORD`       | Database password          | -                     | ✅             |
| `DB_HOST`                 | Database host              | -                     | ✅             |
| `DB_PORT`                 | Database port              | -                     | 5432           |
| `USE_S3`                  | Use S3 for storage         | False                 | True           |
| `AWS_ACCESS_KEY_ID`       | AWS access key             | -                     | ✅ (if USE_S3) |
| `AWS_SECRET_ACCESS_KEY`   | AWS secret key             | -                     | ✅ (if USE_S3) |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name             | -                     | ✅ (if USE_S3) |

## 🐛 Troubleshooting

### Common Issues

**Backend not starting:**

```bash
# Check logs
docker compose -f docker-compose.yml logs backend

# Check if port 8000 is available
lsof -i :8000
```

**Database connection issues:**

```bash
# Check database container
docker compose -f docker-compose.yml exec backend poetry run python manage.py dbshell

# Reset database (WARNING: This will delete all data)
rm -rf db/
./docker-compose.sh
```

**Permission issues:**

```bash
# Fix file permissions
sudo chown -R $USER:$USER db/ logs/
```

**AWS deployment issues:**

```bash
# Check environment variables
docker compose -f docker-compose.aws.yml config

# Verify AWS credentials
aws sts get-caller-identity
```

### Health Checks

The application includes health checks that verify:

- Backend API is responding
- Database connectivity
- Required services are running

Health check endpoint: `GET /api/build`

## 📚 API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is part of the CISO Assistant Community. Please refer to the main project repository for licensing information.

## 🆘 Support

For support and questions:

- Check the [API documentation](http://localhost:8000/api/schema/swagger-ui/)
- Review the troubleshooting section above
- Open an issue in the project repository

---

**Happy coding! 🚀**
