import datetime

def calculate_savings_goal(price, target_date, monthly_income):
    
    today = datetime.date.today()
    remaining_months = (target_date.year - today.year) * 12 + (target_date.month - today.month)
    
    
    if remaining_months <= 0:
        raise ValueError("Target date must be in the future")
    
    
    savings_needed = price / remaining_months
    
    
    savings_percentage = (savings_needed / monthly_income) * 100
    
    return savings_needed, savings_percentage

def main():
    
    product_name = input("Enter the product name: ")
    price = float(input("Enter the price of the product: $"))
    target_date_str = input("Enter the target date (YYYY-MM-DD): ")
    target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").date()
    monthly_income = float(input("Enter your monthly income: $"))
    
    
    try:
        savings_goal, savings_percentage = calculate_savings_goal(price, target_date, monthly_income)
        print(f"To buy {product_name} by {target_date}, you need to save ${savings_goal:.2f} per month.")
        print(f"This represents {savings_percentage:.2f}% of your monthly income.")
    except ValueError as e:
        print(e)

if _name_ == "_main_":
    main()