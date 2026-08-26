from flask import Flask, render_template, jsonify, request
from off_lookup import off_lookup
from db import init_db, add_product, get_all_products, get_products_with_urgency, get_product, update_price, log_price_update
from datetime import datetime, timedelta
from pricing import get_price
from collections import deque
import time

app = Flask(__name__)

# Make sure the database and tables exist (the deployed server starts fresh)
init_db()


def seed_demo_data():
    """Add a few demo products so visitors see a working dashboard."""
    if get_all_products():
        return

    def days_from_now(n):
        return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")

    add_product("0001", "Fresh Milk", "Dairy", 1.20, days_from_now(1), 8)
    add_product("0002", "Croissant", "Bakery", 1.50, days_from_now(4), 12)
    add_product("0003", "Cheddar", "Dairy", 3.00, days_from_now(10), 5)
    add_product("0004", "Chicken Sandwich", "Sandwiches", 3.50, days_from_now(2), 6)


seed_demo_data()

# Simple rate limit so a burst of visitors can't drain API credits
AI_CALLS_PER_HOUR = 30
_ai_calls = deque()


def ai_rate_limited():
    now = time.time()
    while _ai_calls and now - _ai_calls[0] > 3600:
        _ai_calls.popleft()
    if len(_ai_calls) >= AI_CALLS_PER_HOUR:
        return True
    _ai_calls.append(now)
    return False

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
    if ai_rate_limited():
        return jsonify({"error": "The demo has hit its hourly AI limit — try again a bit later."}), 429

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

    update_price(product_id, results["reasoning"], new_price)
    log_price_update(product_id, old_price, new_price, results["reasoning"])

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)