import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the SQLite database
conn = sqlite3.connect('banking_app.db')
c = conn.cursor()

# Create a table for accounts if not exists
c.execute('''CREATE TABLE IF NOT EXISTS accounts
             (id INTEGER PRIMARY KEY, name TEXT, balance REAL)''')
conn.commit()

# Function to create a new account
def create_account():
    name = name_entry.get()
    initial_balance = float(initial_balance_entry.get())

    c.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, initial_balance))
    conn.commit()
    messagebox.showinfo("Success", "Account created successfully.")

# Function to deposit money into an account
def deposit():
    account_id = int(account_id_entry.get())
    amount = float(deposit_entry.get())

    c.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    conn.commit()
    messagebox.showinfo("Success", "Deposit successful.")

# Function to withdraw money from an account
def withdraw():
    account_id = int(account_id_entry.get())
    amount = float(withdraw_entry.get())

    c.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = c.fetchone()

    if balance and balance[0] >= amount:
        c.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        conn.commit()
        messagebox.showinfo("Success", "Withdrawal successful.")
    else:
        messagebox.showerror("Error", "Insufficient funds.")

# Function to check account balance
def check_balance():
    account_id = int(account_id_entry.get())

    c.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = c.fetchone()

    if balance:
        messagebox.showinfo("Balance", f"Your balance is: {balance[0]}")
    else:
        messagebox.showerror("Error", "Account not found.")

# Create GUI
root = tk.Tk()
root.title("Banking Application")

# Labels
tk.Label(root, text="Account ID:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Initial Balance:").grid(row=2, column=0, padx=5, pady=5)
tk.Label(root, text="Deposit Amount:").grid(row=3, column=0, padx=5, pady=5)
tk.Label(root, text="Withdraw Amount:").grid(row=4, column=0, padx=5, pady=5)

# Entry fields
account_id_entry = tk.Entry(root)
name_entry = tk.Entry(root)
initial_balance_entry = tk.Entry(root)
deposit_entry = tk.Entry(root)
withdraw_entry = tk.Entry(root)

account_id_entry.grid(row=0, column=1, padx=5, pady=5)
name_entry.grid(row=1, column=1, padx=5, pady=5)
initial_balance_entry.grid(row=2, column=1, padx=5, pady=5)
deposit_entry.grid(row=3, column=1, padx=5, pady=5)
withdraw_entry.grid(row=4, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Create Account", command=create_account).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")
tk.Button(root, text="Deposit", command=deposit).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")
tk.Button(root, text="Withdraw", command=withdraw).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")
tk.Button(root, text="Check Balance", command=check_balance).grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="we")

root.mainloop()

# Close the database connection
conn.close()
