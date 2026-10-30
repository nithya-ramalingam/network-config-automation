
import argparse
import os

from dotenv import load_dotenv
from netmiko import ConnectHandler

from config_generator import generate_all, load_inventory


load_dotenv()


def deploy_config(device, configuration):
    """Deploy configuration to an authorized network device."""

    password = os.getenv("NETWORK_PASSWORD")
    secret = os.getenv("NETWORK_SECRET", "")

    if not password:
        raise ValueError("NETWORK_PASSWORD is missing from the .env file.")

    username = os.getenv("NETWORK_USERNAME") or device.get("username")

    if not username:
        raise ValueError("Network username is missing.")

    connection_details = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": username,
        "password": password,
        "secret": secret,
    }

    commands = [
        line.strip()
        for line in configuration.splitlines()
        if line.strip() and line.strip().lower() != "end"
    ]

    with ConnectHandler(**connection_details) as connection:
        if secret:
            connection.enable()

        result = connection.send_config_set(commands)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Network configuration deployment tool"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Deploy configuration to an authorized network device"
    )

    args = parser.parse_args()

    try:
        devices = load_inventory()
        configurations = generate_all()

        for device in devices:
            device_name = device["name"]
            configuration = configurations[device_name]

            print(f"\nConfiguration for {device_name}")
            print("-" * 50)
            print(configuration)

            if not args.apply:
                print("\nDRY RUN: No network connection was made.")
                continue

            confirmation = input(
                f"\nType DEPLOY to apply configuration to {device_name}: "
            )

            if confirmation != "DEPLOY":
                print("Deployment cancelled.")
                continue

            try:
                result = deploy_config(device, configuration)
                print("\nDeployment result:")
                print(result)

            except Exception as error:
                print(f"\nDeployment failed: {error}")

    except (ValueError, KeyError, OSError) as error:
        print(f"\nConfiguration error: {error}")


if __name__ == "__main__":
    main()
