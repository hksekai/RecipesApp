#!/usr/bin/env python3
'''
Import unittest framework and the recipe service function
we are testing. Also import mock for mocking HTTP requests.
'''
import unittest
from unittest.mock import MagicMock
from src.recipe_service import RecipeService


class TestRecipeService(unittest.TestCase):
    '''
    setUp function is used to instantiate the object we are testing.
    '''
    def setUp(self):
        self.recipe_service = RecipeService()
        # return the mocked first result from TheMealDB result.meals
        self.recipe_service.get_recipe_by_main_ingredient = MagicMock(return_value = {
            "idMeal": "52771",
            "strMeal": "Spicy Arrabiata Penne",
            "strMealThumb": "https://www.themealdb.com/images/media/meals/ustsqw1468250014.jpg"
        })

    '''
    Test get the recipe successfully
    '''
    def test_get_recipe_by_main_ingredient_success(self):
        result = self.recipe_service.get_recipe_by_main_ingredient("penne")

        self.assertIsNotNone(result)
        
        self.assertEqual(result["idMeal"], "52771")
        self.assertEqual(result["strMeal"], "Spicy Arrabiata Penne")

if __name__ == '__main__':
    unittest.main()
