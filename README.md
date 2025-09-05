# PDF AI App - Catálogo de Productos con IA

Una aplicación FastAPI moderna para gestión de productos con generación automática de descripciones usando Google Gemini AI.

## 📋 Descripción General

Esta aplicación implementa un catálogo de productos siguiendo principios de Domain-Driven Design (DDD) con integración de servicios de IA para generación automática de contenido. Soporta tanto Google Gemini Direct API como Vertex AI según configuración.

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
pdf_ai_app/
├── app/                          # Código fuente principal
│   ├── __init__.py
│   ├── main.py                   # Aplicación FastAPI principal
│   │
│   ├── core/                     # Núcleo de la aplicación
│   │   ├── config.py            # Configuración y settings
│   │   ├── database.py          # Configuración de base de datos
│   │   ├── dependencies.py      # Dependencias de FastAPI
│   │   └── secret_manager.py    # Gestión de secretos GCP
│   │
│   ├── domain/                   # Capa de dominio (DDD)
│   │   └── entities.py          # Entidades de negocio
│   │
│   ├── models/                   # Modelos de base de datos
│   │   └── product.py           # Modelo SQLAlchemy Product
│   │
│   ├── infrastructure/           # Capa de infraestructura
│   │   ├── ai_services.py       # Servicios de IA (Gemini/Vertex)
│   │   ├── ai_factory.py        # Factory pattern para servicios IA
│   │   ├── database.py          # Repositorio de productos
│   │   ├── external_services.py # Facade para servicios externos
│   │   ├── prompts.py           # Templates de prompts IA
│   │   └── exceptions.py        # Excepciones personalizadas
│   │
│   ├── application/              # Capa de aplicación
│   │   └── product_service.py   # Servicios de casos de uso
│   │
│   └── routers/                  # Capa de presentación
│       ├── product_router.py    # Endpoints de API
│       ├── schemas.py           # Esquemas Pydantic
│       └── utils.py             # Utilidades de router
│
├── tests/                        # Tests organizados por tipo
│   ├── conftest.py              # Fixtures compartidas
│   ├── unit/                    # Tests unitarios
│   ├── integration/             # Tests de integración
│   └── e2e/                     # Tests end-to-end
│
├── docker-compose.yml           # Orquestación de contenedores
├── Dockerfile                   # Imagen Docker multi-stage
├── Makefile                     # Automatización de tareas
├── requirements.txt             # Dependencias Python
├── pytest.ini                  # Configuración de testing
├── gunicorn.conf.py            # Configuración servidor WSGI
└── .env.example                # Variables de entorno ejemplo
```

## 🚀 Características Principales

### ✨ Funcionalidades Core

- **📦 Gestión de Productos**: CRUD completo con validaciones de dominio
- **🤖 IA Integrada**: Generación automática de descripciones con Gemini AI
- **🔄 Dual Backend IA**: Soporte para Gemini Direct API y Vertex AI
- **📊 API RESTful**: Endpoints documentados con OpenAPI/Swagger
- **🗄️ Base de Datos**: MariaDB 11 con SQLAlchemy async
- **🐳 Containerización**: Docker y docker-compose ready
- **🧪 Testing**: Suite completa de tests unitarios, integración y E2E

### 🛠️ Tecnologías Utilizadas

#### Backend
- **FastAPI 0.104**: Framework web moderno y rápido
- **Python 3.11**: Lenguaje de programación
- **SQLAlchemy 2.0**: ORM con soporte async
- **Pydantic 2.5**: Validación y serialización de datos
- **Alembic**: Migraciones de base de datos

#### Base de Datos
- **MariaDB 11**: Sistema de gestión de base de datos
- **aiomysql**: Driver async para MySQL/MariaDB

#### IA y Machine Learning
- **Google Generative AI**: SDK directo para Gemini
- **Google Cloud AI Platform**: Vertex AI para empresas
- **Custom Prompts**: Templates optimizados para e-commerce

#### DevOps y Despliegue
- **Docker**: Containerización con multi-stage builds
- **Gunicorn + Uvicorn**: Servidor WSGI de producción
- **pytest**: Framework de testing
- **GitHub Actions**: CI/CD (configuración disponible)

## ⚙️ Configuración e Instalación

### Prerrequisitos

- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)
- Google API Key (Gemini) o Proyecto GCP (Vertex AI)

### 🐳 Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd pdf_ai_app
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

3. **Iniciar servicios**
```bash
make up
# O directamente: docker-compose up -d
```

4. **Verificar instalación**
```bash
# API disponible en: http://localhost:8000
# Documentación en: http://localhost:8000/docs
curl http://localhost:8000/health
```

### 💻 Instalación Local (Desarrollo)

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
# Iniciar MariaDB con Docker
docker run -d --name mariadb -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -e MYSQL_DATABASE=pdf_ai_db \
  -e MYSQL_USER=pdf_user \
  -e MYSQL_PASSWORD=pdf_password \
  mariadb:11
```

