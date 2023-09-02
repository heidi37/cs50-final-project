from flask import Flask, render_template, request

app = Flask(__name__) #turn this file into a flask application

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
