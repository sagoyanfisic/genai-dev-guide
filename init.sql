-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS product_catalog_db;

-- Usar la base de datos
USE product_catalog_db;

-- Crear usuario si no existe
CREATE USER IF NOT EXISTS 'catalog_user'@'%' IDENTIFIED BY 'catalog_password';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON product_catalog_db.* TO 'catalog_user'@'%';

-- Aplicar cambios
FLUSH PRIVILEGES;