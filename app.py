from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')

def hello_world(name="Cutie"):
    return render_template("index.html", name=name)

@app.route('/add/<int:num1>/<int:num2>')

def add(num1, num2):
    return render_template("add.html", num1=num1, num2=num2)
