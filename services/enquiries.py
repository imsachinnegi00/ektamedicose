"""Validation and SQL Server storage for retailer enquiries."""
import os
import re

import pyodbc


def save_enquiry(values):
    """Save one validated enquiry using the SQL Server connection string in the environment."""
    connection_string = os.environ.get("SQLSERVER_CONNECTION_STRING")
    if not connection_string:
        raise RuntimeError("SQLSERVER_CONNECTION_STRING is not configured")

    # The question marks are parameter placeholders; values are sent separately,
    # so user-entered text is never assembled into the SQL statement.
    with pyodbc.connect(connection_string, timeout=5) as connection:
        connection.cursor().execute(
            """INSERT INTO dbo.Enquiries
               (FullName, BusinessName, Mobile, Email, City, State,
                EnquiryType, Category, Message, ConsentGiven)
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


def validate_enquiry(values):
    errors = {}
    required = {"name": "Full name", "business": "Shop or company name", "mobile": "Mobile number",
                "city": "City", "state": "State", "enquiry_type": "Enquiry type"}
    for key, label in required.items():
        if not values.get(key, "").strip():
            errors[key] = f"{label} is required."
    mobile = re.sub(r"[\s()+-]", "", values.get("mobile", ""))
    if values.get("mobile", "").strip() and not re.fullmatch(r"\d{10,13}", mobile):
        errors["mobile"] = "Enter a valid phone number (10–13 digits)."
    email = values.get("email", "").strip()
    if email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        errors["email"] = "Enter a valid email address."
    if not values.get("consent"):
        errors["consent"] = "Consent is required to process this enquiry."
    return errors
