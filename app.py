from flask import Flask, jsonify, render_template
from flask_cors import CORS  # <-- Import CORS
from database import init_db

app = Flask(__name__, static_folder='static', static_url_path='/', template_folder='templates')
CORS(app)  # <-- Enable CORS for all routes

# Initialize DB on startup
init_db()

@app.route("/")
def home():
    return render_template("index.html")

# Add a catch-all route so React Router can handle client-side routing
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)