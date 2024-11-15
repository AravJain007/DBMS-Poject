from os import name
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*****'
app.config['MYSQL_DB'] = 'bank_management'

mysql = MySQL(app)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers (name, phone, address, password) VALUES (%s, %s, %s, %s)", (name, phone, address, password))
        mysql.connection.commit()
        cur.close()
        flash("Registration successful!", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        # Retrieve user data from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT customer_id, password FROM customers WHERE name = %s", (name,))
        user = cur.fetchone()
        print("USER: ", user)
        cur.close()

        # Debugging statements
        print("User fetched from DB:", user)

        if user==None:
            flash("The User does not exist. Please try some other Username.", "danger")
            return redirect(url_for('register'))

        # Check if user exists and password matches
        if user[0] and user[1]==password:
            session['customer_id'] = user[0]
            session['name'] = user[1]
            print("Login successful. Redirecting to dashboard.")
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        
        flash("Invalid credentials. Please try again.", "danger")
        print("Login failed. Incorrect credentials.")
    
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'customer_id' in session:
        cur = mysql.connection.cursor()
        
        # Fetch account details
        cur.execute("SELECT account_no, account_type, balance FROM accounts WHERE customer_id = %s", (session['customer_id'],))
        accounts = cur.fetchall()
        
        # Fetch recent transactions for each account
        transactions = []
        for account in accounts:
            account_no = account[0]
            cur.execute("SELECT transaction_date, amount FROM transactions WHERE account_no = %s ORDER BY transaction_date DESC LIMIT 5", (account_no,))
            transactions += [(account_no, trans[0], trans[1]) for trans in cur.fetchall()]
        
        cur.execute("SELECT name FROM customers WHERE customer_id = %s", (session['customer_id'],))
        name = cur.fetchall()
        cur.close()

        return render_template('dashboard.html', name=name[0][0], accounts=accounts, transactions=transactions)
    
    flash("Please log in to view the dashboard.", "warning")
    return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if 'customer_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE customers 
            SET name = %s, phone = %s, address = %s 
            WHERE customer_id = %s
        """, (name, phone, address, session['customer_id']))
        mysql.connection.commit()
        cur.close()

        flash("Details updated successfully!", "success")
        return redirect(url_for('dashboard'))
    
    # Fetch existing customer details
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, phone, address FROM customers WHERE customer_id = %s", (session['customer_id'],))
    customer = cur.fetchone()
    cur.close()
    
    return render_template('update_customer.html', customer={
        'name': customer[0],
        'phone': customer[1],
        'address': customer[2]
    })

# Delete Customer
@app.route('/delete_customer', methods=['GET','POST'])
def delete_customer():
    if 'customer_id' in session:
        cur = mysql.connection.cursor()
        
        # Delete all associated accounts and transactions first
        cur.execute("DELETE FROM transactions WHERE account_no IN (SELECT account_no FROM accounts WHERE customer_id = %s)", (session['customer_id'],))
        cur.execute("DELETE FROM accounts WHERE customer_id = %s", (session['customer_id'],))
        
        # Then delete the customer
        cur.execute("DELETE FROM customers WHERE customer_id = %s", (session['customer_id'],))
        mysql.connection.commit()
        cur.close()

        session.clear()
        flash("Customer deleted successfully!", "info")
        return redirect(url_for('register'))
    
    flash("Please log in to delete your account.", "warning")
    return redirect(url_for('login'))

# Update Account Balance
@app.route('/update_balance/<int:account_no>', methods=['GET', 'POST'])
def update_balance(account_no):
    if 'customer_id' in session:
        if request.method == 'POST':
            transaction_type = request.form['transaction_type']
            amount = float(request.form['amount'])

            cur = mysql.connection.cursor()

            # Fetch current balance
            cur.execute("SELECT balance FROM accounts WHERE account_no = %s", (account_no,))
            account = cur.fetchone()
            if not account:
                flash("Account not found.", "danger")
                return redirect(url_for('dashboard'))
            balance = account[0]

            # Update balance based on transaction type
            if transaction_type == 'deposit':
                new_balance = float(balance) + amount
            elif transaction_type == 'withdrawal':
                if balance < amount:
                    flash("Insufficient balance for withdrawal.", "danger")
                    return redirect(url_for('dashboard'))
                new_balance = float(balance) - amount
            else:
                flash("Invalid transaction type.", "danger")
                return redirect(url_for('dashboard'))

            # Update account and log transaction
            cur.execute("UPDATE accounts SET balance = %s WHERE account_no = %s", (new_balance, account_no))
            cur.execute("INSERT INTO transactions (account_no, transaction_type, amount) VALUES (%s, %s, %s)",
                        (account_no, transaction_type, amount))
            mysql.connection.commit()
            cur.close()

            flash("Account balance updated successfully!", "success")
            return redirect(url_for('dashboard'))

        return render_template('update_balance.html', account_no=account_no)
    
    flash("Please log in to update account balance.", "warning")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
