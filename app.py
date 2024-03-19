from flask import Flask, render_template, jsonify, request
from database import (
    load_motorcycles_from_db,
    load_motorcycle_from_db,
    upload_info_to_db,
    select_user_info,
)


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
@app.route("/motorcycle/<id>")
def show_mc(id):

    mc = load_motorcycle_from_db(id)

    return render_template("motorcycle_pages.html", motorcycle=mc)


# Return JSON
@app.route("/motorcycles")
def available_motorcycles():

    motorcycles = load_motorcycles_from_db()

    return jsonify(motorcycles)


@app.route("/motorcycle/<id>/buy", methods=["GET", "POST"])
def buy_mc(id):

    # use {{args}} when getting data while use form when you want the data to be in the URL
    data = request.form
    motorcycle = load_motorcycle_from_db(id)

    upload_info_to_db(id, data)

    return render_template("submitted.html", buy=data, motorcycle=motorcycle)


@app.route("/user")
def all_user():

    all_us = select_user_info()

    return jsonify(all_us)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
