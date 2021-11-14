from flask_app.config.mysqlconnection import connectToMySQL
from .user import User
from flask import flash



class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date = data["date"]
        self.time = data["time"]
        self.users_id = data["users_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = []
# *******************
#    Validate Recipe
# *******************

    @staticmethod
    def validate_recipe(textinput):
        is_valid = True
        if len(textinput["name"]) < 3:
            flash("Name required! At least 3 Characters")
            is_valid = False
        if len(textinput["description"]) < 3:
            flash("Description needed! At least 3 Characters")
            is_valid = False
        if len(textinput["instructions"]) < 3:
            flash("Instructions needed! At least 3 Characters")
            is_valid = False
        return is_valid


# **************
#    Save Recipe
# **************
    @classmethod
    def save_recipe(cls,data):
        query="INSERT into recipes (name,description,instructions,date,time,users_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(date)s,%(time)s,%(users_id)s)"
        return connectToMySQL("recipes").query_db(query,data)

# ***************
#    Get Recipes
# ***************

    @classmethod
    def get_recipes(cls):
        query= "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.users_id"
        results = connectToMySQL("recipes").query_db(query)
        user_recipes = []
        for r in results:
            recipe_instance = Recipe(r)
            user_data = {
                "id":r["users.id"],
                "first_name":r["first_name"],
                "last_name":r["last_name"],
                "email":r["email"],
                "password":r["password"],
                "created_at":r["created_at"],
                "updated_at":r["updated_at"]
            }
            recipe_instance.user = User(user_data)
            user_recipes.append(recipe_instance)
        return user_recipes

# *******************
#    Show One Recipes
# *******************


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.users_id WHERE recipes.id = %(id)s"
        results = connectToMySQL("recipes").query_db(query,data)
        recipe = cls(results[0])
        user_data = {
            "id" : results[0]['users.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at']
        }
        recipe.user = User(user_data)
        return recipe

# ***************
#    Edit Recipes
# ***************

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s, instructions=%(instructions)s,date=%(date)s,time=%(time)s, updated_at=NOW() WHERE id = %(id)s"
        results = connectToMySQL("recipes").query_db(query,data)
        return


# ****************
#   Delete Recipes
# ****************
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL("recipes").query_db(query,data)