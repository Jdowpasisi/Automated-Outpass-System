from flask import Flask, redirect, url_for, render_template, logging, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user, login_required, login_user, current_user
from flask_mail import Mail, Message  
import sqlite3
import flask_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "29384c28rf98d784238h33h3h3dshbse13bbd32"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'email same as below'
app.config['MAIL_PASSWORD'] = '2 factor authentication key not gmail password'
app.config['MAIL_DEFAULT_SENDER'] = 'email'
mail = Mail(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(45))
    password = db.Column(db.String(50))

class outpass(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    mobile = db.Column(db.String(10))
    email_add = db.Column(db.String(50), nullable = False)
    hostel_name = db.Column(db.String(30))
    hostel_number = db.Column(db.String(15))
    date = db.Column(db.String(30))
    leaving_date = db.Column(db.String(30))
    place = db.Column(db.String(50))
    leaving_time = db.Column(db.String(15))
    return_time = db.Column(db.String(15))
    parent_mobile = db.Column(db.String(10))
    program = db.Column(db.String(20))
    reason = db.Column(db.String(1000))
    status = db.Column(db.String(20), default = 'pending')

class admnuser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    admin_name = db.Column(db.String(30), unique = True, nullable = False)
    admin_email = db.Column(db.String(50), unique = True, nullable = False)
    passkey = db.Column(db.String(60), unique = True, nullable = False)
    
@app.route("/")
def home():
    return render_template("index.html", username = current_user.username if current_user.is_authenticated else None)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        usrname = request.form["usrname"]
        pssword = request.form["pssword"]

        login = user.query.filter_by(username = usrname, password = pssword).first()
        if login is not None:
            flash("logged-in sucsess", category = "success")
            login_user(login)
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

        adminlogin = admnuser.query.filter_by(admin_email = emailaddrs, passkey = psskey).first()
        if adminlogin is not None:
            return redirect(url_for("admin"))
        flash("something invalid", category="error")
    return render_template("adminlogin.html")

@app.route("/form", methods = ["GET", "POST"])
def form():
    if request.method == "POST":
        uname = request.form["uname"]
        num = request.form["num"]
        mail = request.form["mail"]
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

        form = outpass(name = uname, mobile = num, email_add = mail, hostel_name = hname, hostel_number = hnum, date = tarikh, leaving_date = ldate, place = vplace, leaving_time = ltime, return_time = ctime, parent_mobile = pnum, program = prgm, reason = rson)
        db.session.add(form)
        db.session.commit()

        return redirect(url_for("about"))
    return render_template("form.html")

@app.route('/approve/<int:id>', methods = ['POST'])
def approved_mail(id):
    outpass_ord = outpass.query.get(id)
    if outpass_ord:
        outpass_ord.status = 'approved'
        db.session.commit()

        send_mail(outpass_ord.email_add, outpass_ord.name)

    return redirect(url_for("admin"))

@app.route('/reject/<int:id>', methods = ['POST'])
def rejected_mail(id):
    outpass_ord = outpass.query.get(id)
    if outpass_ord:
        outpass_ord.status = 'rejected'
        db.session.commit()

    return redirect(url_for("admin"))

def send_mail(student_email, student_name):
    subject = "Your outpass has been approved"
    body = f"Hello {student_name}, \n\n Your application has been approved, Thank you."

    msg = Message(subject, recipients = [student_email])
    msg.body = body

    try:
        mail.send(msg)
        print(f"mail sent to {student_email}")
    except Exception as e:
        print(f"fail to send email {str(e)}")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html"), 404                 

@app.route("/about")
def about():
    return render_template("about.html")

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

with app.app_context():

    db.create_all()
    app.run(debug = True)