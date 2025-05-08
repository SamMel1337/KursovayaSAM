import json
import unittest
from unittest.mock import MagicMock, patch

# Replace 'cashback' with the actual name of your module
from src.views import mai_per, main_info, new_main


class TestCashbackFunctions(unittest.TestCase):

    @patch("src.views.get_time_for_greeting")
    @patch("src.views.get_data_time")
    @patch("src.views.get_path_and_period")
    @patch("src.views.get_card_with_spend")
    @patch("src.views.get_top_trans")
    @patch("src.views.get_ccurent")
    def test_main_info(
        self,
        mock_get_ccurent,
        mock_get_top_trans,
        mock_get_card_with_spend,
        mock_get_path_and_period,
        mock_get_data_time,
        mock_get_time_for_greeting,
    ):
        # Arrange
        mock_get_time_for_greeting.return_value = "Доброе утро!"
        mock_get_data_time.return_value = "2023-10-01"
        mock_get_path_and_period.return_value = MagicMock()  # Mock DataFrame or relevant structure
        mock_get_card_with_spend.return_value = ["Card 1", "Card 2"]
        mock_get_top_trans.return_value = [
            {"amount": 100, "category": "Food"},
            {"amount": 50, "category": "Transport"},
        ]
        mock_get_ccurent.return_value = {"currency": "RUB"}

        # Act
        result = main_info("2023-10-01 10:00")

        # Assert
        expected_data = {
            "greeting": "Доброе утро!",
            "cards": ["Card 1", "Card 2"],
            "top_trans": [{"amount": 100, "category": "Food"}, {"amount": 50, "category": "Transport"}],
            "ccurent": {"currency": "RUB"},
        }
        expected_json = json.dumps(expected_data, ensure_ascii=False, indent=4)
        self.assertEqual(result, expected_json)

    @patch("src.views.analyze_cashback")
    def test_mai_per(self, mock_analyze_cashback):
        # Arrange
        mock_analyze_cashback.return_value = {"cashback": "10%"}

        # Act
        result = mai_per(2023, 10, "../data/operations.xlsx")

        # Assert
        expected_data = {
            "ser": {"cashback": "10%"},
        }
        expected_json = json.dumps(expected_data, ensure_ascii=False, indent=4)
        self.assertEqual(result, expected_json)

    @patch("src.views.get_expenses_by_category")
    def test_new_main(self, mock_get_expenses_by_category):
        # Arrange
        mock_get_expenses_by_category.return_value = [100, 200, 300]

        # Act
        result = new_main(MagicMock(), "Food", "2023-10-01")

        # Assert
        expected_result = [100, 200, 300]
        self.assertEqual(result, expected_result)
