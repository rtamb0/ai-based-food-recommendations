import json
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={
        "temperature": 0.2,
        "top_p": 0.8,
        "max_output_tokens": 512
    }
)

def parse_llm_json(text: str):
    try:
        text = text.strip()

        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("{"):
                    return json.loads(part)

        return json.loads(text)
    except Exception as e:
        print("LLM parse error:", e)
        print("Raw response:", text)
        return {
            "explanation": "Unable to generate explanation at this time.",
            "nutrients": [],
            "food_categories": []
        }


def generate_ai_recommendation(nutrition_risk, nutrient_risks, user_context):
    prompt = f"""
    Return ONLY raw JSON.
    Do NOT include markdown, comments, or extra text.

    User context:
    - Age: {user_context['Age']}
    - Activity level (FAF scale: 0=very low, 1=low, 2=moderate, 3=high): {user_context['FAF']}
    - Nutrition risk: {nutrition_risk}
    - Nutrient risks: {', '.join(nutrient_risks)}

    You are a nutrition assistant.

    Rules:
    - Do NOT generate recipes
    - Do NOT generate images
    - Do NOT generate URLs
    - Do NOT give medical advice
    - Use simple, non-clinical language
    - Output MUST be valid JSON

    Task:
    1. Explain the user's nutrition risks simply
    2. Identify nutrients that should be prioritized
    3. Suggest general food categories only

    JSON format:
    {{
    "explanation": "string",
    "nutrients": ["string"],
    "food_categories": ["string"]
    }}
    
    Return ONLY raw JSON.
    The response must start with "{" and end with "}".

    """
    response = model.generate_content(prompt)
    return parse_llm_json(response.text)