4. **Ejecutar migraciones**
```bash
alembic upgrade head
```

5. **Iniciar aplicación**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuración

### Variables de Entorno Principales

```bash
# Configuración de Base de Datos
DATABASE_URL=mysql+aiomysql://pdf_user:pdf_password@mariadb:3306/pdf_ai_db
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=pdf_ai_db
DB_USER=pdf_user
DB_PASSWORD=pdf_password

# Configuración de IA
GOOGLE_API_KEY=tu_api_key_aqui
USE_VERTEX_AI=false                    # true para usar Vertex AI
VERTEX_AI_PROJECT_ID=tu-proyecto-gcp   # Solo si USE_VERTEX_AI=true
VERTEX_AI_LOCATION=us-central1

# Configuración de Aplicación
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# GCP (Opcional para Vertex AI o Secret Manager)
GCP_PROJECT_ID=tu-proyecto-gcp
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### Configuración de Servicios IA

#### Opción 1: Google Gemini Direct API
```bash
USE_VERTEX_AI=false
GOOGLE_API_KEY=tu_gemini_api_key
```

#### Opción 2: Google Vertex AI
```bash
USE_VERTEX_AI=true
VERTEX_AI_PROJECT_ID=tu-proyecto-gcp
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## 📚 Guía de Uso

### 🔗 Endpoints de API

#### Productos
```bash
# Listar productos
GET /products/

# Crear producto
POST /products/
{
  "name": "iPhone 15 Pro",
  "category": "Smartphones",
  "brand": "Apple", 
  "price": 999.99,
  "basic_info": "Smartphone premium con chip A17 Pro"
}

# Obtener producto por ID
GET /products/{product_id}

# Actualizar producto
PUT /products/{product_id}

# Eliminar producto
DELETE /products/{product_id}
```

#### Servicios de IA
```bash
# Generar descripción de producto
POST /products/generate-description
{
  "name": "MacBook Pro M3",
  "category": "Laptops",
  "brand": "Apple",
  "basic_info": "Laptop profesional con chip M3"
}

# Generar sugerencias de productos
GET /products/suggestions/{category}?count=5

# Mejorar descripción existente
POST /products/improve-description
{
  "current_description": "Laptop básica para trabajo"
}
```

#### Utilidades
```bash
# Health check
GET /health

# Información del servicio IA activo
GET /ai-service-info
```

### 📖 Documentación Interactiva

La API incluye documentación automática:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
make test

# Por categoría
pytest tests/unit/           # Tests unitarios
pytest tests/integration/    # Tests de integración
pytest tests/e2e/           # Tests end-to-end

# Con coverage
pytest --cov=app --cov-report=html
```

### Estructura de Tests

- **Unit Tests**: Lógica de negocio aislada (entidades, prompts, factory)
- **Integration Tests**: Servicios externos (IA APIs, base de datos)
- **E2E Tests**: Flujos completos de usuario a través de API

### Fixtures Disponibles

```python
# Sesión de BD mockeada
def test_product_creation(mock_db_session):
    pass

