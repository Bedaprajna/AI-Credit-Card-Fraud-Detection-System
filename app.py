from flask import Flask, request, render_template_string
import mysql.connector
from datetime import datetime
import random

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Mysql@2005",
    database="fraud_detection",
    connection_timeout=5
)

cursor = db.cursor()

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>AI Credit Card Fraud Detection</title>

<style>

body{
    font-family: Arial;
    background:#f2f2f2;
    text-align:center;
    margin-top:50px;
}

.box{
    background:white;
    width:500px;
    margin:auto;
    padding:30px;
    border-radius:10px;
    box-shadow:0px 0px 10px gray;
}

input, select{
    padding:10px;
    width:85%;
    margin:10px;
}

button{
    padding:10px 20px;
    background:blue;
    color:white;
    border:none;
    cursor:pointer;
}

h2{
    color:#333;
}

.result{
    margin-top:20px;
    font-size:20px;
    font-weight:bold;
}

</style>

</head>

<body>

<div class="box">

<h2>AI Credit Card Fraud Detection</h2>

<form method="POST">

<input
type="number"
step="0.01"
name="amount"
placeholder="Enter Transaction Amount"
required>

<select name="location" required>

<option value="">Select Location</option>

<option>India</option>
<option>USA</option>
<option>Russia</option>
<option>China</option>
<option>Germany</option>
<option>Pakistan</option>

</select>

<select name="device" required>

<option value="">Select Device</option>

<option>Android</option>
<option>iPhone</option>
<option>Laptop</option>

</select>

<br>

<button type="submit">

Check Transaction

</button>

</form>

<div class="result">

{{ result|safe }}

</div>

</div>

</body>

</html>

"""

@app.route("/", methods=["GET", "POST"])

def home():

    result = ""

    if request.method == "POST":

        amount = float(request.form["amount"])

        location = request.form["location"]

        device = request.form["device"]

        # Auto-generated transaction count
        count = random.randint(1, 10)

        # Auto-detected current hour
        hour = datetime.now().hour

        fraud_probability = 0

        reasons = []

        # Rule 1: High Amount
        if amount > 100000:
            fraud_probability += 40
            reasons.append("Huge transaction amount")

        # Rule 2: Suspicious Country
        suspicious_locations = [
            "Russia",
            "China",
            "Pakistan"
        ]

        if location in suspicious_locations:
            fraud_probability += 30
            reasons.append("Suspicious location")

        # Rule 3: Too Many Transactions
        if count > 5:
            fraud_probability += 20
            reasons.append("Too many recent transactions")

        # Rule 4: Late Night Transactions
        if hour >= 1 and hour <= 4:
            fraud_probability += 10
            reasons.append("Suspicious transaction time")

        # Final Decision
        if fraud_probability >= 50:

            result = f"""
            <span style='color:red'>
            Fraud Transaction Detected
            </span>

            <br><br>

            Fraud Probability: {fraud_probability}%

            <br><br>

            Auto Detected Transaction Count: {count}

            <br><br>

            Reasons:
            <br>

            {'<br>'.join(reasons)}
            """

            db_result = "Fraud"

        else:

            result = f"""
            <span style='color:green'>
            Normal Transaction
            </span>

            <br><br>

            Fraud Probability: {fraud_probability}%

            <br><br>

            Auto Detected Transaction Count: {count}
            """

            db_result = "Normal"

        # Save into database
        sql = """
        INSERT INTO transactions (amount, prediction)
        VALUES (%s, %s)
        """

        values = (amount, db_result)

        cursor.execute(sql, values)

        db.commit()

    return render_template_string(HTML, result=result)

if __name__ == "__main__":

    print("Starting Flask Server...")

    app.run(debug=True)