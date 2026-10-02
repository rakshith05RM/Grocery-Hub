-- DATABASE grocerydb for GROCERY HUB PROJECT
CREATE DATABASE grocerydb;
-- Making Use of grocerydb DATABASE
USE grocerydb;
-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
-- GROCERY TABLE
CREATE TABLE grocery (
    grocId INT PRIMARY KEY AUTO_INCREMENT,
    grocName VARCHAR(50) NOT NULL,
    grocPrice FLOAT NOT NULL,
    grocImg BLOB,
    grocType VARCHAR(50),
    grocQuantity VARCHAR(50),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- LOGIN ATTEMPTS TABLE
CREATE TABLE loginattempts (
    attempt_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    attempt_time DATETIME NOT NULL,
    success TINYINT(1) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- LOGIN SESSIONS TABLE
CREATE TABLE loginsessions (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    login_time DATETIME NOT NULL,
    logout_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
-- ORDERS TABLE
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    order_datetime DATETIME NOT NULL,
    order_items TEXT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id));