# Cliente de API con BD mockeada  
def test_api_endpoint(test_client_with_db):
    pass

# Servicio IA mockeado
def test_ai_functionality(mock_ai_service):
    pass

# Datos de prueba
def test_validation(sample_product_data):
    pass
```

## 🛠️ Comandos de Desarrollo

### Makefile Commands

```bash
make help          # Mostrar ayuda
make build         # Construir imágenes Docker
make up            # Iniciar servicios
make down          # Detener servicios
make logs          # Ver logs en tiempo real
make shell         # Shell en contenedor app
make db-shell      # Shell en base de datos
make test          # Ejecutar tests
make clean         # Limpiar recursos Docker
make restart       # Reiniciar servicios
make status        # Estado de servicios
```

### Comandos Docker Compose

```bash
# Desarrollo
docker-compose up -d                    # Iniciar servicios
docker-compose logs -f app              # Ver logs app
docker-compose exec app bash            # Shell en app
docker-compose exec mariadb mysql -u pdf_user -p pdf_ai_db

# Producción
docker-compose -f docker-compose.yml --env-file .env.production up -d
```

## 🏛️ Arquitectura Detallada

### Capas de la Aplicación (DDD)

#### 1. **Domain Layer** (`app/domain/`)
- **Entidades de Negocio**: `Product` con validaciones de dominio
- **Value Objects**: Objetos inmutables como `Price`, `ProductId` (implícitos)
- **Domain Services**: Lógica de dominio que no pertenece a entidades

```python
# Ejemplo: Entidad Product
class Product(BaseModel):
    def is_valid(self) -> bool:
        """Validación de reglas de negocio"""
        
    def is_available(self) -> bool:
        """Lógica de disponibilidad"""
```

#### 2. **Application Layer** (`app/application/`)
- **Use Cases**: `ProductService` orquesta operaciones de negocio
- **Application Services**: Coordinan infraestructura y dominio
- **Command/Query Handlers**: Separación de operaciones de escritura/lectura

```python
# Ejemplo: Caso de uso
async def create_product_with_ai_description(self, product_data):
    # 1. Crear entidad de dominio
    # 2. Validar reglas de negocio  
    # 3. Generar descripción con IA
    # 4. Persistir en repositorio
```

#### 3. **Infrastructure Layer** (`app/infrastructure/`)
- **Repositorios**: Acceso a datos con SQLAlchemy
- **Servicios Externos**: Integración con APIs de IA
- **Factory Pattern**: Creación de servicios según configuración

```python
# Ejemplo: Factory Pattern para IA
class AIServiceFactory:
    @staticmethod
    def create_ai_service() -> AIServiceInterface:
        if settings.use_vertex_ai:
            return VertexAIService(...)
        else:
            return GeminiDirectService(...)
```

#### 4. **Presentation Layer** (`app/routers/`)
- **API Controllers**: Endpoints REST con FastAPI
- **DTOs**: Esquemas Pydantic para request/response
- **Middleware**: CORS, logging, error handling

### Patrones de Diseño Implementados

#### 🏭 **Factory Pattern** 
Creación de servicios IA según configuración:
```python
service = AIServiceFactory.create_ai_service()
```

#### 🎭 **Facade Pattern**
Simplificación de servicios complejos:
```python
class GeminiAIService:
    def __init__(self):
        self._ai_service = AIServiceFactory.create_ai_service()
```

#### 💉 **Dependency Injection**
Inyección de dependencias con FastAPI:
```python
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_database),
    service: ProductService = Depends(get_product_service)
):
```

#### 🔧 **Repository Pattern**
Abstracción de acceso a datos:
```python
class ProductRepository:
    async def create(self, product: Product) -> Product:
    async def get_by_id(self, product_id: int) -> Optional[Product]:
