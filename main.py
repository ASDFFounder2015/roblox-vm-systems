import os
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_COMMANDS = {
    "cpu": "wmic cpu get name",   # Command to get CPU info
    "ip": "ipconfig",             # Command to get IP config
    "user": "whoami",             # Command to get the current user
    "dir": "dir"                  # Command to list directory
}

@app.route("/run", methods=["POST"])
def run_command():
    data = request.get_json()

    if data.get("auth") != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    cmd_key = data.get("command")
    if cmd_key in ALLOWED_COMMANDS:
        result = subprocess.run(ALLOWED_COMMANDS[cmd_key], shell=True, capture_output=True, text=True)
        return jsonify({"output": result.stdout})
    else:
        return jsonify({"error": "Command not allowed"}), 403

@app.route("/")
def hello():
    return "VM API Running!"

if __name__ == "__main__":
    app.run(debug=True)
