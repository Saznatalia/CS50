import os
import datetime
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from datetime import timedelta
from datetime import date

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# @app.before_request
# def before_request():
#     g.user = current_user

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = "sessions"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///diet.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/blocks")
def blocks():
    return render_template("blocks.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide username")
            return apology("Please provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide password")
            return apology("Please provide password", 403)

        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["password"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Log out page
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    q = request.args.get("username")
    if not q:
        return jsonify(True)
    users = db.execute("SELECT username FROM users WHERE username = :username", username=q)
    if users != []:
        return jsonify(False)
    return jsonify(True)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Make sure all fields are filled and password and conifrmation are same
        if not username:
            flash("Missing username!")
            return apology("Missing username!", 403)
        elif not password:
            flash("Missing password!")
            return apology("Missing password!", 403)
        elif not confirmation:
            flash("Missing password confirmation!")
            return apology("Missing password confirmation!", 403)
        elif password != confirmation:
            flash("Your password and confirmation password do not match!")
            return apology("Your password and confirmation password do not match!", 403)

        # Make sure username is not registered
        elif db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            flash("Username is already exists!")
            return redirect("/register")

        # Hash password
        hash_password = generate_password_hash(password)

        # Insert a new user into database
        user_id = db.execute("INSERT INTO users (username, password) VALUES(:username,:password)",
                             username=request.form.get("username"), password=hash_password)

        # Storing ID number within the session
        session["user_id"] = user_id

        flash("Registered!")

        # Redirect user to registered page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/calculators", methods=["GET", "POST"])
def calculators():
    return render_template("calculators.html")


@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    return render_template("bmi.html")


@app.route("/ideal_weight", methods=["GET", "POST"])
def ideal_weight():
    return render_template("ideal_weight.html")


@app.route("/body_fat", methods=["GET", "POST"])
def body_fat():
    return render_template("body_fat.html")


@app.route("/kcal_intake", methods=["GET", "POST"])
def kcal_intake():
    return render_template("kcal_intake.html")


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    username = (db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"]))[0]['username']
    today = date.today()
    items = db.execute("SELECT * from items")
    breakfast_records = db.execute("SELECT * FROM records WHERE id=:user_id and date=:date and meal=:meal", user_id=session["user_id"], date=today, meal="breakfast")
    lunch_records = db.execute("SELECT * FROM records WHERE id=:user_id and date=:date and meal=:meal", user_id=session["user_id"], date=today, meal="lunch")
    dinner_records = db.execute("SELECT * FROM records WHERE id=:user_id and date=:date and meal=:meal", user_id=session["user_id"], date=today, meal="dinner")
    snack_records = db.execute("SELECT * FROM records WHERE id=:user_id and date=:date and meal=:meal", user_id=session["user_id"], date=today, meal="snack")
    if request.method == "POST":
        return "{}"
    else:
        return render_template("diary.html", username=username, today=today, items=json.dumps(items), breakfast_records=breakfast_records, lunch_records=lunch_records,
                                             dinner_records=dinner_records, snack_records=snack_records)


@app.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():
    today = date.today()
    if request.method == "POST":
        selected_item = request.get_json(force=True)
        print(selected_item)
        db.execute("INSERT INTO records (id, item, unit, size, carb, protein, fat, meal, date) VALUES (:user_id, :item, :unit, :size, :carb, :protein, :fat, :meal, :date)",
                    user_id=session["user_id"], item=selected_item['item'], unit=selected_item['unit'], size=selected_item['size'], carb=selected_item['carb'], protein=selected_item['protein'],
                    fat=selected_item['fat'], meal=selected_item['meal'], date=today)
    return "[]"


@app.route("/delete_item", methods=["GET", "POST"])
@login_required
def delete_item():
    today = date.today()
    if request.method == "POST":
        selected_item = request.get_json(force=True)
        print(selected_item)
        print(selected_item['item'])
        db.execute("DELETE FROM records WHERE id = :user_id and item = :item and unit = :unit and size = :size and carb = :carb and protein = :protein and fat = :fat and meal = :meal and date = :date",
                    user_id=session["user_id"], item=selected_item['item'], unit=selected_item['unit'], size=selected_item['size'], carb=selected_item['carb'], protein=selected_item['protein'],
                    fat=selected_item['fat'], meal=selected_item['meal'], date=today)
    return "[]"


@app.route("/block_today", methods=["GET", "POST"])
@login_required
def block_today():
    today = date.today()
    today_records = db.execute("SELECT * FROM records WHERE id=:user_id and date=:date", user_id=session["user_id"], date=today)
    carbs = []
    proteins = []
    fats = []
    for i in range(0, len(today_records)):
        carbs.append(today_records[i]['carb'])
    for i in range(0, len(today_records)):
        proteins.append(today_records[i]['protein'])
    for i in range(0, len(today_records)):
        fats.append(today_records[i]['fat'])
    total_carb = sum(carbs)
    total_protein = sum(proteins)
    total_fat = sum(fats)
    block = [total_carb, total_protein, total_fat]
    blocks = min(block)
    print("fat: " + str(total_fat))
    print("carbs: " + str(total_carb))
    print("proteins: " + str(total_protein))
    return render_template("block_today.html", today=today, total_carb=total_carb, total_protein=total_protein, total_fat=total_fat, blocks=blocks)

# Might continue later for now obsolete
# @app.route("/recipes", methods=["GET", "POST"])
# @login_required
# def recipes():
#     username = (db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"]))[0]['username']
#     today = date.today()
#     items = db.execute("SELECT * from items")
#     if request.method == "POST":
#         return render_template("recipes.html", username=username, today=today, items=json.dumps(items))
#     return render_template("recipes.html", username=username, today=today, items=json.dumps(items))

@app.route("/add_user_item", methods=["GET", "POST"])
@login_required
def add_user_item():
    today = date.today()
    if request.method == "POST":
        selected_item = request.get_json(force=True)
        print(selected_item)
        db.execute("INSERT INTO user_items (user_id, item, protein, carb, fat, amount, unit) VALUES (:user_id, :item, :protein, :carb, :fat, :amount, :unit)",
                    user_id=session["user_id"], item=selected_item['item'], protein=selected_item['protein'], carb=selected_item['carb'],
                    fat=selected_item['fat'], amount=selected_item['amount'], unit=selected_item['unit'],)
    return "[]"


@app.route("/me", methods=["GET", "POST"])
@login_required
def me():
    username = (db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"]))[0]['username']
    today = date.today()
    measurements = db.execute("SELECT * from measurements WHERE id = :user_id", user_id=session['user_id'])
    if request.method == "POST":

        weight = request.form.get("weight")
        chest = request.form.get("chest")
        waist = request.form.get("waist")
        hips = request.form.get("hips")
        print(1)
        # Make sure input is not blank
        try:
            float(weight)
        except ValueError:
            flash("Weight must be positive number")
            return apology('Your weight must be a positive number')
        if not weight:
            flash("Please enter your weight!")
            return apology("Missing your weight!", 403)
        elif not chest:
            flash("Please enter your chest measurements!")
            return apology("Missing your chest measurements!", 403)
        elif not waist:
            flash("Please enter your waist measurements!")
            return apology("Missing your waist measurements!", 403)
        elif not hips:
            flash("Please enter your hips measurements")
            return apology("Missing your hips measurements!", 403)
        # Make sure the inout are positive numbers
        elif float(weight) < 0:
            flash("Your weight must be a positive number")
            return apology("Your weight must be a positive number")
        elif chest.isdigit() == False or int(chest) < 0:
            flash("Your chest must be a positive number")
            return apology("Your chest must be a positive number")
        elif waist.isdigit() == False or int(waist) < 0:
            flash("Your waist must be a positive number")
            return apology("Your waist must be a positive number")
        elif hips.isdigit() == False or int(hips) < 0:
            flash("Your hips must be a positive number")
            return apology("Your hips must be a positive number")
        db.execute("INSERT INTO measurements (id, weight, chest, waist, hips, date) VALUES (:user_id, :weight, :chest, :waist, :hips, :date)",
                    user_id=session["user_id"], weight=weight, chest=chest, waist=waist, hips=hips, date=today)
        return redirect("/me")

    # If "GET"
    else:
        return render_template("me.html", username=username, today=today, measurements=json.dumps(measurements))


@app.route("/history", methods=['GET'])
@login_required
def history():
    records = db.execute("SELECT * FROM records WHERE id = :user_id ORDER BY DATE DESC", user_id=session["user_id"])
    return render_template("history.html", records=records)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    today = date.today()
    username = (db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"]))[0]['username']
    measurements = db.execute("SELECT * FROM measurements WHERE id=:user_id", user_id=session["user_id"])
    if measurements == []:
        weight = "Uknown"
    else:
        for i in range(len(measurements)):
            weight = measurements[i]['weight']
    print(measurements)
    return render_template("account.html", username=username, today=today, weight=weight)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password_change():
    # User reaches royte vis POST (submitting the form via POST)
    if request.method == "POST":
        password = request.form.get("new_password")
        confirmation = request.form.get("new_confirmation")
        if not password:
            return apology("Missing new password")
        elif not confirmation:
            return apology("Missing new password confirmation!")
        elif password != confirmation:
            return apology("Your new password and confirmation password do not match!")
        db.execute("UPDATE users SET password = :password WHERE id = :user_id",
                   password=generate_password_hash(password), user_id=session["user_id"])
        flash("Password has been updated!")
        return render_template("account.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("account.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)