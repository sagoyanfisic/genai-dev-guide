# Cloud SQL Configuration Guide - IAM Authentication

Esta guía te ayudará a configurar tu aplicación para usar Google Cloud SQL con **IAM Database Authentication** (método recomendado y seguro).

## ¿Por qué IAM Authentication?

✅ **Más seguro**: No hay contraseñas que manejar o rotar
✅ **Escalable**: Usa identidades de Google Cloud
✅ **Auditable**: Mejor logging y control de acceso
✅ **Cloud Run Ready**: Funciona perfectamente con service accounts

## Prerrequisitos

1. **Google Cloud Project** configurado
2. **Cloud SQL instance** creado en tu VPC con flag `--database-flags=cloudsql_iam_authentication=on`
3. **Service Account** con permisos apropiados
4. **IAM Database User** creado en Cloud SQL

## Setup de Cloud SQL con IAM Authentication

### 1. Crear y configurar Service Account

```bash
# Crear service account
gcloud iam service-accounts create cloudsql-app \
    --display-name="Cloud SQL App Service Account"

# Asignar permisos necesarios
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:cloudsql-app@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"
```

### 2. Crear Cloud SQL instance con IAM habilitado

```bash
gcloud sql instances create tu-instancia \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --network=tu-vpc-network \
    --no-assign-ip \
    --database-flags=cloudsql_iam_authentication=on
```

### 3. Crear IAM Database User

```bash
# Crear usuario IAM (usando el service account)
gcloud sql users create cloudsql-app@YOUR_PROJECT_ID.iam.gserviceaccount.com \
    --instance=tu-instancia \
    --type=cloud_iam_service_account

# Darle permisos en la base de datos
gcloud sql databases create tu_base_datos --instance=tu-instancia
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo:
```bash
cp .env.cloud-sql.example .env
```

Edita el archivo `.env`:
```env
USE_CLOUD_SQL=true
USE_IAM_AUTH=true
CLOUD_SQL_INSTANCE_CONNECTION_NAME=tu-proyecto:tu-region:tu-instancia
CLOUD_SQL_IAM_USER=cloudsql-app@tu-proyecto.iam.gserviceaccount.com

DB_NAME=tu_base_datos
# No DB_PASSWORD necesario con IAM auth
```

### 5. Configurar permisos de base de datos

Conéctate a la instancia y da permisos al usuario IAM:

```sql
-- Conectar usando Cloud SQL Proxy o consola web
GRANT ALL PRIVILEGES ON tu_base_datos.* TO 'cloudsql-app@tu-proyecto.iam.gserviceaccount.com'@'%';
FLUSH PRIVILEGES;
```

### 6. Ejecutar la aplicación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar autenticación (para desarrollo local)
gcloud auth application-default login

# Ejecutar migraciones
alembic upgrade head

# Iniciar aplicación
uvicorn app.main:app --reload
```

## Deployment en Cloud Run

### 1. Build y deploy

```bash
# Build de la imagen
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cloudsql-app

# Deploy en Cloud Run
gcloud run deploy cloudsql-app \
    --image gcr.io/YOUR_PROJECT_ID/cloudsql-app \
    --service-account cloudsql-app@YOUR_PROJECT_ID.iam.gserviceaccount.com \
    --add-cloudsql-instances YOUR_PROJECT_ID:REGION:INSTANCE_NAME \
    --set-env-vars USE_CLOUD_SQL=true,USE_IAM_AUTH=true \
    --set-env-vars CLOUD_SQL_INSTANCE_CONNECTION_NAME=YOUR_PROJECT_ID:REGION:INSTANCE_NAME \
    --set-env-vars DB_NAME=tu_base_datos \
    --vpc-connector your-vpc-connector \
    --region us-central1
```

### 2. Variables de entorno para Cloud Run

