import unittest
from unittest.mock import patch
from datetime import datetime

# Предполагаем, что функция get_time_for_greeting определена в файле greetings.py
from src.utils import get_time_for_greeting


class TestGetTimeForGreeting(unittest.TestCase):

    @patch("src.utils.datetime")
    def test_greetings(self, mock_datetime):
        # Тестируем утро
        mock_datetime.now.return_value.hour = 6
        self.assertEqual(get_time_for_greeting(), "Доброе утро")

        # Тестируем день
        mock_datetime.now.return_value.hour = 13
        self.assertEqual(get_time_for_greeting(), "Добрый дeнь")

        # Тестируем вечер
        mock_datetime.now.return_value.hour = 19
        self.assertEqual(get_time_for_greeting(), "Добрый вечер")

        # Тестируем ночь
        mock_datetime.now.return_value.hour = 23
        self.assertEqual(get_time_for_greeting(), "Добрый день")


if __name__ == "__main__":
    unittest.main()
