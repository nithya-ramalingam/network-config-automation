
import unittest
from unittest.mock import patch

from config_generator import generate_all, load_inventory


class TestConfigGenerator(unittest.TestCase):

    def test_device_configuration_is_generated(self):
        configurations = generate_all()
        self.assertIn("SW1", configurations)

    def test_hostname_is_generated(self):
        configurations = generate_all()
        self.assertIn("hostname SW1", configurations["SW1"])

    def test_vlan_configuration_is_generated(self):
        configurations = generate_all()
        self.assertIn("vlan 10", configurations["SW1"])
        self.assertIn("name USERS", configurations["SW1"])

    def test_interface_configuration_is_generated(self):
        configurations = generate_all()
        self.assertIn(
            "interface GigabitEthernet0/1",
            configurations["SW1"]
        )

    def test_invalid_vlan_id_is_rejected(self):
        inventory = {
            "devices": [{
                "name": "SW1",
                "hostname": "SW1",
                "vlans": [{"id": 5000, "name": "INVALID"}],
                "interfaces": []
            }]
        }

        with patch("config_generator.yaml.safe_load", return_value=inventory):
            with self.assertRaises(ValueError):
                load_inventory()

    def test_missing_hostname_is_rejected(self):
        inventory = {
            "devices": [{
                "name": "SW1",
                "vlans": [],
                "interfaces": []
            }]
        }

        with patch("config_generator.yaml.safe_load", return_value=inventory):
            with self.assertRaises(ValueError):
                load_inventory()

    def test_duplicate_device_names_are_rejected(self):
        inventory = {
            "devices": [
                {"name": "SW1", "hostname": "SW1",
                 "vlans": [], "interfaces": []},
                {"name": "SW1", "hostname": "SW1",
                 "vlans": [], "interfaces": []}
            ]
        }

        with patch("config_generator.yaml.safe_load", return_value=inventory):
            with self.assertRaises(ValueError):
                load_inventory()

    def test_missing_device_name_is_rejected(self):
        inventory = {
            "devices": [{
                "hostname": "SW1",
                "vlans": [],
                "interfaces": []
            }]
        }

        with patch("config_generator.yaml.safe_load", return_value=inventory):
            with self.assertRaises(ValueError):
                load_inventory()


if __name__ == "__main__":
    unittest.main()