```bash
# Configurar variables de entorno
gcloud run services update cloudsql-app \
    --set-env-vars USE_CLOUD_SQL=true \
    --set-env-vars USE_IAM_AUTH=true \
    --set-env-vars CLOUD_SQL_INSTANCE_CONNECTION_NAME=tu-proyecto:tu-region:tu-instancia \
    --set-env-vars CLOUD_SQL_IAM_USER=cloudsql-app@tu-proyecto.iam.gserviceaccount.com \
    --set-env-vars DB_NAME=tu_base_datos
```

## Desarrollo Local

Para desarrollo local con Cloud SQL, simplemente configura las variables de entorno:

```bash
# Configurar variables de entorno
export USE_CLOUD_SQL=true
export USE_IAM_AUTH=true
export CLOUD_SQL_INSTANCE_CONNECTION_NAME="tu-proyecto:tu-region:tu-instancia"
export CLOUD_SQL_IAM_USER="cloudsql-app@tu-proyecto.iam.gserviceaccount.com"
export DB_NAME="tu_base_datos"

# Configurar autenticación local
gcloud auth application-default login

# Ejecutar aplicación - el Python Connector se encarga de la conexión
uvicorn app.main:app --reload
```

## Permisos Necesarios

Tu service account necesita estos roles:

```bash
# Permisos mínimos necesarios
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:cloudsql-app@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

# Para Cloud Run deployment
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:cloudsql-app@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.instanceUser"
```

## Migración desde MariaDB local

1. **Exportar datos existentes**:
```bash
docker exec pdf_ai_mariadb mysqldump -u root -p pdf_ai_db > backup.sql
```

2. **Importar a Cloud SQL**:
```bash
gcloud sql import sql tu-instancia gs://tu-bucket/backup.sql \\
    --database=tu_base_datos
```

3. **Cambiar configuración**:
```bash
# En .env
USE_CLOUD_SQL=true
# ... resto de configuración Cloud SQL
```

4. **Reiniciar aplicación**

## Troubleshooting

### Error: "IAM authentication failed"
- Verifica que IAM authentication esté habilitado: `--database-flags=cloudsql_iam_authentication=on`
- Confirma que el usuario IAM exista: `gcloud sql users list --instance=tu-instancia`
- Revisa permisos del service account: `gcloud projects get-iam-policy YOUR_PROJECT_ID`

### Error: "connection refused"
- Confirma que el `INSTANCE_CONNECTION_NAME` sea correcto
- Revisa que las credenciales de aplicación estén configuradas: `gcloud auth application-default print-access-token`
- Verifica conectividad de red (VPC, firewall rules)

### Error: "Access denied for user"
- Ejecuta los GRANT statements en la base de datos
- Verifica que el usuario IAM tenga permisos: `SHOW GRANTS FOR 'user@domain.iam.gserviceaccount.com'@'%';`

### Error: "instance not found"
- Confirma que el formato sea: `PROJECT_ID:REGION:INSTANCE_NAME`
- Verifica que la instancia exista: `gcloud sql instances list`

### Cloud Run connection issues
- Verifica que el service account esté asignado al servicio
- Confirma que `--add-cloudsql-instances` esté configurado
- Revisa que el VPC connector permita acceso a Cloud SQL

## Monitoreo

Para monitorear las conexiones de Cloud SQL:

```bash
# Ver logs de la aplicación
kubectl logs deployment/cloudsql-app  # En GKE
docker logs container_name           # En Docker

# Ver métricas en Cloud Console
# https://console.cloud.google.com/sql/instances/tu-instancia/monitoring

# Ver logs de Cloud SQL
gcloud logging read "resource.type=gce_instance" --limit=50
```

## Arquitectura Final

```
Cloud Run Service (VPC Connector)
    ↓ (Python Connector + IAM Auth)
Cloud SQL Instance (Private VPC)
    ↓ (IAM Database User)
Database Tables
```

- **Sin proxy necesario**: Conexión directa desde Cloud Run
- **Sin credenciales**: Solo IAM authentication
- **Completamente en VPC**: Comunicación privada
- **Escalable**: Connection pooling automático