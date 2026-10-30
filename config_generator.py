from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
INVENTORY_FILE = BASE_DIR / "inventory.yml"


def load_inventory():
    """Load network device information from the YAML inventory."""
    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        inventory = yaml.safe_load(file)

    if not isinstance(inventory, dict) or "devices" not in inventory:
        raise ValueError("Inventory must contain a 'devices' section.")

    return inventory["devices"]


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
    """Generate configurations for all devices in the inventory."""
    devices = load_inventory()

    configurations = {}

    for device in devices:
        name = device["name"]

        if name in configurations:
            raise ValueError(f"Duplicate device name: {name}")

        configurations[name] = generate_config(device)

    return configurations


if __name__ == "__main__":
    for device_name, configuration in generate_all().items():
        print(f"\n{'=' * 50}")
        print(f"Configuration for {device_name}")
        print("=" * 50)
        print(configuration)