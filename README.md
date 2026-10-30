# Network Configuration Automation

## Project Overview

A Python-based network configuration automation tool that generates Cisco IOS configurations using YAML inventory files and Jinja2 templates. The application provides a Flask web interface and REST API to view generated configurations, with optional SSH-based deployment using Netmiko.

## Features

- YAML-based network device inventory
- Automated Cisco IOS configuration generation
- Jinja2 configuration templates
- Flask web interface
- REST API for device and configuration retrieval
- Netmiko SSH deployment support
- Safe dry-run mode by default
- Automated unit testing with Python unittest

## Technologies Used

- Python 3.11
- Flask
- Jinja2
- PyYAML
- Netmiko
- python-dotenv

## Project Architecture

YAML Inventory → Python Configuration Generator → Jinja2 Template → Cisco IOS Configuration

Flask provides the web interface and REST API. Netmiko supports optional deployment to authorized network devices.

## Project Structure

```text
network-config-automation/
│
├── templates/
│   └── cisco_ios.j2
│
├── tests/
│   └── test_config_generator.py
│
├── app.py
├── config_generator.py
├── deploy.py
├── inventory.yml
├── requirements.txt
└── README.md
```

## Installation

Clone the repository and open the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Generate Configurations

```bash
python config_generator.py
```

## Run the Web Application

```bash
python app.py
```

Open:

http://127.0.0.1:5000

## REST API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Web interface |
| `/api/devices` | List available devices |
| `/api/config/SW1` | Retrieve SW1 configuration |

## Run Automated Tests

```bash
python -m unittest discover -s tests -v
```

## Deployment

Dry-run mode (default):

```bash
python deploy.py
```

Optional deployment to an authorized lab device:

```bash
python deploy.py --apply
```

Deployment requires valid device credentials and explicit confirmation. Never commit credentials or `.env` files to version control.

## Safety

The sample IP address `192.0.2.10` is reserved for documentation and examples. It is not a real switch target. Use only network devices you are authorized to manage.

## Future Improvements

- Multi-vendor network device support
- Configuration backup and comparison
- Configuration validation before deployment
- Role-based access control
- Deployment logging and reporting