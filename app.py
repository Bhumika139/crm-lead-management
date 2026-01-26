from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# ---------- DB CONNECTION ----------


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )



# ---------- HOME ----------
@app.route("/")
def home():
    return "Backend running"

# ---------- GET LEADS ----------
@app.route("/leads", methods=["GET"])
def get_leads():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM leads")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(data)

#---------Run----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ---------- ADD LEAD ----------
@app.route("/addLead", methods=["POST"])
def add_lead():
    data = request.json

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO leads
        (name, mobile, email, source, campaign, city, product, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["name"],
        data["mobile"],
        data["email"],
        data.get("source",""),
        data.get("campaign",""),
        data.get("city",""),
        data.get("product",""),
        data.get("status","New")
    ))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "Lead added successfully"})

# ---------- DELETE LEAD ----------
@app.route("/deleteLead/<int:lead_id>", methods=["DELETE"])
def delete_lead(lead_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM leads WHERE id=%s", (lead_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Lead deleted successfully"})

# ---------- UPDATE LEAD ----------
@app.route("/updateLead/<int:lead_id>", methods=["PUT"])
def update_lead(lead_id):
    data = request.json

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE leads SET
        name=%s,
        mobile=%s,
        email=%s,
        source=%s,
        campaign=%s,
        city=%s,
        product=%s,
        status=%s
        WHERE id=%s
    """, (
        data["name"],
        data["mobile"],
        data["email"],
        data["source"],
        data["campaign"],
        data["city"],
        data["product"],
        data["status"],
        lead_id
    ))

    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Lead updated successfully"})

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

