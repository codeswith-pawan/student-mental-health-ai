from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Mental_Health_Model.pkl"

model = joblib.load(MODEL_PATH)


app = FastAPI(
    title="Student Mental Health Prediction API",
    description="Predict Mental Health Score from student social-media and lifestyle features.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentData(BaseModel):
    Age: float = Field(..., ge=0)
    Gender: str
    Country: str
    Academic_Level: str
    Most_Used_Platform: str
    Purpose_Of_Use: str

    Avg_Daily_Usage_Hours: float = Field(..., ge=0)
    Daily_Unlocks: float = Field(..., ge=0)
    Study_Hours: float = Field(..., ge=0)
    Physical_Activity_Hours: float = Field(..., ge=0)
    Sleep_Hours_Per_Night: float = Field(..., ge=0)

    Stress_Level: str


@app.get("/")
def greet():
    return {
        "message": "Student Mental Health Prediction API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: StudentData):

    top10_country = {
        "Other",
        "India",
        "USA",
        "Canada",
        "Australia",
        "UK",
        "Germany",
        "Mexico",
        "Turkey",
        "France"
    }

    group_country = (
        data.Country
        if data.Country in top10_country
        else "Other"
    )

    input_data = pd.DataFrame([{
        "Study_Hours": data.Study_Hours,
        "Age": data.Age,
        "Avg_Daily_Usage_Hours": data.Avg_Daily_Usage_Hours,
        "Daily_Unlocks": data.Daily_Unlocks,
        "Physical_Activity_Hours": data.Physical_Activity_Hours,
        "Sleep_Hours_Per_Night": data.Sleep_Hours_Per_Night,
        "Stress_Level": data.Stress_Level,
        "Gender": data.Gender,
        "Country": data.Country,
        "Academic_Level": data.Academic_Level,
        "Most_Used_Platform": data.Most_Used_Platform,
        "Purpose_Of_Use": data.Purpose_Of_Use,
        "Group_country": group_country
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_mental_health_score": round(float(prediction), 2)
    }