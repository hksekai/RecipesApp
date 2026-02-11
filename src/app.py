from flask import Flask, request
from .recipe_service import get_recipe_by_main_ingredient

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <h1>Recipe App</h1>
     <p>Enter a main ingredient to get a dish suggestion. Examples: chicken breast, beef, salmon</p>
     <form action="/get_recipe" method="POST">
         <input name="ingredient" placeholder="e.g., chicken breast">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/get_recipe", methods=["POST"])
def echo_input():
    input_text = request.form.get("ingredient", "")
    recipe = get_recipe_by_main_ingredient(input_text)
    if recipe:
        return f"Recipe found: {recipe.get('strMeal')}"
    else:
        return "No recipe found for that ingredient."
