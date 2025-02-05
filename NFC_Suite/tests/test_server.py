import unittest
import requests

class TestServerEndpoints(unittest.TestCase):
    def test_get_logs(self):
        """Test the /nfc/logs endpoint."""
        response = requests.get("http://localhost:5000/nfc/logs")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_execute_apdu(self):
        """Test the /execute_apdu endpoint."""
        payload = {
            "protocol": "emv",
            "apdu": "00A404000E325041592E5359532E4444463031"
        }
        response = requests.post("http://localhost:5000/execute_apdu", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

if __name__ == "__main__":
    unittest.main()
