#Author - Shakeel Gadhafi
#Uow ID - w2083054
#IIT ID - 20230343
#Semester 01 Computer Science
#SD 1 2nd CW

import json
import datetime

# Global dictionary to store transactions
transactions = {}

# Function to load transactions from file
def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save transactions to file
def save_transactions(transactions):
    formatted_transactions = {}
    for category, category_transactions in transactions.items():
        formatted_transactions[category] = [{"amount": transaction["Amount"], "date": transaction["Date"]} for transaction in category_transactions.values()]

    with open("transactions.json", "w") as file:
        json.dump(formatted_transactions, file, indent=4)

# Function to add a new transaction
def add_transaction(transactions):
    while True:
        try:
            amount = float(input("Amount: "))  # Prompt user for amount input
            if amount >= 0:  # Check if amount is non-negative
                break  # Break if input is valid
            else:
                print("Amount cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")  # Handle invalid input exceptions

    while True:
        category = input("Category: ")
        if category:  # Check if category is not empty
            break
        else:
            print("Category cannot be empty.")  # Prompt user for category input

    while True:
        transaction_type = input("Income/Expense: ").capitalize()
        if transaction_type == "Income" or transaction_type == "Expense":  # Check if input is either "Income" or "Expense"
            break
        else:
            print("Invalid input. Please enter 'Income' or 'Expense'.")  # Prompt user for type input

    while True:
        date_str = input("Date (YYYY-MM-DD): ")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()  # Parse input as date object
            break  # Break out of the loop if input is valid
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")  # Handle invalid date format

    # Generate a unique transaction ID starting from 1
    transaction_id = str(len(transactions) + 1)
    
    # Once all inputs are valid, add the transaction to the dictionary
    transaction = {"Amount": amount, "Category": category, "Type": transaction_type, "Date": str(date)}
    
    if category not in transactions:
        transactions[category] = {transaction_id: transaction}
    else:
        transactions[category][transaction_id] = transaction
    
    save_transactions(transactions)
    print("Transaction added!!")  # Confirmation message
    
# Function to view all transactions
def view_transactions(transactions):
    if transactions:
        print("Transactions:")
        for category, category_transactions in transactions.items():
            print(f"Category: {category}")
            for transaction_id, transaction in category_transactions.items():
                print(f"Transaction ID: {transaction_id}, Amount: {transaction['Amount']}, Type: {transaction['Type']}, Date: {transaction['Date']}")
    else:
        print("No transactions to display.")

# Function to update an existing transaction
def update_transaction(transactions):
    if not transactions:
        print("No transactions to update.")
        return

    view_transactions(transactions)
    transaction_id = input("Enter the transaction ID to update: ")
    
    for category, category_transactions in transactions.items():
        if transaction_id in category_transactions:
            transaction = category_transactions[transaction_id]
            print("Enter new transaction details:")
            amount_input = input(f"New amount ({transaction['Amount']}): ")
            amount = float(amount_input) if amount_input else transaction['Amount']
            category_input = input(f"New category ({transaction['Category']}): ")
            category = category_input if category_input else transaction['Category']
            type_input = input(f"New type (Income/Expense) ({transaction['Type']}): ").capitalize()
            transaction_type = type_input if type_input else transaction['Type']
            date_input = input(f"New date (YYYY-MM-DD) ({transaction['Date']}): ")
            date = date_input if date_input else transaction['Date']
            
            # Update the transaction with the new details
            if category not in transactions:
                transactions[category] = {}
            transactions[category][transaction_id] = {"Amount": amount, "Category": category, "Type": transaction_type, "Date": date}
            print("Transaction updated.")
            save_transactions(transactions)  # Save transactions after updating
            break
    else:
        print("Invalid transaction ID.")
        
# Function to delete a transaction
def delete_transaction(transactions):
    if not transactions:
        print("No transactions to delete.")
        return

    view_transactions(transactions)
    transaction_id = input("Enter the transaction ID to delete: ")

    for category, category_transactions in transactions.items():
        if transaction_id in category_transactions:
            del transactions[category][transaction_id]
            print("Transaction deleted.")
            save_transactions(transactions)  # Save transactions after deletion
            return

    print("Invalid transaction ID.")

# Function to read bulk transactions from file
def read_bulk_transactions_from_file(filename):
    try:
        with open(filename, "r") as file:
            transactions = {}  # Initialize an empty dictionary to store transactions
            for line in file:
                # Parse the line as JSON to extract transaction data
                transaction_data = json.loads(line)
                # Extract transaction details from the parsed JSON data
                amount = transaction_data.get("Amount", 0)
                category = transaction_data.get("Category", "")
                date = transaction_data.get("Date", "")

                # Create a transaction entry
                transaction = {"amount": amount, "date": date}

                # Add the transaction to the corresponding category list
                if category not in transactions:
                    transactions[category] = [transaction]
                else:
                    transactions[category].append(transaction)

            return transactions

    except FileNotFoundError:
        print("File not found.")
        return {}
# Function to display summary of transactions
def display_summary(transactions):
    total_income = 0
    total_expense = 0

    # Calculate total income and expenses
    for category, category_transactions in transactions.items():
        for transaction in category_transactions.values():
            if transaction["Type"] == "Income":
                total_income += transaction["Amount"]
            else:
                total_expense += transaction["Amount"]

    # Calculate balance
    balance = total_income - total_expense

    # Print summary
    print("Summary:")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expense}")
    print(f"Balance: {balance}")

# Function to display the main menu and handle user choices
def main_menu():
    global transactions
    transactions = load_transactions()  # Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction(transactions)
        elif choice == '2':
            view_transactions(transactions)
        elif choice == '3':
            update_transaction(transactions)
        elif choice == '4':
            delete_transaction(transactions)
        elif choice == '5':
            display_summary(transactions)
        elif choice == '6':
            save_transactions(transactions)
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
    
# if you are paid to do this assignment please delete this line of commen
