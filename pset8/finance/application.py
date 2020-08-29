import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Check all available stock history and cash
    owned_shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
    available_cash = db.execute("SELECT cash FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    cash = float(available_cash[0]['cash'])
    total_price_list = []
    for item in owned_shares:
        total = float(item['price']) * int(item['number'])
        item["total"] = usd(total)
        total_price_list.append(total)

    # Find the total for all shares
    grand_total = cash + sum(total_price_list)
    return render_template("index.html", owned_shares=owned_shares, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check symbol if it's valid, i.e. exists in API_KEY
        stock = lookup(request.form.get("symbol"))
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Shares must be positive number")

        # Make sure the symbol was provided
        if not request.form.get("symbol"):
            return apology("Must provide symbol")

        # Make sure the number of shares was provided
        if not shares:
            return apology("Must provide number of shares")

        # Make sure the number of shares is positivite
        if shares <= 0:
            return apology("Number of shares must be higher than 0")

        # Make sure symbol is valid
        if stock == None:
            return apology("Invalid symbol")

        price = float(stock['price'])
        total_price = shares * price

        # Check how much cash available
        available_cash = db.execute("SELECT cash FROM users WHERE user_id = :user_id", user_id=session["user_id"])
        cash = float(available_cash[0]['cash'])

        # Make sure user have enough cash to buy shares
        if (total_price <= cash):

            # Creates list of existing symbols in portfolio
            owned_symbols = db.execute("SELECT symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
            list_symbols = []
            for item in owned_symbols:
                list_symbols.append(item['symbol'])

            # Symbol is already in portfolio
            if request.form.get("symbol") in list_symbols:

                # Records into history table
                id = db.execute("INSERT INTO history (user_id, symbol, company, number, price, date) VALUES (:user_id, :symbol, :company,  :number, :price, :date)",
                                user_id=session["user_id"], symbol=stock['symbol'], company=stock['name'], number=shares, price=stock['price'], date=datetime.datetime.now().date())

                # Updates cash in users
                db.execute("UPDATE users SET cash = cash - :spent WHERE user_id = :user_id",
                           spent=total_price, user_id=session["user_id"])
                updated_cash = float((db.execute("SELECT cash FROM users WHERE :user_id = user_id",
                                                 user_id=session["user_id"])[0]['cash']))

                # Updates number in portfolio
                db.execute("UPDATE portfolio SET number = number + :shares WHERE user_id = :user_id and symbol = :symbol",
                           shares=int(request.form.get("shares")), user_id=session["user_id"], symbol=stock['symbol'])

                # Finds total price for owned shares
                owned_shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
                total_price_list = []
                for item in owned_shares:
                    total = float(item['price']) * int(item['number'])
                    item["total"] = usd(total)
                    total_price_list.append(total)

                # Finds the total for all shares adn cash
                grand_total = updated_cash + sum(total_price_list)
                return render_template("bought.html", owned_shares=owned_shares, cash=usd(updated_cash), grand_total=usd(grand_total))

            # For a new symbol
            else:

                # Records into history table
                id = db.execute("INSERT INTO history (user_id, symbol, company, number, price, date) VALUES (:user_id, :symbol, :company,  :number, :price, :date)",
                                user_id=session["user_id"], symbol=stock['symbol'], company=stock['name'], number=shares, price=stock['price'], date=datetime.datetime.now().date())

                # Records into portfolio new symbol
                id = db.execute("INSERT INTO portfolio (user_id, symbol, company, number, price, date) VALUES (:user_id, :symbol, :company,  :number, :price, :date)",
                                user_id=session["user_id"], symbol=stock['symbol'], company=stock['name'], number=shares, price=stock['price'], date=datetime.datetime.now().date())

                # Updates cash in users
                db.execute("UPDATE users SET cash = cash - :spent WHERE user_id = :user_id",
                           spent=total_price, user_id=session["user_id"])
                updated_cash = float((db.execute("SELECT cash FROM users WHERE :user_id = user_id",
                                                 user_id=session["user_id"])[0]['cash']))

                # Finds total price for owned shares
                owned_shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id",
                                          user_id=session["user_id"])
                total_price_list = []
                for item in owned_shares:
                    total = float(item['price']) * int(item['number'])
                    item["total"] = usd(total)
                    total_price_list.append(total)

                # Find the total for all shares and cash
                grand_total = updated_cash + sum(total_price_list)

                # Redirect to bought page
                return render_template("bought.html", owned_shares=owned_shares, cash=usd(updated_cash), grand_total=usd(grand_total))

        # Apologise as user does not enough cash
        else:
            return apology("Sorry you don't have enough cash to purchase the shares")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    q = request.args.get("username")
    accounts = db.execute("SELECT username FROM users WHERE username = :username", username=q)
    print(accounts)
    if not q:
        return jsonify(False)
    elif accounts != []:
        return jsonify(False)
    return jsonify(True)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""

    # All transactions from history table
    history = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not request.form.get("symbol"):
            return apology("Must provide symbol")
        if stock == None:
            return apology("Invalid symbol")
        else:
            return render_template("quoted.html", name=stock['name'], symbol=stock['symbol'], price=usd(stock['price']))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


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
            return apology("Missing username!")
        elif not password:
            return apology("Missing password!")
        elif not confirmation:
            return apology("Missing password confirmation!")
        elif password != confirmation:
            return apology("Your password and confirmation password do not match!")

        # Make sure username is not registered
        elif db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            return apology("Username is already taken!")

        # Hash password
        hash_password = generate_password_hash(password)

        # Insert a new user into database
        user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username,:hash)",
                             username=request.form.get("username"), hash=hash_password)

        # Storing ID number within the session
        session["user_id"] = user_id

        # Redirect user to registered page
        return redirect("/registered")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/registered", methods=["GET", "POST"])
