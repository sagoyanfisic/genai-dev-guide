# Deployment Guide - PDF AI Assistant

## 🚀 Deployment Options

### 1. Local Development
```bash
# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar con Docker Compose
docker-compose up --build
```

### 2. Production con GCP Secret Manager

#### Prerequisitos
- Proyecto GCP configurado
- Service Account con permisos de Secret Manager
- Google Cloud CLI instalado

#### Setup GCP Secret Manager

```bash
# 1. Crear service account
gcloud iam service-accounts create pdf-ai-app \
    --description="Service account for PDF AI App" \
    --display-name="PDF AI App"

# 2. Asignar permisos
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:pdf-ai-app@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# 3. Crear key del service account
gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=pdf-ai-app@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 4. Crear secrets manualmente en GCP Console o CLI:
gcloud secrets create google-api-key --data-file=- <<< "YOUR_GEMINI_API_KEY"
gcloud secrets create db-password --data-file=- <<< "YOUR_DB_PASSWORD"
```

#### Variables de Entorno para Producción
```bash
export GCP_PROJECT_ID=your-gcp-project-id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 3. GitHub Actions CI/CD

#### Secrets requeridos en GitHub:
```
GCP_SA_KEY: Contenido del service-account-key.json (base64)
GCP_PROJECT_ID: ID del proyecto GCP
```

#### Setup GitHub Secrets:
```bash
# Convertir service account key a base64
cat service-account-key.json | base64 | pbcopy

# Agregar como secret GCP_SA_KEY en GitHub Settings > Secrets
```

#### Workflow Features:
- ✅ Tests unitarios con pytest
- ✅ Security scan con Bandit
- ✅ Vulnerability scan con Trivy
- ✅ Multi-stage deployment (staging/production)
- ✅ Docker image build & push a GCR

## 🧪 Testing

### Ejecutar Tests Localmente
```bash
# Tests unitarios
pytest tests/unit/ -v

# Tests con coverage
pytest tests/unit/ --cov=app --cov-report=html

# Tests específicos
pytest tests/unit/test_document_processor_service.py -v
```

### Tests en CI/CD
- Se ejecutan automáticamente en cada push/PR
- Incluye security scanning y vulnerability assessment

## 🔐 Security & Secret Management

### Variables Sensibles:
- `google-api-key`: API Key de Google Gemini
- `db-password`: Password de la base de datos

### Fallback Strategy:
1. **Primero**: Intenta obtener de GCP Secret Manager
2. **Fallback**: Usa variables de entorno locales

### Ejemplo de Uso:
```python
# La aplicación automáticamente:
# 1. Intenta obtener 'google-api-key' de Secret Manager
# 2. Si falla, usa GOOGLE_API_KEY de env vars
```

## 🐳 Docker Images

### Registry: Google Container Registry (GCR)
```
gcr.io/YOUR_PROJECT_ID/pdf-ai-app:latest
gcr.io/YOUR_PROJECT_ID/pdf-ai-app:v1.0.0
gcr.io/YOUR_PROJECT_ID/pdf-ai-app:develop
```

### Tagging Strategy:
- `latest`: Branch main
- `develop`: Branch develop  
- `v*`: Tags semánticos
- `main-sha123`: Commit específico

## 🚀 Production Deployment

### Cloud Run (Recomendado)
```bash
# Deploy desde imagen
gcloud run deploy pdf-ai-app \
    --image gcr.io/YOUR_PROJECT_ID/pdf-ai-app:latest \
    --platform managed \
    --region us-central1 \
    --set-env-vars GCP_PROJECT_ID=YOUR_PROJECT_ID \
    --service-account pdf-ai-app@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pdf-ai-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: gcr.io/YOUR_PROJECT_ID/pdf-ai-app:latest
        env:
        - name: GCP_PROJECT_ID
          value: "YOUR_PROJECT_ID"
        - name: ENVIRONMENT
          value: "production"
```

## 📊 Monitoring & Logs

### Health Checks
- `/health`: Application health
- `/docs`: API documentation
- Container health checks configurados

### Logs Structure
- Access logs: `/app/logs/access.log`
- Error logs: `/app/logs/error.log`
- Application logs: stdout/stderr

### Metrics
- Request latency
- Error rates
- Resource utilization
- Secret access events

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Secret Manager Access Denied
```bash
# Verificar permisos del service account
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --format="table(bindings.role)" \
    --filter="bindings.members:pdf-ai-app@YOUR_PROJECT_ID.iam.gserviceaccount.com"
```

#### 2. Tests Failing
```bash
# Verificar variables de entorno para testing
export GOOGLE_API_KEY="fake-key-for-testing"
pytest tests/unit/ -v
```

#### 3. Docker Build Issues
```bash
# Clean build
docker system prune -a
docker-compose build --no-cache
```

#### 4. Secret Not Found
```bash
# Listar secrets disponibles
gcloud secrets list

# Verificar contenido del secret
gcloud secrets versions access latest --secret="google-api-key"
```

## 🔄 Rollback Strategy

### GitHub Actions
- Manual rollback via GitHub Actions
- Deploy tag específico para rollback

### Cloud Run
```bash
# Rollback a revisión anterior
gcloud run services update-traffic pdf-ai-app \
    --to-revisions PREVIOUS_REVISION=100
```

### Kubernetes
```bash
# Rollback deployment
kubectl rollout undo deployment/pdf-ai-app
```