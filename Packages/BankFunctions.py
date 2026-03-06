# The requested changes are to be made in main.py, not in this file.
# No changes are needed in this file (BankFunctions.py) as per instructions.
from Packages.Bankaccount import BankAccount

class CustomerFunctions:
    
    def deposit(account, amount):
        if amount < 0:
            print("Request DENIED. Invalid amount.")
        else: 
            account.balance += amount
    
    def withdraw(account, amount):
        if amount > account.balance or amount < 0:
            print("Request DENIED. Insufficient balance or invalid amount.")
        else: 
            account.balance -= amount
    
    def show_balance(account):
        print(f"Current balance: {account.balance}")
    @staticmethod
    def transfer(from_account, to_account, amount):
        if amount > from_account.balance or amount < 0:
            print("Request DENIED. Insufficient balance or invalid amount.")
        else:
            from_account.balance -= amount
            to_account.balance += amount
    
class BankFunctions:
    def create_account(self, owner, balance, id, password):
        password = input("Set a password for the account: ")
        return BankAccount(owner, balance, id, password)
    def view_account(self, account):
        print(account)
    def view_all_accounts(self, accounts):
        if not accounts:
            print("No accounts to display.")
        else:
            for account in accounts:
                print(account)
    def delete_account(self, accounts, account):
        if account in accounts:
            accounts.remove(account)