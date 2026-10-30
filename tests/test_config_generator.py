import unittest

from config_generator import generate_all


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


if __name__ == "__main__":
    unittest.main()