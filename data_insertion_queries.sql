-- Insert data into the customers table
INSERT INTO customers (name, phone, address, password)
VALUES 
('Alice Johnson', '123-456-7890', '123 Main St, Springfield', 'hashed_password_1'),
('Bob Smith', '987-654-3210', '456 Elm St, Shelbyville', 'hashed_password_2'),
('Carol White', '555-555-5555', '789 Oak St, Springfield', 'hashed_password_3'),
('David Brown', '444-444-4444', '101 Maple St, Shelbyville', 'hashed_password_4'),
('Eve Black', '333-333-3333', '202 Pine St, Springfield', 'hashed_password_5');

-- Insert data into the branches table
INSERT INTO branches (name, address, bank_name)
VALUES 
('Springfield Branch', '123 Main St, Springfield', 'OpenAI Bank'),
('Shelbyville Branch', '456 Elm St, Shelbyville', 'OpenAI Bank');

-- Insert data into the accounts table
INSERT INTO accounts (customer_id, branch_id, account_type, balance)
VALUES 
(1, 1, 'savings', 1500.00),
(1, 1, 'checking', 500.00),
(2, 2, 'savings', 2500.00),
(3, 1, 'loan', 3000.00),
(4, 2, 'checking', 750.00),
(5, 1, 'savings', 1200.00),
(5, 1, 'loan', 5000.00);

-- Insert data into the transactions table
INSERT INTO transactions (account_no, transaction_type, amount)
VALUES 
(1, 'deposit', 500.00),
(1, 'withdrawal', 200.00),
(2, 'deposit', 1500.00),
(3, 'deposit', 2500.00),
(4, 'withdrawal', 300.00),
(5, 'deposit', 1000.00),
(6, 'withdrawal', 700.00),
(7, 'deposit', 2000.00),
(7, 'withdrawal', 1500.00);
