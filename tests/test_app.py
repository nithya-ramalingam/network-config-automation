
import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_devices_api(self):
        response = self.client.get("/api/devices")
        self.assertEqual(response.status_code, 200)

    def test_device_config_api(self):
        response = self.client.get("/api/config/SW1")
        self.assertEqual(response.status_code, 200)

    def test_unknown_device_returns_404(self):
        response = self.client.get("/api/config/SW99")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
