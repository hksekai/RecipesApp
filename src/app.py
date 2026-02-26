from flask import Flask, request, session
from uuid import uuid4

from .recipe_service import RecipeService
from .models import (
    init_db,
    record_user_recipe_view,
    link_recipe_to_ingredient,
    get_recipe_history_view,
    get_recipes_by_ingredient
)

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Required for session cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'

init_db(app)


@app.before_request
def assign_user_id():
    """
    Ensure each user has a unique session ID stored in a cookie.
    This session ID is used as the primary key for user tracking.
    """
    if 'user_id' not in session:
        session['user_id'] = str(uuid4())


@app.route("/")
def main():
    # Get user's view history for display
    user_history = get_recipe_history_view(session['user_id'])
    history_html = ""
    
    if user_history:
        history_html = "<h3>Your Viewed Recipes:</h3><ul>"
        for recipe in user_history:
            history_html += f"<li>{recipe.name}</li>"
        history_html += "</ul>"
    
    return f'''
     <h1>Recipe App</h1>
     <p>Enter a main ingredient to get a dish suggestion. Examples: chicken breast, beef, salmon</p>
     <form action="/get_recipe" method="POST">
         <input name="ingredient" placeholder="e.g., chicken breast">
         <input type="submit" value="Submit!">
     </form>
     {history_html}
     '''


@app.route("/get_recipe", methods=["POST"])
def echo_input():
    input_text = request.form.get("ingredient", "")
    recipe_data = RecipeService.get_recipe_by_main_ingredient(input_text)
    
    if recipe_data:
        # Record this recipe view in the database
        recipe = record_user_recipe_view(session['user_id'], recipe_data)
        
        # Link the recipe to the ingredient
        link_recipe_to_ingredient(recipe, input_text)
        
        # Build response with thumbnail if available
        thumbnail_html = ""
        if recipe.thumbnail:
            thumbnail_html = f'<br><img src="{recipe.thumbnail}" alt="{recipe.name}" style="max-width: 300px;">'
        
        return f"""
        <h2>Recipe Found: {recipe.name}</h2>
        {thumbnail_html}
        <br><br>
        <a href="/">Search Again</a>
        """
    else:
        return """
        <p>No recipe found for that ingredient.</p>
        <a href="/">Try Again</a>
        """


@app.route("/history")
def view_history():
    """
    View all recipes the current user has searched for.
    """
    user_history = get_recipe_history_view(session['user_id'])
    
    if not user_history:
        return """
        <h2>Your Recipe History</h2>
        <p>You haven't viewed any recipes yet.</p>
        <a href="/">Search for Recipes</a>
        """
    
    history_html = "<h2>Your Recipe History</h2><ul>"
    for recipe in user_history:
        thumbnail = f'<br><img src="{recipe.thumbnail}" style="max-width: 150px;">' if recipe.thumbnail else ""
        history_html += f"<li>{recipe.name}{thumbnail}</li>"
    history_html += '</ul><br><a href="/">Search for More Recipes</a>'
    
    return history_html


@app.route("/recipes-by-ingredient/<ingredient>")
def recipes_by_ingredient(ingredient):
    """
    View all recipes that contain a specific ingredient.
    """
    recipes = get_recipes_by_ingredient(ingredient)
    
    if not recipes:
        return f"""
        <h2>Recipes with {ingredient}</h2>
        <p>No recipes found with that ingredient.</p>
        <a href="/">Search Again</a>
        """
    
    recipes_html = f"<h2>Recipes with {ingredient}</h2><ul>"
    for recipe in recipes:
        thumbnail = f'<br><img src="{recipe.thumbnail}" style="max-width: 150px;">' if recipe.thumbnail else ""
        recipes_html += f"<li>{recipe.name}{thumbnail}</li>"
    recipes_html += '</ul><br><a href="/">Search Again</a>'
    
    return recipes_html
