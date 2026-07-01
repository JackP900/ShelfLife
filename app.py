from flask import Flask, render_template, jsonify, request
from off_lookup import off_lookup
from db import add_product, get_products_with_urgency

app = Flask(__name__)

@app.route("/")
def index():
    products = get_products_with_urgency()
    return render_template("index.html", products=products)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    add_product(
        data["barcode"],
        data["name"],
        data["category"],
        float(data["original_price"]),
        data["expiry"],
        int(data["stock"])
    )
    return jsonify({"status": "saved"})


@app.route("/lookup/<barcode>")
def lookup(barcode):
    return jsonify(off_lookup(barcode))


if __name__ == "__main__":
    app.run(debug=True)