```

## 🔒 Seguridad

### Medidas de Seguridad Implementadas

1. **CORS Configurado**: Origins específicos, no wildcard
2. **Validación de Entrada**: Pydantic schemas en todos los endpoints
3. **SQL Injection Protection**: SQLAlchemy ORM
4. **Gestión de Secretos**: Google Secret Manager integration
5. **User Non-root**: Contenedores ejecutan con usuario limitado
6. **Input Sanitization**: Validación y limpieza de strings

### Configuración de Seguridad

```python
# CORS seguro
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # No usar ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)

# Validación de entrada
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0)
```

## 📊 Monitoreo y Logging

### Logs Estructurados

```python
import logging

logger = logging.getLogger(__name__)

# Ejemplo de logging en servicios
logger.info(f"Generating description for product: {product.name}")
logger.error(f"AI service error: {error}", extra={"product_id": product.id})
```

### Health Checks

```bash
# Application health
GET /health
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:00:00Z",
  "version": "1.0.0"
}

# Database health (a través de ORM)
# AI service health (a través de factory info)
```

### Métricas Recomendadas

- **Latencia de API**: Tiempo de respuesta por endpoint
- **Uso de IA**: Llamadas exitosas/fallidas a servicios IA
- **Base de Datos**: Conexiones activas, query time
- **Errores**: Tasa de errores por endpoint

## 🚀 Despliegue en Producción

### Checklist de Producción

- [ ] Variables de entorno configuradas
- [ ] CORS con dominios específicos
- [ ] Base de datos con credenciales seguras
- [ ] SSL/TLS habilitado
- [ ] Logs centralizados
- [ ] Monitoreo activo
- [ ] Backups configurados
- [ ] Rate limiting habilitado

### Docker en Producción

```bash
# Build optimizado para producción
docker build --target production -t pdf-ai-app:prod .

# Despliegue con variables de entorno
docker-compose --env-file .env.production up -d

# Logs en producción
docker-compose logs --tail=100 -f app
```

### Variables de Entorno Producción

```bash
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DB_PASSWORD=secure_password_here
GOOGLE_API_KEY=production_api_key
```

## 🤝 Contribución

### Guías de Desarrollo

1. **Seguir principios DDD**: Mantener separación de capas
2. **Tests obligatorios**: Mínimo 80% coverage
3. **Type hints**: Usar anotaciones de tipo
4. **Documentación**: Docstrings en funciones públicas
5. **Convenciones**: Nombres en inglés, documentación en español

### Proceso de Contribución

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Add nueva funcionalidad'`
4. Push rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📞 Soporte

### Problemas Comunes

**❌ Error de conexión a base de datos**
```bash
# Verificar servicio MariaDB
make status
docker-compose logs mariadb

# Reiniciar servicios
make restart
```

**❌ Error de API Key de Gemini**
```bash
# Verificar variable de entorno
echo $GOOGLE_API_KEY

# Verificar configuración
curl http://localhost:8000/ai-service-info
```

**❌ Tests fallan**
```bash
# Limpiar entorno de test
pytest --cache-clear

# Ejecutar tests específicos
pytest tests/unit/test_entities.py -v
```

### Logs y Debugging

```bash
# Ver logs de aplicación
make logs

# Debug en desarrollo
docker-compose exec app python -m pdb app/main.py

# Logs específicos
docker-compose logs --tail=50 app
```

## 📄 Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

## 📈 Roadmap

### Versión 2.0 (Futuro)
- [ ] Autenticación JWT
- [ ] Rate limiting por usuario
- [ ] Cache Redis para respuestas IA
- [ ] Websockets para notificaciones
- [ ] API GraphQL
- [ ] Microservicios con Kubernetes
- [ ] Métricas con Prometheus
- [ ] CI/CD con GitHub Actions

---

**Desarrollado con ❤️ usando FastAPI, Docker y Google Gemini AI**

Para más información, consulta la [documentación de la API](http://localhost:8000/docs) o contacta al equipo de desarrollo.