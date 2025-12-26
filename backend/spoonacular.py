import os
import requests
from dotenv import load_dotenv
import time
import logging

logger = logging.getLogger(__name__)

NEAR_LIMIT_THRESHOLD = 5  # requests remaining

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com"

def search_recipes_by_ingredients(ingredients: list[str], number: int = 5, retries: int = 2):
    if not SPOONACULAR_API_KEY or not ingredients:
        return []

    params = {
        "ingredients": ",".join(ingredients),
        "number": number,
        "ranking": 2,          # prioritse ingredient match
        "ignorePantry": True,
        "apiKey": SPOONACULAR_API_KEY,
    }

    for attempt in range(retries + 1):
        resp = requests.get(
            f"{BASE_URL}/recipes/findByIngredients",
            params=params,
            timeout=8,
        )

        # --- Rate limit hit ---
        if resp.status_code in (402, 429):
            logger.warning("Spoonacular rate limit reached.")
            return []

        # --- Near rate limit ---
        quota_left = resp.headers.get("X-API-Quota-Left")
        if quota_left is not None:
            try:
                if int(quota_left) <= NEAR_LIMIT_THRESHOLD:
                    logger.warning(
                        f"Spoonacular near rate limit: {quota_left} left"
                    )
            except ValueError:
                pass

        # --- Success ---
        if resp.status_code == 200:
            return resp.json()

        # --- Retry on transient errors ---
        if resp.status_code >= 500 and attempt < retries:
            time.sleep(2 ** attempt)
            continue

        break

    return []

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
