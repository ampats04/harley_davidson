from flask import Flask, render_template, jsonify, request, make_response, session
from database import (
    load_motorcycles_from_db,
    load_motorcycle_from_db,
    upload_info_to_db,
    select_user_info,
    select_one_user,
)
import jwt
from datetime import datetime, timedelta
from functools import wraps


# assign the Flask app to a variable called 'app
app = Flask(__name__)

company = "Harley Davidson"
app.config["SECRET_KEY"] = "82c82be9f515444a99764d7e2b84e893"


# Initial Route
@app.route("/")
def index():

    motorcycles = load_motorcycles_from_db()

    output = (
        render_template("login.html", login="Login Page")
        if not session.get("logged_in")
        else render_template(
            "index.html", motorcycles=motorcycles, company_name=company
        )
    )

    return output


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


# GET & POST BUY
@app.route("/motorcycle/<id>/buy", methods=["GET", "POST"])
def buy_mc(id):

    # use {{args}} when getting data while use form when you want the data to be in the URL
    data = request.form
    motorcycle = load_motorcycle_from_db(id)

    upload_info_to_db(id, data)

    return render_template("submitted.html", buy=data, motorcycle=motorcycle)


# GET ALL USERS
@app.route("/user")
def all_user():

    all_us = select_user_info()

    return jsonify(all_us)


# GET SINGLE USER
@app.route("/user/<id>")
def one_user(id):

    print("test")
    one_us = select_one_user(id)

    print(one_us)
    return jsonify(one_us)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
