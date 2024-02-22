
import sqlite3
import os
import matplotlib.pyplot as plt

class Asset:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Liability:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PersonalFinanceDashboard:
    def __init__(self, conn):
        self.assets = []
        self.liabilities = []
        self.income = 0
        self.conn = conn
        self.create_tables()
        self.load_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                name TEXT,
                value REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS liabilities (
                name TEXT,
                value REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                amount REAL
            )
        ''')
        self.conn.commit()

    def load_data(self):
        self.load_assets()
        self.load_liabilities()
        self.load_income()

    def load_assets(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, value FROM assets')
        rows = cursor.fetchall()
        self.assets = [Asset(name, value) for name, value in rows]

    def load_liabilities(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, value FROM liabilities')
        rows = cursor.fetchall()
        self.liabilities = [Liability(name, value) for name, value in rows]

    def load_income(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT amount FROM income')
        row = cursor.fetchone()
        if row:
            self.income = row[0]

    def add_asset(self, asset):
        self.assets.append(asset)
        self.save_asset_to_db(asset)

    def add_liability(self, liability):
        self.liabilities.append(liability)
        self.save_liability_to_db(liability)

    def add_income(self, income):
        self.income += income
        self.save_income_to_db(income)

    def calculate_assets_total(self):
        return sum(asset.value for asset in self.assets)

    def calculate_liabilities_total(self):
        return sum(liability.value for liability in self.liabilities)

    def calculate_net_worth(self):
        return self.calculate_assets_total() - self.calculate_liabilities_total()

    def get_asset_allocation(self):
        asset_allocation = {}
        for asset in self.assets:
            asset_allocation[asset.name] = asset.value
        return asset_allocation

    def get_liability_distribution(self):
        liability_distribution = {}
        for liability in self.liabilities:
            liability_distribution[liability.name] = liability.value
        return liability_distribution

    def save_asset_to_db(self, asset):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO assets VALUES (?, ?)', (asset.name, asset.value))
        self.conn.commit()

    def save_liability_to_db(self, liability):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO liabilities VALUES (?, ?)', (liability.name, liability.value))
        self.conn.commit()

    def save_income_to_db(self, income):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO income VALUES (?)', (income,))
        self.conn.commit()

def add_assets(dashboard):
    while True:
        print("Add Asset:")
        name = input("Enter asset name: ")
        value = float(input("Enter asset value: "))
        dashboard.add_asset(Asset(name, value))
        choice = input("Do you want to add another asset? (yes/no): ")
        if choice.lower() != 'yes':
            break

def add_liabilities(dashboard):
    while True:
        print("Add Liability:")
        name = input("Enter liability name: ")
        value = float(input("Enter liability value: "))
        dashboard.add_liability(Liability(name, value))
        choice = input("Do you want to add another liability? (yes/no): ")
        if choice.lower() != 'yes':
            break

def add_income(dashboard):
    while True:
        income = float(input("Enter income amount: "))
        dashboard.add_income(income)
        choice = input("Do you want to add more income? (yes/no): ")
        if choice.lower() != 'yes':
            break

def display_dashboard(dashboard):
    print("\nPersonal Finance Dashboard")
    print("Total Assets:", dashboard.calculate_assets_total())
    print("Total Liabilities:", dashboard.calculate_liabilities_total())
    print("Net Worth:", dashboard.calculate_net_worth())
    print("Income:", dashboard.income)

    # Displaying pie chart of asset allocation
    asset_allocation = dashboard.get_asset_allocation()
    labels = asset_allocation.keys()
    sizes = asset_allocation.values()
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Asset Allocation')
    plt.axis('equal')
    plt.show()

    # Displaying pie chart of liability distribution
    liability_distribution = dashboard.get_liability_distribution()
    labels = liability_distribution.keys()
    sizes = liability_distribution.values()
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Liability Distribution')
    plt.axis('equal')
    plt.show()

# Main function
def main():
    conn = sqlite3.connect('finance_data.db')
    dashboard = PersonalFinanceDashboard(conn)

    while True:
        print("\n1. Add Assets")
        print("2. Add Liabilities")
        print("3. Add Income")
        print("4. Display Dashboard")
        print("5. Save and Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_assets(dashboard)
        elif choice == '2':
            add_liabilities(dashboard)
        elif choice == '3':
            add_income(dashboard)
        elif choice == '4':
            display_dashboard(dashboard)
        elif choice == '5':
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()