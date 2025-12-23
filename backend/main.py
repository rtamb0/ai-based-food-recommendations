from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",  # Vite default
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model/nutrition_risk_model.pkl")
feature_encoders = joblib.load("model/feature_encoders.pkl")
target_encoder = joblib.load("model/target_encoder.pkl")

FEATURES = [
    "Age", 
    "Height", 
    "Weight",
    "FCVC", # Do you usually eat vegetables in your meals?
    "FAVC", # Do you eat high caloric food frequently?
    "NCP", # How many main meals do you have daily?
    "CAEC", # Do you eat any food between meals?
    "CH2O", # How much water do you drink daily?
    "FAF", # How often do you have physical activity?
    "TUE", # How much time do you use technological devices such as cell phone, videogames, television, computer and others?
    "SMOKE", # Do you smoke?
    "CALC", # How often do you drink alcohol?
    "MTRANS", # Which transportation do you usually use?
    "SCC" # Do you monitor the calories you eat daily?
]

def infer_nutrient_risks(user_data, nutrition_risk):
    """
    Infers potential nutrient deficiencies or excesses
    using ML output + lifestyle and dietary behavior.
    """

    nutrient_risks = set()

    # ==============================
    # 1. ML-Based Global Risk
    # ==============================
    if nutrition_risk == "UNDER_NUTRITION":
        nutrient_risks.update([
            "Calorie deficiency",
            "Protein deficiency",
            "Iron deficiency",
            "Vitamin B12 deficiency",
            "Zinc deficiency"
        ])

    elif nutrition_risk == "OVER_NUTRITION":
        nutrient_risks.update([
            "Excess calorie intake",
            "High saturated fat intake",
            "Low fiber intake",
            "Micronutrient imbalance"
        ])

    # ==============================
    # 2. Vegetable Intake (FCVC)
    # ==============================
    if user_data["FCVC"] <= 1:
        nutrient_risks.update([
            "Low fiber intake",
            "Vitamin A deficiency",
            "Vitamin C deficiency",
            "Potassium deficiency"
        ])

    elif user_data["FCVC"] == 2:
        nutrient_risks.add("Suboptimal fiber intake")

    # ==============================
    # 3. Meal Regularity & Snacking
    # ==============================
    if user_data["NCP"] < 3:
        nutrient_risks.add("Inconsistent energy intake")
    if user_data["NCP"] < 3 and nutrition_risk == "UNDER_NUTRITION":
        nutrient_risks.add("Meal frequency insufficient for energy needs")

    if user_data["CAEC"] == "Frequently":
        nutrient_risks.update([
            "Unstable blood glucose risk",
            "Excess sugar intake"
        ])

    # ==============================
    # 4. Hydration (CH2O)
    # ==============================
    if user_data["CH2O"] < 2:
        nutrient_risks.update([
            "Inadequate hydration",
            "Electrolyte imbalance risk"
        ])

    # ==============================
    # 5. Physical Activity (FAF)
    # ==============================
    if user_data["FAF"] <= 1:
        nutrient_risks.update([
            "Poor metabolic health",
            "Low insulin sensitivity"
        ])

    elif user_data["FAF"] >= 3:
        nutrient_risks.add("Increased protein requirement")
        
    if nutrition_risk == "UNDER_NUTRITION" and user_data["FAF"] >= 2:
        nutrient_risks.add("Increased energy requirement")

    # ==============================
    # 6. Screen Time (TUE)
    # ==============================
    if user_data["TUE"] == 2:
        nutrient_risks.add("Sedentary lifestyle risk")

    # ==============================
    # 7. Smoking
    # ==============================
    if user_data["SMOKE"] == "yes":
        nutrient_risks.update([
            "Vitamin C deficiency",
            "Vitamin E deficiency"
        ])

    # ==============================
    # 8. Alcohol Consumption (CALC)
    # ==============================
    if user_data["CALC"] == "Frequently":
        nutrient_risks.update([
            "Magnesium deficiency",
            "Vitamin B1 deficiency",
            "Liver health risk"
        ])

    elif user_data["CALC"] == "Sometimes":
        nutrient_risks.add("Moderate alcohol intake")

    # ==============================
    # 9. Self-Calorie Monitoring (SCC)
    # ==============================
    if user_data["SCC"] == "no":
        nutrient_risks.add("Low dietary awareness")

    # ==============================
    # 10. Transportation (MTRANS)
    # ==============================
    if user_data["MTRANS"] == "Automobile":
        nutrient_risks.add("Low daily physical activity")
    elif user_data["MTRANS"] == "Motorbike":
        nutrient_risks.add("Mostly sedentary commuting")
    elif user_data["MTRANS"] == "Public_Transportation":
        nutrient_risks.add("Moderate incidental physical activity")
    elif user_data["MTRANS"] == "Walking":
        nutrient_risks.add("High incidental physical activity")

    if not nutrient_risks:
        nutrient_risks.add("No major nutritional risk detected")

    return sorted(nutrient_risks)

class YesNo(str, Enum):
    yes = "yes"
    no = "no"

class Frequency(str, Enum):
    no = "no"
    Sometimes = "Sometimes"
    Frequently = "Frequently"
    Always = "Always"
    
class Transportation(str, Enum):
    Walking = "Walking"
    Bicycle = "Bicycle"
    Automobile = "Automobile"
    Motorbike = "Motorbike"
    Public_Transportation = "Public_Transportation"
    
class UserInput(BaseModel):
    Age: int = Field(ge=1, le=125)
    Height: float = Field(ge=0.5, le=2.8)     # meters
    Weight: float = Field(ge=2, le=700)       # kg

    FCVC: int = Field(ge=1, le=3)
    FAVC: YesNo 
    NCP: int = Field(ge=1, le=4)
    CAEC: Frequency

    CH2O: float = Field(ge=1, le=3)
    FAF: int = Field(ge=0, le=3)
    TUE: int = Field(ge=0, le=2)

    SMOKE: YesNo
    CALC: Frequency
    MTRANS: Transportation
    SCC: YesNo

@app.post("/predict")
def predict(data: UserInput):
    df = pd.DataFrame([data.model_dump()])
    df = df[FEATURES]

    # Encode categoricals
    for col, encoder in feature_encoders.items():
        try:
            df[col] = encoder.transform(df[col])
        except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid value for {col}: {str(e)}"
            )

    # ML prediction
    pred = model.predict(df)[0]
    nutrition_risk = target_encoder.inverse_transform([pred])[0]

    # Rule-based nutrient inference
    nutrient_risks = infer_nutrient_risks(data.model_dump(), nutrition_risk)

    return {
        "nutrition_risk": nutrition_risk,
        "nutrient_risks": nutrient_risks
    }
