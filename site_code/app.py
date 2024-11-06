from flask import Flask, redirect, url_for, render_template, logging, request, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(45))
    password = db.Column(db.String(50))

class outpass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True)
    mobile = db.Column(db.String(10), unique = True)
    hostel_name = db.Column(db.String(30), unique = True)
    hostel_number = db.Column(db.String(15), unique = True)
    date = db.Column(db.String(30), unique = True)
    leaving_date = db.Column(db.String(30), unique = True)
    place = db.Column(db.String(50), unique = True)
    leaving_time = db.Column(db.String(15), unique = True)
    return_time = db.Column(db.String(15), unique = True)
    parent_mobile = db.Column(db.String(10), unique = True)
    program = db.Column(db.String(20), unique = True)
    reason = db.Column(db.String(1000), unique = True)

class admnuser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    admin_name = db.Column(db.String(30), unique = True, nullable = False)
    admin_email = db.Column(db.String(50), unique = True, nullable = False)
    passkey = db.Column(db.String(60), unique = True, nullable = False)
    
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
    users = outpass.query.all()
    return render_template("adminpanel.html", users = users)

@app.route("/adminsignup", methods = ["GET", "POST"])
def adminsignup():
    if request.method == "POST":
        admname = request.form["admname"]
        emailaddrs = request.form["emailaddrs"]
        psskey = request.form["psskey"]

        adminsignup = admnuser(admin_name = admname, admin_email = emailaddrs, passkey = psskey)
        db.session.add(adminsignup)
        db.session.commit()

        return redirect(url_for("adminlogin"))
    return render_template("adminsignup.html")

@app.route("/adminlogin", methods = ["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        emailaddrs = request.form["emailaddrs"]
        psskey = request.form["psskey"]

        login = admnuser.query.filter_by(admin_email = emailaddrs, passkey = psskey).first()
        if adminlogin is not None:
            return redirect(url_for("admin"))
    return render_template("adminlogin.html")

@app.route("/form", methods = ["GET", "POST"])
def form():
    if request.method == "POST":
        uname = request.form["uname"]
        num = request.form["num"]
        hname = request.form["hname"]
        hnum = request.form["hnum"]
        tarikh = request.form["tarikh"]
        ldate = request.form["ldate"]
        vplace = request.form["vplace"]
        ltime = request.form["ltime"]
        ctime = request.form["ctime"]
        pnum = request.form["pnum"]
        prgm = request.form["prgm"]
        rson = request.form["rson"]

        form = outpass(name = uname, mobile = num, hostel_name = hname, hostel_number = hnum, date = tarikh, leaving_date = ldate, place = vplace, leaving_time = ltime, return_time = ctime, parent_mobile = pnum, program = prgm, reason = rson)
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