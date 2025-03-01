from fastapi import FastAPI
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# 1️⃣ Charger les coefficients depuis le fichier CSV
coefficients = pd.read_csv("coefficients.csv")
coef_dict = dict(zip(coefficients["Variable"], coefficients["Coefficient"]))

# 2️⃣ Définir le modèle de données pour l'input utilisateur
class PredictionInput(BaseModel):
    bathrooms: float
    accomodate: int
    bedrooms: int
    beds: int
    country_encoding: dict  # Exemple : {"pays_USA": 1, "pays_France": 0}

# 3️⃣ Fonction pour prédire un prix
def predict_price_linear(input_data: PredictionInput):
    # Commencer avec l'intercept
    price = coef_dict["Intercept"]
    
    # Ajouter les contributions des variables numériques
    price += coef_dict["bathrooms"] * input_data.bathrooms
    price += coef_dict["accomodate"] * input_data.accomodate
    price += coef_dict["bedrooms"] * input_data.bedrooms
    price += coef_dict["beds"] * input_data.beds

    # Ajouter la contribution du pays encodé
    for key, value in input_data.country_encoding.items():
        if key in coef_dict:
            price += coef_dict[key] * value

    return price

# 4️⃣ Définir l'endpoint POST pour prédire le prix
@app.post("/predict")
async def predict(input_data: PredictionInput):
    predicted_price = predict_price_linear(input_data)
    return {"predicted_price": round(predicted_price, 2)}
