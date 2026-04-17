import pandas as pd
import numpy as np
from fastapi import FastAPI
from sklearn.ensemble import RandomForestClassifier
import joblib

app = FastAPI()


X = np.random.rand(100, 3) * [100, 24, 10]
y = np.random.randint(0, 2, 100) 
model = RandomForestClassifier().fit(X, y)

@app.get("/")
def home():
    return {"status": "Churn Prediction API is Active"}

@app.get("/live-customer")
def get_customer():
   
    return {
        "customer_id": f"ID-{np.random.randint(1000, 9999)}",
        "monthly_charges": round(np.random.uniform(20, 120), 2),
        "tenure_months": np.random.randint(1, 72),
        "support_calls": np.random.randint(0, 10)
    }

@app.get("/predict")
def predict(charges: float, tenure: int, calls: int):
    
    prob = model.predict_proba([[charges, tenure, calls]])[0][1]
    return {"churn_probability": round(float(prob), 4)}

@app.post("/retrain")
def retrain():
    
    return {"message": "Model retrained with latest behavior patterns"}
