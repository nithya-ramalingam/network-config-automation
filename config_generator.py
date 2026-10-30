
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
INVENTORY_FILE = BASE_DIR / "inventory.yml"


def load_inventory():
    """Load and validate network device information from YAML."""
    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        inventory = yaml.safe_load(file)

    if not isinstance(inventory, dict):
        raise ValueError("Inventory must be a YAML dictionary.")

    devices = inventory.get("devices")

    if not isinstance(devices, list) or not devices:
        raise ValueError("Inventory must contain a non-empty 'devices' list.")

    device_names = set()

    for device in devices:
        if not isinstance(device, dict):
            raise ValueError("Every device must be a dictionary.")

        name = device.get("name")
        hostname = device.get("hostname")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every device must have a valid name.")

        if name in device_names:
            raise ValueError(f"Duplicate device name: {name}")

        device_names.add(name)

        if not isinstance(hostname, str) or not hostname.strip():
            raise ValueError(f"Device {name} must have a valid hostname.")

        vlans = device.get("vlans", [])
        interfaces = device.get("interfaces", [])

        if not isinstance(vlans, list):
            raise ValueError(f"VLANs for {name} must be a list.")

        if not isinstance(interfaces, list):
            raise ValueError(f"Interfaces for {name} must be a list.")

        for vlan in vlans:
            if not isinstance(vlan, dict):
                raise ValueError(f"Invalid VLAN entry in {name}.")

            vlan_id = vlan.get("id")

            if not isinstance(vlan_id, int) or isinstance(vlan_id, bool) or not 1 <= vlan_id <= 4094:
                raise ValueError(f"Invalid VLAN ID in {name}: {vlan_id}")

            if not isinstance(vlan.get("name"), str) or not vlan["name"].strip():
                raise ValueError(f"VLAN {vlan_id} in {name} must have a name.")

        for interface in interfaces:
            if not isinstance(interface, dict):
                raise ValueError(f"Invalid interface entry in {name}.")

            if not isinstance(interface.get("name"), str) or not interface["name"].strip():
                raise ValueError(f"Every interface in {name} must have a name.")

            access_vlan = interface.get("access_vlan")

            if access_vlan is not None:
                if (
                    not isinstance(access_vlan, int)
                    or isinstance(access_vlan, bool)
                    or not 1 <= access_vlan <= 4094
                ):
                    raise ValueError(
                        f"Invalid access VLAN on {interface['name']} in {name}."
                    )

    return devices


def generate_config(device):
    """Generate Cisco IOS configuration for one device."""
    if not device.get("name"):
        raise ValueError("Every device must have a name.")

    environment = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = environment.get_template("cisco_ios.j2")
    return template.render(device=device)


def generate_all():
    """Generate configurations for all validated devices."""
    devices = load_inventory()

    configurations = {}

    for device in devices:
        name = device["name"]
        configurations[name] = generate_config(device)

    return configurations


if __name__ == "__main__":
    for device_name, configuration in generate_all().items():
        print(f"\n{'=' * 50}")
        print(f"Configuration for {device_name}")
        print("=" * 50)
        print(configuration)
