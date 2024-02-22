
import sqlite3


class Reminder:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

    def __str__(self):
        return f"Reminder: {self.description}, Amount: ${self.amount:.2f}"


class ReminderManager:
    def __init__(self, conn):
        self.conn = conn
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                name TEXT PRIMARY KEY,
                amount REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS debts (
                person TEXT PRIMARY KEY,
                amount REAL
            )
        ''')
        self.conn.commit()

    def create_bill_reminders(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, amount FROM bills')
        bills = dict(cursor.fetchall())
        return [Reminder(f"Pay {bill} bill", amount) for bill, amount in bills.items()]

    def create_debt_reminders(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT person, amount FROM debts')
        debts = dict(cursor.fetchall())
        return [Reminder(f"Collect ${amount:.2f} from {person}", amount) for person, amount in debts.items()]

    def save_bill(self, bill_name, bill_amount):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO bills VALUES (?, ?)', (bill_name, bill_amount))
        self.conn.commit()

    def save_debt(self, person_name, debt_amount):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO debts VALUES (?, ?)', (person_name, debt_amount))
        self.conn.commit()


def input_bill(reminder_manager):
    bill_name = input("Enter the name of the bill: ")
    bill_amount = float(input("Enter the amount of the bill: "))
    reminder_manager.save_bill(bill_name, bill_amount)


def input_debt(reminder_manager):
    person_name = input("Enter the name of the person: ")
    debt_amount = float(input("Enter the amount they owe: "))
    reminder_manager.save_debt(person_name, debt_amount)


def main():
    conn = sqlite3.connect('reminders.db')
    reminder_manager = ReminderManager(conn)

    # Menu for user input
    while True:
        print("\nMenu:")
        print("1. Input a new bill")
        print("2. Input a new owing")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            input_bill(reminder_manager)
        elif choice == "2":
            input_debt(reminder_manager)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please choose again.")

    # Create and display reminders
    bill_reminders = reminder_manager.create_bill_reminders()
    debt_reminders = reminder_manager.create_debt_reminders()

    print("\nBills Reminders:")
    for reminder in bill_reminders:
        print(reminder)

    print("\nOwings Reminders:")
    for reminder in debt_reminders:
        print(reminder)

    conn.close()


if __name__ == "__main__":
    main()