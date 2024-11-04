from flask import Flask, redirect, url_for, render_template, logging, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(45))
    password = db.Column(db.String(50))

class note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reason = db.Column(db.String(1000), unique = True)

class info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    newname = db.Column(db.String(40), unique = True)
    mobilenum = db.Column(db.String(10), unique = True)    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        usrname = request.form["usrname"]
        pssword = request.form["pssword"]

        login = user.query.filter_by(username = usrname, password = pssword).first()
        if login is not None:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        usrname = request.form["usrname"]
        emailadds = request.form["emailadds"]
        pssword = request.form["pssword"]

        signup = user(username = usrname, email = emailadds, password = pssword)
        db.session.add(signup)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/adminpanel")
def admin():
    return render_template("adminpanel.html")

@app.route("/adminsignup")
def adminsignup():
    return render_template("adminsignup.html")

@app.route("/form", methods = ["GET", "POST"])
def form():
    if request.method == "POST":
        rson = request.form["rson"]
        uname = request.form["uname"]
        num = request.form["num"]

        form = note(reason = rson)
        form = info(newname = uname, mobilenum = num)
        db.session.add(form)
        db.session.commit()

        return redirect(url_for("about"))
    return render_template("form.html")

@app.route("/about")
def about():
    return render_template("about.html")

with app.app_context():
        
    db.create_all()
    app.run(debug = True)