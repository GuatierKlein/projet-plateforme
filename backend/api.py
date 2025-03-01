from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# 1️⃣ Activer CORS pour éviter l'erreur 405
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines (mettre le domaine spécifique en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, OPTIONS...)
    allow_headers=["*"],  # Autorise tous les headers
)

# 2️⃣ Charger les coefficients depuis le fichier CSV
coefficients = pd.read_csv("coefficients.csv")
coef_dict = dict(zip(coefficients["Variable"], coefficients["Coefficient"]))

# 3️⃣ Définir le modèle de données pour l'input utilisateur
class PredictionInput(BaseModel):
    bathrooms: float
    accomodate: int
    bedrooms: int
    beds: int
    room_type: str
    country: str

# 4️⃣ Fonction pour prédire un prix
def predict_price(input_data: PredictionInput):
    price = coef_dict["Intercept"]
    
    price += coef_dict["bathrooms"] * input_data.bathrooms
    price += coef_dict["accomodate"] * input_data.accomodate
    price += coef_dict["bedrooms"] * input_data.bedrooms
    price += coef_dict["beds"] * input_data.beds

    room_types = ["Shared room", "Hotel room"]
    for room in room_types:
        if input_data.room_type == room and room in coef_dict:
            price += coef_dict[room]

    countries = ["Australie", "Argentine", "Thaïlande", "USA", "Bresil", "France", "Japon", "Espagne"]
    for country in countries:
        if input_data.country == country and country in coef_dict:
            price += coef_dict[country]

    return price

# 5️⃣ Définir l'endpoint POST pour prédire le prix
@app.post("/predict")
async def predict(input_data: PredictionInput):
    print("input data : ", input_data)
    predicted_price = predict_price(input_data)
    return {"predicted_price": round(predicted_price, 2)}
