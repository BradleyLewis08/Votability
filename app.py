from flask import Flask, session, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://zxrxhxukltcqii:5d703cb2bba4ed23a3a3c7bcc6c97eeaa5823861794c6c458abb137843a8d83b@ec2-23-23-36-227.compute-1.amazonaws.com:5432/dd99q3btjrrfa4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zxrxhxukltcqii:5d703cb2bba4ed23a3a3c7bcc6c97eeaa5823861794c6c458abb137843a8d83b@ec2-23-23-36-227.compute-1.amazonaws.com:5432/dd99q3btjrrfa4'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(128))
db.create_all()
db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first() != None:
            return render_template("signup.html", error="Email already exists.")
        else:    
            user = User(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            session["logged_in"] = True
            return redirect("/")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", error="")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first() == None:
            return render_template("login.html", error="Invalid Credentials")
        else:
            if User.query.filter_by(email=email).first().password != password:
                return render_template("login.html", error="Invalid credentials")
            else:
                session["logged_in"] = True
                session["name"] = User.query.filter_by(email=email).first().name
                session["email"] = email
                return redirect("/profile")

@app.route("/profile", methods=['GET'])
def profile():
    if "logged_in" not in session:
        return redirect("/login")
    else:
        if request.method == 'GET':
            return render_template("profile.html")

@app.route("/logout", methods=['GET'])
def logout():
    session.pop("logged_in")
    return redirect("/")

@app.route("/parties", methods=['GET'])
def parties():
    return render_template("parties.html")

@app.route("/navigation", methods=['GET'])
def navigation():
    return render_template("navigation.html")

@app.route("/polling", methods=['GET'])
def polling():
    return render_template("polling.html")

@app.route("/finance", methods=['GET'])
def finance():
    return render_template("finance.html")

@app.route("/local", methods=['GET'])
def local():
    return render_template("local.html")

@app.route("/community", methods=['GET'])
def community():
    return render_template("community.html")

@app.route("/candidates", methods=['GET'])
def candidates():
    return render_template("candidates.html")

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

