import cs50
import csv


from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

# Open and write into csv file
@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name") or not request.form.get("last_name") or not request.form.get("age") or not request.form.get("activity"):
        return render_template("error.html")
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "last_name", "age", "activity", "response"])
        writer.writerow({"name": request.form.get("name"), "last_name": request.form.get("last_name"),
                         "age": request.form.get("age"), "activity": request.form.get("activity"), "response": request.form.get("response")})
    return redirect("/sheet")

# Read from csv file into list
@app.route("/sheet", methods=["GET", "POST"])
def get_sheet():
    result = []
    with open("survey.csv", "r") as file:
        data = csv.reader(file)
        result = list(data)
    return render_template("sheet.html", result=result)