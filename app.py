"""Ekta Medicose B2B pharmaceutical distribution showcase."""
import json
import os
import secrets
from pathlib import Path

import pyodbc
from flask import Flask, flash, redirect, render_template, request, url_for

from services.enquiries import validate_enquiry

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
secret_key = os.environ.get("SECRET_KEY")
if not secret_key and os.environ.get("RENDER") == "true":
    raise RuntimeError("Set the SECRET_KEY environment variable in Render.")
app.config["SECRET_KEY"] = secret_key or secrets.token_hex(32)


def load_json(filename):
    with (BASE_DIR / "data" / filename).open(encoding="utf-8") as data_file:
        return json.load(data_file)


def get_db_connection():
    """Use a configured production connection, or local SQL Server Express."""
    connection_string = os.environ.get("SQLSERVER_CONNECTION_STRING") or (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        r"SERVER=.\SQLEXPRESS;"
        "DATABASE=EnquiryDB;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string, timeout=5)


def save_enquiry(values):
    """Insert a validated website enquiry into dbo.Enquiries."""
    connection = None
    try:
        connection = get_db_connection()
        connection.cursor().execute(
            """INSERT INTO dbo.Enquiries
               (FullName, BusinessName, Mobile, Email, City, State,
                EnquiryType, Category, Message, Consent)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            values.get("name", "").strip(),
            values.get("business", "").strip(),
            values.get("mobile", "").strip(),
            values.get("email", "").strip() or None,
            values.get("city", "").strip(),
            values.get("state", "").strip(),
            values.get("enquiry_type", "").strip(),
            values.get("category", "").strip() or None,
            values.get("message", "").strip() or None,
            1,
        )
        connection.commit()
    except Exception:
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()


@app.context_processor
def shared_company_data():
    return {"company": load_json("company.json")}


@app.get("/")
def home():
    products = load_json("products.json")
    categories = list(dict.fromkeys(item["category"] for item in products))
    return render_template("home.html", categories=categories)


@app.get("/products")
def products_page():
    products = load_json("products.json")
    return render_template("products.html", products=products,
                           categories=list(dict.fromkeys(item["category"] for item in products)))


@app.get("/about")
def about():
    return render_template("about.html")


@app.route("/retailer-enquiry", methods=["GET", "POST"])
def enquiry():
    values = request.args.to_dict() if request.method == "GET" else request.form.to_dict()
    errors = {}
    if request.method == "POST":
        errors = validate_enquiry(values)
        if not errors:
            try:
                save_enquiry(values)
            except Exception:
                app.logger.exception("Could not save enquiry to SQL Server")
                flash("We could not save your enquiry right now. Please call Ekta Medicose.", "error")
            else:
                flash("Thank you. Your enquiry has been saved. Our team will be in touch.", "success")
                return redirect(url_for("enquiry", sent="1"))
        if errors:
            flash("Please review the highlighted fields and try again.", "error")
    return render_template("enquiry.html", values=values, errors=errors,
                           submitted=request.args.get("sent") == "1",
                           categories=load_json("products.json"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
