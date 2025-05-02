import unittest
import pandas as pd
from io import BytesIO
from datetime import datetime
import json

from src.reports import get_expenses_by_category

# Assuming the function get_expenses_by_category is imported from your module
# from your_module import get_expenses_by_category


class TestGetExpensesByCategory(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame to simulate the Excel file
        data = {
            "Дата операции": ["2023-01-15", "2023-02-10", "2023-03-05", "2023-03-20"],
            "Категория": ["Food", "Transport", "Food", "Transport"],
            "Сумма операции": [100, 50, 150, 75],
        }
        self.df = pd.DataFrame(data)

        # Save the DataFrame to a BytesIO object to simulate an Excel file
        self.excel_file = BytesIO()
        self.df.to_excel(self.excel_file, sheet_name="Отчет по операциям", index=False)
        self.excel_file.seek(0)  # Move to the beginning of the BytesIO object

    def test_get_expenses_by_category(self):
        # Define the parameters for the test
        category = "Food"
        reference_date = "2023-03-31"

        # Call the function
        result = get_expenses_by_category(self.excel_file, category, reference_date)

        # Convert the result back from JSON
        result_dict = json.loads(result)

        # Check if the total expenses are correct
        expected_total_expenses = 250  # 100 + 150
        self.assertEqual(result_dict["total_expenses"], expected_total_expenses)

        # Check if the transactions list is correct
        expected_transactions = [
            {"Дата операции": "2023-01-15", "Категория": "Food", "Сумма операции": 100},
            {"Дата операции": "2023-03-05", "Категория": "Food", "Сумма операции": 150},
        ]
        self.assertEqual(result_dict["transactions"], expected_transactions)

    def test_get_expenses_by_category_no_data(self):
        # Test with a category that has no expenses
        category = "Entertainment"
        reference_date = "2023-03-31"

        # Call the function
        result = get_expenses_by_category(self.excel_file, category, reference_date)

        # Convert the result back from JSON
        result_dict = json.loads(result)

        # Check if the total expenses are zero
        expected_total_expenses = 0
        self.assertEqual(result_dict["total_expenses"], expected_total_expenses)
        self.assertEqual(result_dict["transactions"], [])

    def test_get_expenses_by_category_invalid_date(self):
        # Test with an invalid reference date format
        category = "Food"
        reference_date = "invalid-date"

        # Call the function
        result = get_expenses_by_category(self.excel_file, category, reference_date)

        # Convert the result back from JSON
        result_dict = json.loads(result)

        # Check if an error is returned
        self.assertIn("error", result_dict)

    def tearDown(self):
        # Clean up any resources if needed
        pass


if __name__ == "__main__":
    unittest.main()