@login_required
def registered():
    available_cash = db.execute("SELECT cash FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    cash = float(available_cash[0]['cash'])
    return render_template("registered.html", cash=usd(cash))


@app.route("/password", methods=["GET", "POST"])
@login_required
def password_change():
    ''' https://www.patricksoftwareblog.com/changing-users-password '''

    # User reaches royte vis POST (submitting the form via POST)
    if request.method == "POST":
        password = request.form.get("new_password")
        confirmation = request.form.get("new_confirmation")
        if not password:
            return apology("Missing new password!")
        elif not confirmation:
            return apology("Missing new password confirmation!")
        elif password != confirmation:
            return apology("Your new password and confirmation password do not match!")
        db.execute("UPDATE users SET hash = :hash WHERE user_id = :user_id",
                   hash=generate_password_hash(password), user_id=session["user_id"])
        flash("Password has been updated!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # All symbols owned and list of them
    owned_symbols = db.execute("SELECT symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
    owned_symbols_list = []
    for item in owned_symbols:
        owned_symbols_list.append(item['symbol'])

    # User reaches royte vis POST (submitting the form via POST)
    if request.method == "POST":

        # Variables
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        symbol_portfolio = lookup(symbol)
        current_price = float(symbol_portfolio['price'])
        total_got = current_price * shares

        # All available shares in portfolio for requested symbol
        available_shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id and symbol = :symbol",
                                      user_id=session["user_id"], symbol=symbol)

        # Make sure the symbol was provided
        if not symbol:
            return apology("Must provide symbol")

        # Make sure symbol is valid
        if symbol not in owned_symbols_list:
            return apology("You don't have these shares")

        # Make sure the number of shares was provided
        if not shares:
            return apology("Must provide number of shares")

        # Make sure the number of shares is positivite
        if shares <= 0:
            return apology("Number of shares must be higher than 0")

        # Make sure you have enough number of shares on hands
        if shares > int(available_shares[0]['number']):
            return apology("You don't have enough shares")

        # Record transaction to history table
        id = db.execute("INSERT INTO history (user_id, symbol, company, number, price, date) VALUES (:user_id, :symbol, :company,  :number, :price, :date)",
                        user_id=session["user_id"], symbol=symbol, company=symbol_portfolio['name'], number=-shares, price=current_price, date=datetime.datetime.now().date())

        # Update available cash
        db.execute("UPDATE users SET cash = cash + :got WHERE user_id = :user_id", got=total_got, user_id=session["user_id"])
        updated_cash = float((db.execute("SELECT cash FROM users WHERE :user_id = user_id", user_id=session["user_id"])[0]['cash']))

        # Update available number of shares
        db.execute("UPDATE portfolio SET number = number - :shares WHERE user_id = :user_id and symbol = :symbol",
                   shares=shares, user_id=session["user_id"], symbol=symbol)

        # Updated_number = int((db.execute("SELECT number FROM portfolio WHERE user_id = :user_id and symbol = :symbol, user_id=session["user_id"], symbol=symbol))[0]['number'])

        # Check if updated number != 0 after selling
        db.execute("DELETE FROM portfolio WHERE number = 0")

        # Total price for shares only
        owned_shares = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
        total_price_list = []
        for item in owned_shares:
            total = float(item['price']) * int(item['number'])
            item["total"] = usd(total)
            total_price_list.append(total)

        # Find the total for all shares and cash
        grand_total = updated_cash + sum(total_price_list)
        return render_template("sold.html", owned_symbols=owned_symbols, owned_shares=owned_shares, cash=usd(updated_cash), grand_total=usd(grand_total))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", owned_symbols=owned_symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)