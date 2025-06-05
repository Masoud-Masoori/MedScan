from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import pickle
import pandas as pd
import traceback

# Load model pipeline
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Define Pydantic model for input
class Features(BaseModel):
    features: List[float]

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Application Diabetes Classifier is running"}

@app.post("/predict")
async def predict(data: Features, request: Request):
    try:
        input_data = pd.DataFrame([data.features], columns=[
            "pregnancies", "glucose", "bloodpressure", "skinthickness",
            "insulin", "bmi", "diabetespedigreefunction", "age"
        ])
        print("📥 Received input:\n", input_data)

        prediction = model.predict(input_data)[0]
        return {"message": f"Predicted Age Class: {prediction}"}

    except Exception as e:
        traceback.print_exc()
        return {
            "error": str(e),
            "received_input": data.features
        }
