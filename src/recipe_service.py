import requests


TEST_API_KEY = "1" # Test api key
MEALDB_BASE_URL = f"https://www.themealdb.com/api/json/v1/{TEST_API_KEY}/"
# For free API usage we can only use a single main ingredient. The hope was to use a list of ingredients but for now in the MVP stage we'll settle for a single ingredient, i.e chicken_breast
def get_recipe_by_main_ingredient(main_ingredient):
    """
    Fetches recipe details from TheMealDB by recipe name.
    """
    response = requests.get(f"{MEALDB_BASE_URL}/filter.php?i={main_ingredient}")
    data = response.json()
    
    if data and data.get("meals"):
        # TheMealDB API returns a list of meals, we'll take the first one.
        return data["meals"][0] 
    else:
        return None # No recipe found