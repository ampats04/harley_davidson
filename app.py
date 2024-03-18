import json
from flask import Flask, render_template, jsonify
from database import load_motorcycles_from_db, load_motorcycle_from_db


# assign the Flask app to a variable called 'app
app = Flask(__name__)

# assign marshmallow to a variable and bind it with the app


company = "Harley Davidson"


# Initial Route
@app.route("/")
def index():

    motorcycles = load_motorcycles_from_db()

    return render_template("index.html", motorcycles=motorcycles, company_name=company)


# GET motorcycle
@app.route("/motorcycle/<id>", methods=["GET"])
def show_mc(id):

    mc = load_motorcycle_from_db(id)

    return jsonify(mc)


# Return JSON
@app.route("/motorcycles")
def available_motorcycles():

    motorcycles = load_motorcycles_from_db()

    return jsonify(motorcycles)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
