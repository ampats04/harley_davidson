from functools import wraps
from flask import (
    Flask,
    redirect,
    render_template,
    jsonify,
    request,
    make_response,
    session,
    url_for,
)
import jwt
from database import (
    load_motorcycles_from_db,
    load_motorcycle_from_db,
    upload_info_to_db,
    select_user_info,
    select_one_user,
    login_user,
    register_user,
)
from uuid import uuid4
from datetime import *


# assign the Flask app to a variable called 'app
app = Flask(__name__)

company = "Harley Davidson"
app.config["SECRET_KEY"] = uuid4().hex


# function decorator
def authenticated(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            response = {"message": "Not Authenticated"}
            return jsonify(response)
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "No Tokens"})
        return func(*args, **kwargs)

    return wrapped()


# Initial Route
@app.route("/")
def index():

    motorcycles = load_motorcycles_from_db()

    if "username" in session:
        return render_template(
            "index.html",
            motorcycles=motorcycles,
            company_name=company,
            username=session["username"],
        )

    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        data = request.form
        if login_user(data):
            session["logged_in"] = True
            expiry = datetime.now(timezone.utc) + timedelta(seconds=60)
            token = jwt.encode(
                {"user": data["username"], "exp": expiry}, app.config["SECRET_KEY"]
            )

            decoded_token = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            return jsonify({"token": decoded_token})
        else:
            error = "Invalid token ss"
            # return render_template("login.html", error=error)
            return jsonify(error)

    # return render_template("login.html")


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
    if request.method == "POST":
        upload_info_to_db(id, data)

        redirect(url_for("index"))

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


@app.route("/register", methods=["GET", "POST"])
def register():
    data = request.form
    if request.method == "POST":
        if register_user(data):

            return render_template("register.html", error="Username already existed!")

        else:
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
