import json
import unittest
from unittest.mock import patch

import pandas as pd

# Предполагаем, что функция analyze_cashback определена в файле cashback_analysis.py
from src.services import analyze_cashback


class TestAnalyzeCashback(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_analyze_cashback_success(self, mock_read_excel):
        # Подготовка тестовых данных
        test_data = {
            "Дата платежа": ["01.01.2023", "15.01.2023", "20.01.2023"],
            "Категория": ["Еда", "Техника", "Еда"],
            "Кэшбэк": [100, 200, 150],
        }
        mock_df = pd.DataFrame(test_data)
        mock_read_excel.return_value = mock_df

        # Запуск функции
        response = analyze_cashback(2023, 1, "../data/operations.xlsx")

        # Проверка результата
        expected_response = {"year": 2023, "month": 1, "cashback_by_category": {"Еда": 250, "Техника": 200}}
        self.assertEqual(json.loads(response), expected_response)

    @patch("pandas.read_excel")
    def test_analyze_cashback_file_read_error(self, mock_read_excel):
        mock_read_excel.side_effect = Exception("File not found")

        response = analyze_cashback(2023, 1, "../data/operations.xlsx")

        expected_response = {"error": "Ошибка при чтении файла Excel"}
        self.assertEqual(json.loads(response), expected_response)

    @patch("pandas.read_excel")
    def test_analyze_cashback_missing_columns(self, mock_read_excel):
        test_data = {"Дата платежа": ["01.01.2023", "15.01.2023"], "Кэшбэк": [100, 200]}
        mock_df = pd.DataFrame(test_data)
        mock_read_excel.return_value = mock_df

        response = analyze_cashback(2023, 1, "../data/operations.xlsx")

        expected_response = {"error": "Отсутствуют необходимые колонки в Excel файле."}
        self.assertEqual(json.loads(response), expected_response)

    @patch("pandas.read_excel")
    def test_analyze_cashback_date_conversion_error(self, mock_read_excel):
        test_data = {
            "Дата платежа": ["invalid_date", "15.01.2023"],
            "Категория": ["Еда", "Техника"],
            "Кэшбэк": [100, 200],
        }
        mock_df = pd.DataFrame(test_data)
        mock_read_excel.return_value = mock_df

        response = analyze_cashback(2023, 1, "../data/operations.xlsx")

        expected_response = {"error": "Ошибка при преобразовании дат."}
        self.assertEqual(json.loads(response), expected_response)


if __name__ == "__main__":
    unittest.main()
