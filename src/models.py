'''
Define the database model
that is used to store 
the recipe.
'''

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class UserSession(db.Model):
    """
    Stores unique user sessions using session_id from cookie as the primary key.
    """
    __tablename__ = 'user_sessions'
    
    session_id = db.Column(db.String(255), primary_key=True)
    
    recipes = db.relationship('UserRecipe', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<UserSession {self.session_id}>"


class Recipe(db.Model):
    """
    Stores recipe details from TheMealDB API.
    """
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    mealdb_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_views = db.relationship('UserRecipe', back_populates='recipe', cascade='all, delete-orphan')
    ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Recipe {self.name}>"


class UserRecipe(db.Model):
    """
    Association table linking UserSession to Recipe.
    Tracks which users have viewed which recipes.
    """
    __tablename__ = 'user_recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), db.ForeignKey('user_sessions.session_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('UserSession', back_populates='recipes')
    recipe = db.relationship('Recipe', back_populates='user_views')
    
    def __repr__(self):
        return f"<UserRecipe {self.session_id} -> {self.recipe_id}>"


class Ingredient(db.Model):
    """
    Stores unique ingredients.
    """
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    recipes = db.relationship('RecipeIngredient', back_populates='ingredient', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Ingredient {self.name}>"


class RecipeIngredient(db.Model):
    """
    Association table linking Recipe to Ingredient.
    Maps ingredients to recipes (many-to-many).
    """
    __tablename__ = 'recipe_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    
    recipe = db.relationship('Recipe', back_populates='ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipes')
    
    def __repr__(self):
        return f"<RecipeIngredient {self.recipe_id} -> {self.ingredient_id}>"


def init_db(app):
    """
    Initialize the database with the Flask app.
    Creates all tables.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()


def get_or_create_user_session(session_id):
    """
    Get existing user session or create a new one.
    """
    user_session = UserSession.query.get(session_id)
    if not user_session:
        user_session = UserSession(session_id=session_id)
        db.session.add(user_session)
        db.session.commit()
    return user_session


def get_or_create_recipe(mealdb_id, name, thumbnail=None):
    """
    Get existing recipe or create a new one.
    """
    recipe = Recipe.query.filter_by(mealdb_id=mealdb_id).first()
    if not recipe:
        recipe = Recipe(mealdb_id=mealdb_id, name=name, thumbnail=thumbnail)
        db.session.add(recipe)
        db.session.commit()
    return recipe


def get_or_create_ingredient(name):
    """
    Get existing ingredient or create a new one.
    """
    ingredient = Ingredient.query.filter_by(name=name.lower().strip()).first()
    if not ingredient:
        ingredient = Ingredient(name=name.lower().strip())
        db.session.add(ingredient)
        db.session.commit()
    return ingredient


def record_user_recipe_view(session_id, recipe_data):
    """
    Record that a user viewed a recipe.
    Creates session and recipe if they don't exist.
    """
    # Get or create user session
    user = get_or_create_user_session(session_id)
    
    # Get or create recipe
    recipe = get_or_create_recipe(
        mealdb_id=recipe_data.get('idMeal'),
        name=recipe_data.get('strMeal'),
        thumbnail=recipe_data.get('strMealThumb')
    )
    
    # Check if this view already exists
    existing = UserRecipe.query.filter_by(
        session_id=session_id,
        recipe_id=recipe.id
    ).first()
    
    if not existing:
        user_recipe = UserRecipe(session_id=session_id, recipe_id=recipe.id)
        db.session.add(user_recipe)
        db.session.commit()
    
    return recipe


def link_recipe_to_ingredient(recipe, ingredient_name):
    """
    Link a recipe to an ingredient.
    """
    ingredient = get_or_create_ingredient(ingredient_name)
    
    existing = RecipeIngredient.query.filter_by(
        recipe_id=recipe.id,
        ingredient_id=ingredient.id
    ).first()
    
    if not existing:
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id
        )
        db.session.add(recipe_ingredient)
        db.session.commit()
    
    return ingredient


def get_recipes_by_ingredient(ingredient_name):
    """
    Get all recipes that are indexed by main ingredient.
    """
    ingredient = Ingredient.query.filter_by(name=ingredient_name.lower().strip()).first()
    if ingredient:
        return [ri.recipe for ri in ingredient.recipes]
    return []


def get_recipe_history_view(session_id):
    """
    Get all the recipes that have been viewed by this session id.
    """
    user = UserSession.query.get(session_id)
    if user:
        return [ur.recipe for ur in user.recipes]
    return []
