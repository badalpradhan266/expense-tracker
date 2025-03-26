import json
import os
from datetime import datetime, timedelta

class ExpenseTracker:
    def __init__(self, filename='expenses.json'):
        """
        Initialize the expense tracker with a JSON file for persistent storage.
        
        Args:
            filename (str): Name of the file to store expenses
        """
        self.filename = filename
        self.expenses = self.load_expenses()
        self.categories = self.get_unique_categories()
    
    def load_expenses(self):
        """
        Load expenses from JSON file or create a new list if file doesn't exist.
        
        Returns:
            list: List of expense entries
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_expenses(self):
        """
        Save expenses to JSON file.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.expenses, file, indent=4)
    
    def add_expense(self, amount, category, description, date=None):
        """
        Add a new expense to the tracker.
        
        Args:
            amount (float): Cost of the expense
            category (str): Category of the expense
            description (str): Description of the expense
            date (str, optional): Date of the expense in YYYY-MM-DD format
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        expense = {
            'id': len(self.expenses) + 1,
            'amount': round(float(amount), 2),
            'category': category.strip().capitalize(),
            'description': description.strip(),
            'date': date
        }
        
        self.expenses.append(expense)
        self.save_expenses()
        self.categories = self.get_unique_categories()
        print(f"Expense of ${amount} in {category} added successfully!")
    
    def get_unique_categories(self):
        """
        Get unique expense categories.
        
        Returns:
            set: Unique expense categories
        """
        return set(expense['category'] for expense in self.expenses)
    
    def view_expenses(self, filter_category=None, start_date=None, end_date=None):
        """
        View expenses with optional filtering.
        
        Args:
            filter_category (str, optional): Filter expenses by category
            start_date (str, optional): Start date for filtering in YYYY-MM-DD format
            end_date (str, optional): End date for filtering in YYYY-MM-DD format
        
        Returns:
            list: Filtered list of expenses
        """
        filtered_expenses = self.expenses.copy()
        
        if filter_category:
            filtered_expenses = [
                expense for expense in filtered_expenses 
                if expense['category'].lower() == filter_category.lower()
            ]
        
        if start_date:
            filtered_expenses = [
                expense for expense in filtered_expenses 
                if expense['date'] >= start_date
            ]
        
        if end_date:
            filtered_expenses = [
                expense for expense in filtered_expenses 
                if expense['date'] <= end_date
            ]
        
        return sorted(filtered_expenses, key=lambda x: x['date'], reverse=True)
    
    def calculate_total_expenses(self, filter_category=None, start_date=None, end_date=None):
        """
        Calculate total expenses with optional filtering.
        
        Args:
            filter_category (str, optional): Filter expenses by category
            start_date (str, optional): Start date for filtering in YYYY-MM-DD format
            end_date (str, optional): End date for filtering in YYYY-MM-DD format
        
        Returns:
            float: Total expenses
        """
        filtered_expenses = self.view_expenses(filter_category, start_date, end_date)
        return round(sum(expense['amount'] for expense in filtered_expenses), 2)
    
    def generate_expense_report(self, start_date=None, end_date=None):
        """
        Generate a detailed expense report by category.
        
        Args:
            start_date (str, optional): Start date for report in YYYY-MM-DD format
            end_date (str, optional): End date for report in YYYY-MM-DD format
        
        Returns:
            dict: Expense report with total spending per category
        """
        filtered_expenses = self.view_expenses(start_date=start_date, end_date=end_date)
        
        report = {}
        for expense in filtered_expenses:
            category = expense['category']
            amount = expense['amount']
            report[category] = report.get(category, 0) + amount
        
        return {k: round(v, 2) for k, v in sorted(report.items(), key=lambda x: x[1], reverse=True)}
    
    def delete_expense(self, expense_id):
        """
        Delete an expense by its ID.
        
        Args:
            expense_id (int): ID of the expense to delete
        """
        for index, expense in enumerate(self.expenses):
            if expense['id'] == expense_id:
                del self.expenses[index]
                self.save_expenses()
                print(f"Expense with ID {expense_id} deleted successfully!")
                return
        
        print(f"No expense found with ID {expense_id}")
    
    def print_expenses(self, expenses):
        """
        Print expenses in a formatted manner.
        
        Args:
            expenses (list): List of expenses to print
        """
        if not expenses:
            print("No expenses found.")
            return
        
        print("\n{:<5} {:<15} {:<15} {:<20} {:<10}".format("ID", "Amount", "Category", "Description", "Date"))
        print("-" * 65)
        
        for expense in expenses:
            print("{:<5} ${:<14.2f} {:<15} {:<20} {}".format(
                expense['id'], 
                expense['amount'], 
                expense['category'], 
                expense['description'][:20], 
                expense['date']
            ))

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. View Expenses by Date Range")
        print("5. Generate Expense Report")
        print("6. Calculate Total Expenses")
        print("7. Delete Expense")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        try:
            if choice == '1':
                amount = float(input("Enter expense amount: "))
                category = input("Enter expense category: ")
                description = input("Enter expense description: ")
                date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
                tracker.add_expense(amount, category, description, date or None)
            
            elif choice == '2':
                tracker.print_expenses(tracker.view_expenses())
            
            elif choice == '3':
                category = input("Enter category to filter: ")
                tracker.print_expenses(tracker.view_expenses(filter_category=category))
            
            elif choice == '4':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                tracker.print_expenses(tracker.view_expenses(start_date=start_date, end_date=end_date))
            
            elif choice == '5':
                start_date = input("Enter start date (YYYY-MM-DD) or press Enter: ")
                end_date = input("Enter end date (YYYY-MM-DD) or press Enter: ")
                report = tracker.generate_expense_report(start_date or None, end_date or None)
                
                print("\n--- Expense Report ---")
                for category, total in report.items():
                    print(f"{category}: ${total}")
            
            elif choice == '6':
                category = input("Enter category (or press Enter for all): ")
                start_date = input("Enter start date (YYYY-MM-DD) or press Enter: ")
                end_date = input("Enter end date (YYYY-MM-DD) or press Enter: ")
                total = tracker.calculate_total_expenses(
                    category or None, 
                    start_date or None, 
                    end_date or None
                )
                print(f"\nTotal Expenses: ${total}")
            
            elif choice == '7':
                expense_id = int(input("Enter expense ID to delete: "))
                tracker.delete_expense(expense_id)
            
            elif choice == '8':
                print("Thank you for using Expense Tracker. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"Error: {e}. Please enter valid input.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()