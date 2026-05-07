from flask import Flask, jsonify
from database import init_db

app = Flask(__name__)

# Initialize DB on startup
init_db()

@app.route("/")
def home():
    return jsonify({"message": "Logistics API running", "message": "This is just for test purposes"})

if __name__ == "__main__":
    app.run(debug=True)

    app.run(host="0.0.0.0", port=5000)