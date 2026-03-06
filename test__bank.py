import unittest
from unittest.mock import patch, MagicMock
import json
import random

# ── Minimal stubs so tests run without the full Packages folder ──────────────

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
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            owner=data["owner"],
            balance=data["balance"],
            ID=data["ID"],
            password=data.get("password"),
        )

    def __str__(self):
        return f"Owner: {self.owner}, Balance: {self.balance}, ID: {self.ID}"

    def __repr__(self):
        return f"BankAccount(owner: {self.owner}, balance: {self.balance}, ID: {self.ID})"


class CustomerFunctions:
    def deposit(self, account, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        account.balance += amount
        print(f"Deposited {amount}. New balance: {account.balance}")

    def withdraw(self, account, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > account.balance:
            print("Insufficient funds.")
            return
        account.balance -= amount
        print(f"Withdrew {amount}. New balance: {account.balance}")

    def transfer(self, from_account, to_account, amount):
        if amount <= 0:
            print("Transfer amount must be positive.")
            return
        if amount > from_account.balance:
            print("Insufficient funds.")
            return
        from_account.balance -= amount
        to_account.balance += amount
        print(f"Transferred {amount} to {to_account.owner}.")


class BankFunctions:
    def create_account(self, owner, balance, ID, password):
        return BankAccount(owner, balance, ID, password)

    def view_all_accounts(self, accounts):
        for acc in accounts:
            print(acc)


# ── Tests ────────────────────────────────────────────────────────────────────

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", 1000.0, 1234567890, "pass123")

    # --- Construction ---
    def test_account_creation(self):
        self.assertEqual(self.account.owner, "Alice")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.ID, 1234567890)
        self.assertEqual(self.account.password, "pass123")

    def test_auto_generate_id_when_none(self):
        acc = BankAccount("Bob", 500.0, None, "secret")
        self.assertIsNotNone(acc.ID)
        self.assertGreaterEqual(acc.ID, 1000000000)
        self.assertLessEqual(acc.ID, 9999999999)

    # --- Serialisation ---
    def test_to_dict(self):
        d = self.account.to_dict()
        self.assertEqual(d["owner"], "Alice")
        self.assertEqual(d["balance"], 1000.0)
        self.assertEqual(d["ID"], 1234567890)
        self.assertEqual(d["password"], "pass123")

    def test_from_dict(self):
        d = {"owner": "Alice", "balance": 1000.0, "ID": 1234567890, "password": "pass123"}
        acc = BankAccount.from_dict(d)
        self.assertEqual(acc.owner, "Alice")
        self.assertEqual(acc.balance, 1000.0)
        self.assertEqual(acc.ID, 1234567890)

    def test_from_dict_missing_password(self):
        """from_dict should not crash when password key is absent."""
        d = {"owner": "Alice", "balance": 500.0, "ID": 1234567890}
        acc = BankAccount.from_dict(d)
        self.assertIsNone(acc.password)

    def test_round_trip_serialisation(self):
        """to_dict → from_dict should reproduce the original account."""
        restored = BankAccount.from_dict(self.account.to_dict())
        self.assertEqual(restored.owner, self.account.owner)
        self.assertEqual(restored.balance, self.account.balance)
        self.assertEqual(restored.ID, self.account.ID)
        self.assertEqual(restored.password, self.account.password)

    def test_json_round_trip(self):
        """Accounts should survive a JSON encode/decode cycle."""
        accounts = [self.account, BankAccount("Bob", 200.0, 9876543210, "abc")]
        json_str = json.dumps([a.to_dict() for a in accounts])
        loaded = [BankAccount.from_dict(d) for d in json.loads(json_str)]
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].owner, "Alice")
        self.assertEqual(loaded[1].owner, "Bob")

    # --- __str__ / __repr__ ---
    def test_str(self):
        self.assertIn("Alice", str(self.account))
        self.assertIn("1000.0", str(self.account))

    def test_repr(self):
        self.assertIn("BankAccount", repr(self.account))


class TestCustomerFunctions(unittest.TestCase):

    def setUp(self):
        self.cf = CustomerFunctions()
        self.alice = BankAccount("Alice", 1000.0, 1111111111, "pass")
        self.bob   = BankAccount("Bob",   500.0,  2222222222, "word")

    # --- Deposit ---
    def test_deposit_increases_balance(self):
        self.cf.deposit(self.alice, 200)
        self.assertEqual(self.alice.balance, 1200.0)

    def test_deposit_zero_does_not_change_balance(self):
        self.cf.deposit(self.alice, 0)
        self.assertEqual(self.alice.balance, 1000.0)

    def test_deposit_negative_does_not_change_balance(self):
        self.cf.deposit(self.alice, -50)
        self.assertEqual(self.alice.balance, 1000.0)

    # --- Withdraw ---
    def test_withdraw_decreases_balance(self):
        self.cf.withdraw(self.alice, 300)
        self.assertEqual(self.alice.balance, 700.0)

    def test_withdraw_exact_balance(self):
        self.cf.withdraw(self.alice, 1000.0)
        self.assertEqual(self.alice.balance, 0.0)

    def test_withdraw_insufficient_funds(self):
        self.cf.withdraw(self.alice, 5000)
        self.assertEqual(self.alice.balance, 1000.0)  # unchanged

    def test_withdraw_negative_does_not_change_balance(self):
        self.cf.withdraw(self.alice, -100)
        self.assertEqual(self.alice.balance, 1000.0)

    # --- Transfer ---
    def test_transfer_moves_funds(self):
        self.cf.transfer(self.alice, self.bob, 400)
        self.assertEqual(self.alice.balance, 600.0)
        self.assertEqual(self.bob.balance, 900.0)

    def test_transfer_insufficient_funds(self):
        self.cf.transfer(self.alice, self.bob, 9999)
        self.assertEqual(self.alice.balance, 1000.0)  # unchanged
        self.assertEqual(self.bob.balance, 500.0)     # unchanged

    def test_transfer_negative_amount(self):
        self.cf.transfer(self.alice, self.bob, -100)
        self.assertEqual(self.alice.balance, 1000.0)
        self.assertEqual(self.bob.balance, 500.0)

    def test_transfer_zero_amount(self):
        self.cf.transfer(self.alice, self.bob, 0)
        self.assertEqual(self.alice.balance, 1000.0)
        self.assertEqual(self.bob.balance, 500.0)


class TestBankFunctions(unittest.TestCase):

    def setUp(self):
        self.bf = BankFunctions()

    def test_create_account_returns_bank_account(self):
        acc = self.bf.create_account("Carol", 750.0, 3333333333, "pw")
        self.assertIsInstance(acc, BankAccount)
        self.assertEqual(acc.owner, "Carol")
        self.assertEqual(acc.balance, 750.0)

    def test_view_all_accounts_runs_without_error(self):
        accounts = [
            BankAccount("Alice", 1000.0, 1111111111, "p1"),
            BankAccount("Bob",   500.0,  2222222222, "p2"),
        ]
        # Should not raise
        try:
            self.bf.view_all_accounts(accounts)
        except Exception as e:
            self.fail(f"view_all_accounts raised an exception: {e}")

    def test_view_all_accounts_empty_list(self):
        try:
            self.bf.view_all_accounts([])
        except Exception as e:
            self.fail(f"view_all_accounts raised an exception on empty list: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)