from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Activer CORS pour éviter l'erreur 405
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines (mettre le domaine spécifique en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, OPTIONS...)
    allow_headers=["*"],  # Autorise tous les headers
)

# Charger les coefficients depuis le fichier CSV
coefficients = pd.read_csv("coefficients_withreviews.csv")
coef_dict = dict(zip(coefficients["Variable"], coefficients["Coefficient"]))

# Définir le modèle de données pour l'input utilisateur
class PredictionInput(BaseModel):
    bathrooms: float
    accomodate: int
    bedrooms: int
    beds: int
    room_type: str
    country: str

class PredictionInputWithReview(BaseModel):
    bathrooms: float
    accomodate: int
    bedrooms: int
    beds: int
    room_type: str
    country: str
    review_scores_rating : float
    review_scores_accuracy : float
    review_scores_cleanliness : float
    review_scores_checkin : float
    review_scores_communication : float
    review_scores_location : float

# Fonction pour prédire un prix
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

# Fonction pour prédire un prix avec review
def predict_price_review(input_data: PredictionInputWithReview):
    price = coef_dict["Intercept"]
    
    price += coef_dict["bathrooms"] * input_data.bathrooms
    price += coef_dict["accomodate"] * input_data.accomodate
    price += coef_dict["bedrooms"] * input_data.bedrooms
    price += coef_dict["review_scores_rating"] * input_data.review_scores_rating
    price += coef_dict["review_scores_accuracy"] * input_data.review_scores_accuracy
    price += coef_dict["review_scores_cleanliness"] * input_data.review_scores_cleanliness
    price += coef_dict["review_scores_checkin"] * input_data.review_scores_checkin
    price += coef_dict["review_scores_communication"] * input_data.review_scores_communication
    price += coef_dict["review_scores_location"] * input_data.review_scores_location

    room_types = ["Shared room", "Hotel room"]
    for room in room_types:
        if input_data.room_type == room and room in coef_dict:
            price += coef_dict[room]

    countries = ["Australie", "Argentine", "Thaïlande", "USA", "Bresil", "France", "Japon", "Espagne"]
    for country in countries:
        if input_data.country == country and country in coef_dict:
            price += coef_dict[country]

    return price

# Définir l'endpoint POST pour prédire le prix
@app.post("/predict")
async def predict(input_data: PredictionInput):
    print("input data : ", input_data)
    predicted_price = predict_price(input_data)
    return {"predicted_price": round(predicted_price, 2)}

# Définir l'endpoint POST pour prédire le prix
@app.post("/predict_with_reviews")
async def predict_review(input_data: PredictionInputWithReview):
    print("input data : ", input_data)
    predicted_price = predict_price_review(input_data)
    return {"predicted_price": round(predicted_price, 2)}
