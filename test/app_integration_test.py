"""
Integration tests using coftest as the test client
"""

from unittest.mock import patch
from src.recipe_service import RecipeService
from src.models import Recipe, UserSession, UserRecipe


class TestRecipeSearchIntegration:
    def test_recipe_search_success(self, client, session_id):
        # Mock result of first entry in meals[0] from TheMealDB
        mock_recipe_data = {
            "idMeal": "52771",
            "strMeal": "Spicy Arrabiata Penne",
            "strMealThumb": "https://www.themealdb.com/images/media/meals/ustsqw1468250014.jpg"
        } 
        
        with client.session_transaction() as sess:
            sess["user_id"] = session_id
        
        with patch.object(RecipeService, "get_recipe_by_main_ingredient", return_value=mock_recipe_data):
            response = client.post("/get_recipe", data={"ingredient": "penne"})
        
        # Check the response data
        assert response.status_code == 200
        assert b"Spicy Arrabiata Penne" in response.data
        assert b"Search Again" in response.data
        
        # Check the db has added an entry
        recipe = Recipe.query.filter_by(mealdb_id="52771").first()
        assert recipe is not None
        assert recipe.name == "Spicy Arrabiata Penne"
        
        # Check the session was created
        user = UserSession.query.get(session_id)
        assert user is not None
        
        # Check a recipe was recorded
        view = UserRecipe.query.filter_by(session_id=session_id, recipe_id=recipe.id).first()
        assert view is not None