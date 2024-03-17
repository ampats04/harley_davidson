import json
from flask import Flask, render_template, jsonify
from database import load_motorcycles_from_db
from flask_marshmallow import Marshmallow

# assign the Flask app to a variable called 'app
app = Flask(__name__)

# assign marshmallow to a variable and bind it with the app

ma = Marshmallow(app)

company = "Harley Davidson"


# Initial Route
@app.route("/")
def index():

    motorcycles = load_motorcycles_from_db()

    return render_template("index.html", motorcycles=motorcycles, company_name=company)


# Return JSON
@app.route("/motorcycles")
def available_motorcycles():

    motorcycles = load_motorcycles_from_db()
    serialized_data = json.dumps(motorcycles)

    return jsonify(serialized_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
