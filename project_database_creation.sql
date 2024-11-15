DROP DATABASE IF EXISTS bank_management;
CREATE DATABASE bank_management;
USE bank_management;
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    password VARCHAR(255) NOT NULL  -- Added for storing hashed password
);
CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    bank_name VARCHAR(100)
);
CREATE TABLE accounts (
    account_no INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    branch_id INT,
    account_type ENUM('savings', 'checking', 'loan') NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE SET NULL
);
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no INT,
    transaction_type ENUM('deposit', 'withdrawal') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_no) REFERENCES accounts(account_no) ON DELETE CASCADE
);
SHOW TABLES;
DESCRIBE customers;
DESCRIBE branches;
DESCRIBE accounts;
DESCRIBE transactions;