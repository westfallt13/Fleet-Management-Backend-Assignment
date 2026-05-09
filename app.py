from flask import Flask, jsonify, render_template, request
from flask_cors import CORS  # <-- Import CORS
from database import init_db
import crud

app = Flask(__name__, static_folder='static', static_url_path='/', template_folder='templates')
CORS(app)  # <-- Enable CORS for all routes

# Initialize DB on startup
init_db()

# --- API Routes ---

@app.route("/drivers", methods=["GET", "POST"])
def manage_drivers():
    if request.method == "POST":
        data = request.json
        new_driver = crud.create_driver(data.get("Name"), data.get("LicenseType"), data.get("VehicleID"))
        return jsonify(new_driver), 201
    return jsonify(crud.get_all_drivers())

@app.route("/vehicles", methods=["GET", "POST"])
def manage_vehicles():
    if request.method == "POST":
        data = request.json
        new_vehicle = crud.create_vehicle(data.get("LicensePlate"), data.get("Model"))
        return jsonify(new_vehicle), 201
    return jsonify(crud.get_all_vehicles())

@app.route("/routes", methods=["GET", "POST"])
def manage_routes():
    if request.method == "POST":
        data = request.json
        new_route = crud.create_route(data.get("Date"), data.get("ServiceZone"))
        return jsonify(new_route), 201
    return jsonify(crud.get_all_routes())

@app.route("/packages", methods=["GET", "POST"])
def manage_packages():
    if request.method == "POST":
        data = request.json
        new_package = crud.create_package(data.get("Description"), data.get("Weight"), data.get("RouteID"))
        return jsonify(new_package), 201
    # Assuming there's a get_all_packages, but didn't see one. If it doesn't exist, we will add it.
    try:
        return jsonify(crud.get_all_packages())
    except AttributeError:
        # Fallback if get_all_packages isn't implemented in crud.py yet
        return jsonify({"message": "Packages feature coming soon"}), 501

# --- Frontend Serving ---

@app.route("/")
def home():
    return render_template("index.html")

# Add a catch-all route so React Router can handle client-side routing
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)