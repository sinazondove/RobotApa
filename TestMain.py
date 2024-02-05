import unittest
from unittest.mock import patch
from io import StringIO
from main import main

class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['yes', '9506051245089', 'no', 'no'])
    def test_existing_user_no_add_survivor(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
        output = fake_out.getvalue().strip()
        self.assertIn("Are you an existing user?", output)
        self.assertIn("Do you want to update your location?", output)
        self.assertIn("Would you like to Add yourself as a survivor?", output)
        self.assertNotIn("Enter your ID number:", output)

    @patch('builtins.input', side_effect=['yes', '9506051245089', 'yes', 'no', 'no'])
    def test_existing_user_update_location_no_update_infection_status(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
        output = fake_out.getvalue().strip()
        self.assertIn("Are you an existing user?", output)
        self.assertIn("Do you want to update your location?", output)
        self.assertIn("Do you want to update your infection status?", output)
        self.assertNotIn("Would you like to Add yourself as a survivor?", output)
        self.assertNotIn("Enter your ID number:", output)

    # Add more test cases to cover other scenarios...

if __name__ == '__main__':
    unittest.main()
