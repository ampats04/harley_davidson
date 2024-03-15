from flask import Flask, render_template, jsonify

app = Flask(__name__)

company = "Harley Davidson"

MOTORCYCLES = [
    {
        "id": 1,
        "model": "Street Bob 114",
        "year": 2024,
        "displacement": "1868 cc",
        "price": 500000,
    },
    {
        "id": 2,
        "model": "Soft tail",
        "year": 2024,
        "displacement": "1868 cc",
        "price": 500000,
    },
    {
        "id": 3,
        "model": "Low Rider",
        "year": 2024,
        "displacement": "1868 cc",
        "price": 500000,
    },
    {
        "id": 4,
        "model": "Sport Glide",
        "year": 2024,
        "displacement": "1868 cc",
        "price": 500000,
    },
]


@app.route("/")
def index():
    return render_template("home.html", motorcycles=MOTORCYCLES, company_name=company)


# Return JSON
@app.route("/motorcycles")
def available_motorcycles():
    return jsonify(MOTORCYCLES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
