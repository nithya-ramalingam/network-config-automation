from flask import Flask, jsonify, render_template_string

from config_generator import generate_all


app = Flask(__name__)


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Configuration Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f6f8;
        }

        h1 {
            color: #1f2937;
        }

        .device {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }

        pre {
            background: #1e293b;
            color: #e2e8f0;
            padding: 15px;
            overflow-x: auto;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Network Configuration Generator</h1>
    <p>Automatically generated Cisco configurations</p>

    {% for name, config in configurations.items() %}
        <div class="device">
            <h2>{{ name }}</h2>
            <pre>{{ config }}</pre>
        </div>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def home():
    configurations = generate_all()

    return render_template_string(
        HTML_PAGE,
        configurations=configurations
    )


@app.route("/api/devices")
def devices():
    configurations = generate_all()

    return jsonify({
        "devices": list(configurations.keys())
    })


@app.route("/api/config/<device_name>")
def device_config(device_name):
    configurations = generate_all()

    if device_name not in configurations:
        return jsonify({
            "error": "Device not found"
        }), 404

    return jsonify({
        "device": device_name,
        "configuration": configurations[device_name]
    })


if __name__ == "__main__":
    app.run(debug=True)