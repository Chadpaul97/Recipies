from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



# **************
#    Recipe Page
# **************
@app.route("/create_recipe")
def create_recipe():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    return render_template("create_recipe.html")


# **************
#     Add Recipe
# **************
@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    if Recipe.validate_recipe(request.form):
        data = {
            "name":request.form["name"],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "date":request.form["date"],
            "time":request.form["time"],
            "users_id":session["user_id"]
        }
        Recipe.save_recipe(data)
        flash("Recipe Added")
        return redirect('/userpage')
    else:
        return redirect("/create_recipe")

# ***************
#    Edit Recipes
# ***************

@app.route("/edit_recipe/<int:id>")
def edit_recipe(id):
    data = {
        "id":id
    }
    user_recipes= Recipe.get_one(data)
    return render_template("edit_recipe.html",user_recipes=user_recipes )

@app.route("/update_recipe/<int:id>", methods=["POST"])
def update_recipe(id):
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    if Recipe.validate_recipe(request.form):
        data = {
            "name":request.form["name"],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "date":request.form["date"],
            "time":request.form["time"],
            "id": id
        }
    Recipe.update_recipe(data)
    return redirect('/get_recipes')

# ****************
#   Delete Recipes
# ****************

@app.route("/delete/<int:id>")
def delete_recipe(id):
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect("/get_recipes")



# ***************
#    Show Recipes
# ***************
@app.route("/get_recipes")
def get_recipes():
    user_recipes = Recipe.get_recipes()
    return render_template("userpage.html", user_recipes=user_recipes)

# *******************
#    Show One Recipes
# *******************
@app.route("/show/<int:id>")
def show_recipe(id):
    data = {
        "id":id
    }
    user_recipes= Recipe.get_one(data)
    return render_template("show_recipe.html",user_recipes=user_recipes)