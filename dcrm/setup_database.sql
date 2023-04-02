-- Preparing the MySQL server for the project
CREATE DATABASE IF NOT EXISTS crm_django;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'django_user_pwd';
GRANT ALL PRIVILEGES ON *.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
