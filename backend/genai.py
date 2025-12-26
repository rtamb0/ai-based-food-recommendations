import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Literal

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": NutritionAdvice.model_json_schema(),
            "temperature": 0.2,
            "max_output_tokens": 4096,
        },
    )
    if response.parsed is None:
        raise RuntimeError(
            f"GenAI output truncated (finish_reason={response.candidates[0].finish_reason})"
        )
    return response.parsed
