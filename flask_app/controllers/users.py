from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ***************
#   Home Page
# ***************
@app.route("/")
def index():
    return render_template("index.html")

# *******************
#   Register User
# *******************
@app.route("/register_user", methods=["POST"])
def register_user():
    if User.validate_form(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash
        }
        user_db = User.user_email(data)
        if user_db:
            flash("User Exist")
            return redirect("/")

        user_id = User.add_user(data)
        session["user_id"] = user_id
        flash("User added!")
        return redirect("/")
    else:
        return redirect("/")


# ***************
#    Login User 
# ***************
@app.route("/login_user", methods=["POST"])
def login_user():
    if User.validate_user_login(request.form):
        data ={
            "email":request.form["email"]
        }
        user_db = User.user_email(data)

        if not user_db:
            flash("Invalid Email/Password")
            return redirect("/")
        if not (user_db.password,request.form["password"]):
            flash("Invalid Email/Password")
            return redirect("/")
        session["user_id"] = user_db.id
        session["first_name"] = user_db.first_name
        return redirect("/userpage")
    else:
        return redirect("/")

# ***************
#    Logout User
# ***************
@app.route("/logout_user")
def logout():
    session.clear()
    flash("logged out!")
    return redirect("/")



# **************
#    User Page
# **************
@app.route("/userpage")
def userpage():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    return redirect("/get_recipes")

