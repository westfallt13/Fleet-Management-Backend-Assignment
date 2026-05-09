from flask import Flask, jsonify
from flask_cors import CORS  # <-- Import CORS
from database import init_db

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

# Initialize DB on startup
init_db()

@app.route("/")
def home():
    return jsonify({"message": "Logistics API running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)