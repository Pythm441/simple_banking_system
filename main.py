from Packages.Bankaccount import BankAccount
from Packages.BankFunctions import BankFunctions, CustomerFunctions
import json
from pathlib import Path
import random

DATA_FILE = Path("accounts.json")


def main():
    accounts = []

    # Load accounts from JSON
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            for acc_data in data:
                accounts.append(BankAccount.from_dict(acc_data))
            print("Accounts loaded from file.")  # successfully loaded
    except (FileNotFoundError, json.JSONDecodeError):
        print("No accounts found or file is empty. Starting with an empty list.")

    # Create instances of function classes
    bank_functions = BankFunctions()
    customer_functions = CustomerFunctions()

    # Login function
    def login(accounts):
        acc_id = int(input("Enter account ID: "))
        account = next((a for a in accounts if a.ID == acc_id), None)
        if not account:
            print("Account not found.")
            return None
        password = input("Enter account password: ")
        if account.password == password:
            print("Login successful!")
            print("Welcome, " + account.owner + "!")
            return account
        else:
            print("Login failed! Incorrect password.")
            return None
        

    print("Welcome to the Simple Bank System!")
    print("Please log in to continue.")

    logged_in_account = login(accounts)
    while logged_in_account:
        
        print("\n=== Simple Bank System ===")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View All Accounts")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            owner = input("Enter account owner name: ").strip()
            balance = float(input("Enter initial balance: "))
            password = input("Set account password: ")
            # Generate a random 10-digit ID
            ID = random.randint(10**9, 10**10 - 1)
            account = bank_functions.create_account(owner, balance, ID, password)
            accounts.append(account)
            try:
                with open(DATA_FILE, "w") as file:
                    json.dump([acc.to_dict() for acc in accounts], file, indent=4)
            except Exception as e:
                print(f"Error saving account data: {e}")
            print(f"Account created! ID: {account.ID}")

        elif choice == "2":
            amount = float(input("Enter deposit amount: "))
            customer_functions.deposit(logged_in_account, amount)

        elif choice == "3":
            amount = float(input("Enter withdrawal amount: "))
            customer_functions.withdraw(logged_in_account, amount)

        elif choice == "4":
            to_id = int(input("Enter TO account ID: "))
            to_account = next((a for a in accounts if a.ID == to_id), None)
            if to_account:
                amount = float(input("Enter transfer amount: "))
                customer_functions.transfer(logged_in_account, to_account, amount)
            else:
                print("Destination account not found!")

        elif choice == "5":
            bank_functions.view_all_accounts(accounts)

        elif choice == "6":
            # Save before exiting
            accounts_dict = [acc.to_dict() for acc in accounts]
            with open(DATA_FILE, "w") as file:
                json.dump(accounts_dict, file, indent=4)
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
