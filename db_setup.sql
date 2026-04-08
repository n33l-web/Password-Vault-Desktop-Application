CREATE DATABASE IF NOT EXISTS password_vault;
USE password_vault;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS credentials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    site_name VARCHAR(100),
    login_username VARCHAR(100),
    encrypted_password BLOB,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

SHOW DATABASES;
USE password_vault;
SHOW TABLES;
DESCRIBE users;
DESCRIBE credentials;
