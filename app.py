from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session.__init__ import Session

#Configure app
app = Flask(__name__) #turn this file into a flask application

#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///brunches.db")

DISHTYPES = [
    "Carbohydrate",
    "Protein",
    "Fruit",
    "Beverage"
]

@app.route('/')
@app.route('/<name>')

def helloWorld(name="Cutie"):
    brunches = db.execute("SELECT * FROM brunches")
    return render_template("index.html", name=name, brunches=brunches)


@app.route('/create-event', methods=["POST", "GET"])
def createEvent():
    if request.method == "POST":
        # Validate submission
        name = request.form.get("event-name")
        date = request.form.get("event-date")
        time = request.form.get("event-time")
        location = request.form.get("event-location")
        if not name:
            return render_template("failure.html")

        db.execute("INSERT INTO brunches (name, date, time, location) VALUES(?, ?, ?, ?)", name, date, time, location)

        return redirect("brunch-list")
    return render_template("create-event.html")

@app.route('/brunch-list')
def brunchList():
    brunches = db.execute("SELECT * FROM brunches")
    return render_template("brunch-list.html", brunches=brunches)

@app.route('/add-dish')
@app.route('/add-dish/<id>', methods=["POST", "GET"])
def addDish(id):
    # if request.method == "POST":
        # Validate submission
    selectedId=id
    if not selectedId:
        return render_template("failure.html")

    first_name = request.form.get("first-name")
    last_name_form = request.form.get("last-name")
    dish_type_form = request.form.get("dish-type")
    dish_form = request.form.get("dish-name")
    if not first_name:
        return render_template("failure.html")
    # if not first_name_form or dish_type_form not in DISHTYPES:
    #     return render_template("failure.html")
    return "Selected ID is: {}".format(selectedId);

    # db.execute("INSERT INTO attendees (first_name, last_name, dish_type, dish) VALUES(?, ?, ?, ?)", first_name_form, last_name_form, dish_type_form, dish_form)

    # newAttendeeId=db.execute("SELECT id FROM attendees WHERE first_name=first_name_form AND last_name=last_name_form")

    # db.execute("INSERT INTO attendee_brunch (brunch_id, attendee_id) VALUES (?,?) selectedId, newAttendeeId")

    # return redirect("/guest-list")
    # return render_template("add-dish.html", dishtypes=DISHTYPES)

# @app.route('/guest-list')
# def guestList():
#     attendees = db.execute("SELECT * FROM attendees")
#     return render_template("guest-list.html", attendees=attendees)

@app.route('/guest-list')
@app.route('/guest-list/<id>', methods=["POST"])

def guestList(id):
    selectedId=id
    if not id:
            return render_template("failure.html")
    attendees = db.execute("SELECT first_name, last_name, dish_type, dish FROM attendees JOIN attendee_brunch ON attendees.id=attendee_brunch.attendee_id JOIN brunches ON brunches.id=attendee_brunch.brunch_id WHERE brunches.id = ?", selectedId)
    return render_template("guest-list.html", attendees=attendees)

@app.route('/delete-brunch', methods=["POST"])
def deleteBrunch():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM brunches WHERE id = ?", id)
    return redirect("brunch-list")

@app.route('/RSVP', methods=["POST"])
def rsvpBrunch():
    id = request.form.get("id")
    # if id:
    #     db.execute("DELETE FROM brunches WHERE id = ?", id)
    return redirect("guest-list")
