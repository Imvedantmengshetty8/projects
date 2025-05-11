import json
import os
import time

DATA_FILE = 'users.json'

class User:
    def __init__(self, username, pin, balance):
        self.username = username
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def check_pin(self, pin_input):
        return self.pin == pin_input

    def withdraw(self, amount):
        if amount % 10 != 0:
            return "Amount must be in multiples of 10"
        if amount > self.balance:
            return "Insufficient balance"
        self.balance -= amount
        self.transaction_history.append(f"Withdrew €{amount} on {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return f"Withdrawal successful. New balance: €{self.balance}"

    def deposit(self, amount):
        if amount % 10 != 0:
            return "Amount must be in multiples of 10"
        self.balance += amount
        self.transaction_history.append(f"Deposited €{amount} on {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return f"Deposit successful. New balance: €{self.balance}"

    def change_pin(self, new_pin):
        self.pin = new_pin
        self.transaction_history.append(f"Changed PIN on {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def view_transaction_history(self):
        if not self.transaction_history:
            return "No transactions found."
        return "\n".join(self.transaction_history)

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return {u: User(u, d['pin'], d['balance']) for u, d in data.items()}

def save_users(users):
    data = {u.username: {"pin": u.pin, "balance": u.balance} for u in users.values()}
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_user(users):
    username = input("Enter a new username: ").lower()
    if username in users:
        print("Username already exists!")
        return
    pin = input("Enter a 4-digit PIN: ")
    while not pin.isdigit() or len(pin) != 4:
        print("Invalid PIN. Please enter a 4-digit number.")
        pin = input("Enter a 4-digit PIN: ")
    users[username] = User(username, pin, 0)
    save_users(users)
    print("User created successfully!")

def main():
    users = load_users()
    print("=== Welcome to Python ATM ===")

    while True:
        print("\nChoose an option:")
        print("1. Login")
        print("2. Create a new user")
        print("3. Quit")
        choice = input("Select (1-3): ")

        if choice == '1':
            username = input("Enter username: ").lower()
            if username not in users:
                print("User not found.")
                continue

            user = users[username]
            attempts = 0
            while attempts < 3:
                pin = input("Enter your 4-digit PIN: ")
                if user.check_pin(pin):
                    break
                else:
                    attempts += 1
                    print("Invalid PIN.")
            if attempts == 3:
                print("Too many failed attempts. Exiting.")
                continue

            print(f"\nWelcome, {user.username}!")

            while True:
                print("\nChoose an option:")
                print("1. View Balance")
                print("2. Withdraw")
                print("3. Deposit")
                print("4. Change PIN")
                print("5. View Transaction History")
                print("6. Quit")
                choice = input("Select (1-6): ")

                if choice == '1':
                    print(f"Current balance: €{user.balance}")
                elif choice == '2':
                    try:
                        amt = int(input("Enter amount to withdraw: "))
                        print(user.withdraw(amt))
                    except ValueError:
                        print("Invalid amount.")
                elif choice == '3':
                    try:
                        amt = int(input("Enter amount to deposit: "))
                        print(user.deposit(amt))
                    except ValueError:
                        print("Invalid amount.")
                elif choice == '4':
                    new_pin = input("Enter new 4-digit PIN: ")
                    if new_pin.isdigit() and len(new_pin) == 4 and new_pin != user.pin:
                        confirm = input("Confirm new PIN: ")
                        if confirm == new_pin:
                            user.change_pin(new_pin)
                            print("PIN successfully changed.")
                        else:
                            print("PIN mismatch.")
                    else:
                        print("Invalid PIN format or same as old.")
                elif choice == '5':
                    print("\nTransaction History:")
                    print(user.view_transaction_history())
                elif choice == '6':
                    break
                else:
                    print("Invalid option.")

            save_users(users)
            print("Thank you for using Python ATM!")

        elif choice == '2':
            create_user(users)

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()
