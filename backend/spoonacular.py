import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com"

def search_recipes_by_ingredients(ingredients: list[str], number: int = 5):
    if not SPOONACULAR_API_KEY or not ingredients:
        return []

    params = {
        "ingredients": ",".join(ingredients),
        "number": number,
        "ranking": 2,          # prioritse ingredient match
        "ignorePantry": True,
        "apiKey": SPOONACULAR_API_KEY,
    }

    resp = requests.get(
        f"{BASE_URL}/recipes/findByIngredients",
        params=params,
        timeout=8,
    )

    if resp.status_code != 200:
        return []

    return resp.json()

def enrich_food_groups_with_spoonacular(food_groups: list[dict]):
    """
    food_groups example:
    [
      {
        "meal_type": "main",
        "ingredients": [{"name": "chicken breast"}, {"name": "rice"}]
      }
    ]
    """
    enriched_groups = []

    for group in food_groups:
        ingredient_names = [item["name"] for item in group["ingredients"]]

        recipes = search_recipes_by_ingredients(ingredient_names)
        
        MAX_MISSED = 4

        filtered = [
            recipe for recipe in recipes
            if recipe.get("missedIngredientCount", 0) <= MAX_MISSED
        ]

        enriched_groups.append({
            "meal_type": group["meal_type"],
            "ingredients": ingredient_names,
            "recipes": filtered,
        })

    return enriched_groups
