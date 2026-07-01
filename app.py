from flask import Flask, render_template, jsonify, request
from off_lookup import off_lookup
from db import add_product, get_products_with_urgency, get_product, update_price, log_price_update
from datetime import datetime
from pricing import get_price

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


@app.route("/reprice/<int:product_id>", methods=["POST"])
def reprice(product_id):
    product = get_product(product_id)

    hour = datetime.now().hour
    if hour < 12:
        time_of_day = "morning"
    elif hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    expiry = datetime.strptime(product["expiry_date"], "%Y-%m-%d")
    days_left = (expiry - datetime.now()).days

    results = get_price(
        product["name"],
        product["category"],
        product["original_price"],
        days_left,
        product["stock"],
        time_of_day
    )

    old_price = product["current_price"]
    new_price = results["price"]

    update_price(product_id, new_price)
    log_price_update(product_id, old_price, new_price, results["reasoning"])

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)