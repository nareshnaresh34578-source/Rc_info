from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

API_URL = "https://vehicle-eight-vert.vercel.app/api?rc={}"

def valid_rc(rc):
    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{1,4}$"
    return re.match(pattern, rc)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    rc = ""

    if request.method == "POST":
        rc = request.form.get("rc", "").strip().upper()

        if not valid_rc(rc):
            error = "Invalid RC Number"
        else:
            try:
                response = requests.get(API_URL.format(rc), timeout=10)
                if response.status_code == 200:
                    result = response.json()
                else:
                    error = "No Record Found"
            except Exception:
                error = "Server Error"

    return render_template(
        "index.html",
        result=result,
        error=error,
        rc=rc
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
