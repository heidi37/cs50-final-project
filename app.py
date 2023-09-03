from cs50 import SQL
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__) #turn this file into a flask application

db = SQL("sqlite:///brunches.db")

# ATTENDEES = {}

DISHTYPES = [
    "Carbohydrate",
    "Protein",
    "Fruit",
    "Beverage"
]

@app.route('/')
# @app.route('/<name>')

def hello_world(name="Cutie"):
    return render_template("index.html", name=name)

@app.route('/create-event', methods=["POST", "GET"])
def createEvent():
    return render_template("create-event.html")

@app.route('/add-guests', methods=["POST", "GET"])
def addGuests():
    return render_template("add-guests.html")

@app.route('/add-dish', methods=["POST", "GET"])
def addDish():
    if request.method == "POST":
        # Validate submission
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        dish_type = request.form.get("dish-type")
        dish = request.form.get("dish-name")
        if not first_name or dish_type not in DISHTYPES:
            return render_template("failure.html")

        db.execute("INSERT INTO attendees (first_name, last_name, dish_type, dish) VALUES(?, ?, ?, ?)", first_name, last_name, dish_type, dish)

        return redirect("/guest-list")
    return render_template("add-dish.html", dishtypes=DISHTYPES)

@app.route('/guest-list')
def guestList():
    return render_template("guest-list.html")
