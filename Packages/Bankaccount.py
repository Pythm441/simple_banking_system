import random

class BankAccount:
    def __init__(self, owner, balance, ID, password):
        self.owner = owner
        self.balance = balance
        self.ID = ID
        self.password = password
        if self.ID is None:
            self.ID = random.randint(1000000000, 9999999999)

    def to_dict(self):
        return {
            "owner": self.owner,
            "balance": self.balance,
            "ID": self.ID,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            owner=data["owner"],
            balance=data["balance"],
            ID=data["ID"],
            password=data.get("password")
        )

    def __str__(self):
        return f"Owner: {self.owner}, Balance: {self.balance}, ID: {self.ID}"

    def __repr__(self):
        return f"BankAccount(owner: {self.owner}, balance: {self.balance}, ID: {self.ID})"