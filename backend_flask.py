from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from distance_filter import rank_hospital_distances, filter_by_insurance

df = pd.read_pickle("hospital_insurances_accepted_with_hospitalids.pkl")

app = Flask(__name__)
CORS(app)

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(df.to_dict(orient="records"))

@app.route("/filter", methods=["POST"])
def filter_hospitals():
    data = request.get_json()
    user_info = data.get("userInfo", [])

    if len(user_info) != 2:
        return jsonify({"error": "Expected ['address', 'insurance']"}), 400

    user_address = user_info[0]
    user_insurance = user_info[1]

    sorted_distances = rank_hospital_distances(user_address)
    results = filter_by_insurance(user_insurance, sorted_distances)

   

    return jsonify(results)

@app.route("/")
def home():
    return "<h1>Welcome to CareScout!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
