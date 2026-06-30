from flask import Flask, render_template, jsonify
from off_lookup import off_lookup

app = Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/lookup/<barcode>")
def lookup(barcode):
    return jsonify(off_lookup(barcode))


if __name__ == "__main__":
    app.run(debug=True)