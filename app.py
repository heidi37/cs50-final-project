from cs50 import SQL
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_session.__init__ import Session
import datetime

#Configure app
app = Flask(__name__) #turn this file into a flask application
app.config.from_pyfile('config.py')

db = SQL("sqlite:///brunches.db")

DISHTYPES = [
    "Carbohydrate",
    "Protein",
    "Fruit",
    "Beverage"
]

@app.route('/')
def index():
    brunches = db.execute("SELECT * FROM brunches")
    return render_template("index.html", brunches=brunches)

@app.route('/create-brunch', methods=["POST", "GET"])
def createEvent():
    if request.method == "POST":
        # Validate submission
        name = request.form.get("event-name")
        eventDate = request.form.get("event-date")
        time = request.form.get("event-time")
        location = request.form.get("event-location")

        date_obj = datetime.datetime.strptime(eventDate, "%Y-%m-%d")
        output_date = date_obj.strftime("%m-%d-%Y")

        time_obj = datetime.datetime.strptime(time, "%H:%M")
        output_time = time_obj.strftime("%I:%M %p")

        if not name:
            return render_template("failure.html")

        db.execute("INSERT INTO brunches (name, date, time, location) VALUES(?, ?, ?, ?)", name, output_date, output_time, location)

        return redirect("brunch-list")
    return render_template("create-brunch.html")

@app.route('/brunch-list')
def brunchList():
    today_obj = datetime.date.today()
    output_today = today_obj.strftime("%m-%d-%Y")
    brunches = db.execute("SELECT * FROM brunches WHERE date >= ?", output_today)
    return render_template("brunch-list.html", brunches=brunches)


@app.route('/add-guest/<id>', methods=["GET"])
def addDish(id):
    return render_template("add-guest.html", dishtypes=DISHTYPES, id=id)

@app.route('/dish-added/<id>', methods=["POST"])
def dishAdded(id):
        selectedId=id
        if not selectedId:
            return render_template("failure.html")

        first_name_form = request.form.get("first-name")
        last_name_form = request.form.get("last-name")
        dish_type_form = request.form.get("dish-type")
        dish_form = request.form.get("dish-name")

        if not first_name_form or dish_type_form not in DISHTYPES:
            return render_template("failure.html")

        db.execute("INSERT INTO attendees (first_name, last_name, dish_type, dish) VALUES(?, ?, ?, ?)", first_name_form, last_name_form, dish_type_form, dish_form)

        newAttendeeId=db.execute("SELECT id FROM attendees WHERE first_name=? AND last_name=?", first_name_form, last_name_form)
        db.execute("INSERT INTO attendee_brunch (brunch_id, attendee_id) VALUES (?,?)", selectedId, newAttendeeId[0]['id'])

        if dish_type_form == "Protein":
            db.execute("UPDATE brunches SET num_protein = num_protein + 1 WHERE id = ?", selectedId)
        if dish_type_form == "Carbohydrate":
            db.execute("UPDATE brunches SET num_carb = num_carb + 1 WHERE id = ?", selectedId)
        if dish_type_form == "Fruit":
            db.execute("UPDATE brunches SET num_fruit = num_fruit + 1 WHERE id = ?", selectedId)
        if dish_type_form == "Beverage":
            db.execute("UPDATE brunches SET num_bev = num_bev + 1 WHERE id = ?", selectedId)

        db.execute("UPDATE brunches SET num_attend = num_attend + 1 WHERE id = ?", selectedId)

        brunches = db.execute("SELECT * FROM brunches WHERE id = ?", selectedId)

        attendees = db.execute("SELECT * FROM attendees JOIN attendee_brunch ON attendees.id=attendee_brunch.attendee_id JOIN brunches ON brunches.id=attendee_brunch.brunch_id WHERE brunches.id = ?", selectedId)

        return render_template('success.html',selectedId=selectedId)

@app.route('/guest-list/<id>', methods=["POST","GET"])
def guestList(id):
    selectedId=id
    if not id:
            return render_template("failure.html")
    attendees = db.execute("SELECT * FROM attendees JOIN attendee_brunch ON attendees.id=attendee_brunch.attendee_id JOIN brunches ON brunches.id=attendee_brunch.brunch_id WHERE brunches.id = ?", selectedId)

    brunches = db.execute("SELECT * FROM brunches WHERE id = ?", selectedId)
    return render_template("guest-list.html", attendees=attendees, brunches=brunches)

@app.route('/delete-brunch', methods=["POST"])
def deleteBrunch():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM attendees WHERE id IN (SELECT attendee_id FROM attendee_brunch WHERE brunch_id = ?)", id)
        db.execute("DELETE FROM brunches WHERE id = ?", id)
    return redirect("brunch-list")

@app.route('/delete-dish', methods=["POST"])
def deleteDish():
    id = int(request.form.get("dish_id"))
    brunchId = int(request.form.get("brunch_id"))
    dish_type_form = request.form.get("dish_type")
    if id:
        db.execute("DELETE FROM attendees WHERE id = ?", id)

    if dish_type_form == "Protein":
        db.execute("UPDATE brunches SET num_protein = num_protein - 1 WHERE id = ?", brunchId)
    if dish_type_form == "Carbohydrate":
        db.execute("UPDATE brunches SET num_carb = num_carb - 1 WHERE id = ?", brunchId)
    if dish_type_form == "Fruit":
        db.execute("UPDATE brunches SET num_fruit = num_fruit - 1 WHERE id = ?", brunchId)
    if dish_type_form == "Beverage":
            db.execute("UPDATE brunches SET num_bev = num_bev - 1 WHERE id = ?", brunchId)

    db.execute("UPDATE brunches SET num_attend = num_attend - 1 WHERE id = ?", brunchId)

    return redirect(url_for("dishDeleted", id=brunchId))

@app.route('/guest-deleted/<id>')
def dishDeleted(id):
    selectedId=id
    if not id:
            return render_template("failure.html")
    attendees = db.execute("SELECT * FROM attendees JOIN attendee_brunch ON attendees.id=attendee_brunch.attendee_id JOIN brunches ON brunches.id=attendee_brunch.brunch_id WHERE brunches.id = ?", selectedId)

    brunches = db.execute("SELECT * FROM brunches WHERE id = ?", selectedId)

    return render_template("guest-deleted.html", attendees=attendees, brunches=brunches)
