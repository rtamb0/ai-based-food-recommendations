import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Literal
import time
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class FoodItem(BaseModel):
    name: str
    reason: str

class FoodGroup(BaseModel):
    meal_type: Literal["breakfast", "main", "snack"]
    ingredients: List[FoodItem]

class NutritionAdvice(BaseModel):
    explanation: str
    nutrients: List[str]
    food_groups: List[FoodGroup]
    
def normalize_food_groups(food_groups: List[FoodGroup]) -> List[FoodGroup]:
    merged = {}

    for group in food_groups:
        meal = group.meal_type

        if meal not in merged:
            merged[meal] = {
                "meal_type": meal,
                "ingredients": {}
            }

        for item in group.ingredients:
            # Avoid duplicate ingredients by name
            if item.name not in merged[meal]["ingredients"]:
                merged[meal]["ingredients"][item.name] = item.reason

    return [
        FoodGroup(
            meal_type=meal,
            ingredients=[
                FoodItem(name=name, reason=reason)
                for name, reason in data["ingredients"].items()
            ]
        )
        for meal, data in merged.items()
    ]

def call_gemini_with_retry(prompt: str, max_retries: int = 2):
    for attempt in range(max_retries + 1):
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": NutritionAdvice.model_json_schema(),
                    "temperature": 0.2,
                    "max_output_tokens": 4096,
                },
            )

        except ResourceExhausted:
            if attempt >= max_retries:
                raise RuntimeError("Gemini rate limit exceeded")
            time.sleep(2 ** attempt)

        except ServiceUnavailable:
            if attempt >= max_retries:
                raise RuntimeError("Gemini temporarily unavailable")
            time.sleep(2 ** attempt)

def generate_ai_recommendation(nutrition_risk, nutrient_risks, user_context):
    prompt = f"""
    You are a nutrition assistant.

    User context:
    - Age: {user_context['Age']}
    - Activity level (FAF scale 0–3): {user_context['FAF']}
    - Nutrition risk: {nutrition_risk}
    - Nutrient risks: {', '.join(nutrient_risks)}

    Tasks:
    1. Explain the nutrition risks simply
    2. Identify nutrients to prioritize
    3. Suggest foods grouped by compatible meal usage.

    Food grouping rules:
    - Group foods that naturally go together
    - Each group should represent ONE possible meal or eating context
    - Each food must be a specific ingredient searchable in the Spoonacular API
    - Avoid abstract categories (no "vegetables", "healthy fats")

    Meal types allowed:
    - breakfast
    - main
    - snack

    Output structure:
    - food_groups: list of groups
    - Each group has:
    - meal_type
    - ingredients (name + reason)

    Do NOT generate recipes.
    Do NOT combine incompatible foods.

    Rules:
    - No recipes
    - No medical advice
    - No URLs
    - Simple, non-clinical language
    """

    try:
        response = call_gemini_with_retry(prompt)
        print("Gemini response received" + str(response))
    except RuntimeError:
        return NutritionAdvice(
            explanation="We could not generate personalized advice at the moment.",
            nutrients=[],
            food_groups=[]
        )

    if response.parsed is None:
        raise RuntimeError(
            f"GenAI output truncated (finish_reason={response.candidates[0].finish_reason})"
        )
    
    raw = response.parsed

    parsed = NutritionAdvice.model_validate(raw)
    parsed.food_groups = normalize_food_groups(parsed.food_groups)
    print("GenAI response:", parsed)
    
    return parsed.model_dump()

