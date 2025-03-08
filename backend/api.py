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
coefficients = pd.read_csv("coef_poly_noreview.csv")
neighbourhood_prices = pd.read_csv("neighbourhood_prices.csv")
property_prices = pd.read_csv("property_prices.csv")
coef_dict = dict(zip(coefficients["Variable"], coefficients["Coeff."]))
neighbourhood_dict = dict(zip(neighbourhood_prices["neighbourhood"], neighbourhood_prices["Mean(price)"]))
property_dict = dict(zip(property_prices["property_type"], property_prices["Mean(price)"]))

# Définir le modèle de données pour l'input utilisateur
class PredictionInput(BaseModel):
    bathrooms: float
    accomodate: int
    bedrooms: int
    beds: int
    room_type: str
    country: str
    property_type : str 
    neighbourhood : str

def get_neighbourhood_mean_price(neighbourhood):
    return neighbourhood_dict.get(neighbourhood, neighbourhood_dict["Unknown"])

def get_property_type_mean_price(property_type):
    return property_dict.get(property_type)

def apply_polynomial_model(input_data, coef_dict):
    """Applique les coefficients d'un modèle de régression polynomiale à un ensemble de données d'entrée."""
    price = coef_dict.get("Intercept", 0)
    
    for var, coef in coef_dict.items():
        if var == "Intercept":
            continue
        
        if "^" in var:  # Gestion des termes quadratiques
            base_var, exponent = var.split("^")
            exponent = int(exponent)
            if base_var in input_data:
                price += coef * (input_data[base_var] ** exponent)
        
        elif "*" in var:  # Gestion des termes d'interaction
            vars_interaction = var.split("*")
            if all(v in input_data for v in vars_interaction):
                product = np.prod([input_data[v] for v in vars_interaction])
                price += coef * product
        
        elif var in input_data:  # Gestion des termes linéaires
            price += coef * input_data[var]
    
    return price

def one_hot_encode(country, cat_list):
    """Encode en one-hot encoding en fonction de la liste donnée."""
    encoding = {c: 1 if c == country else 0 for c in cat_list}
    return encoding

# Définir l'endpoint POST pour prédire le prix
@app.post("/predict")
async def predict(input_data: PredictionInput):
    print("input data : ", input_data)
    
    country_list = ["Australie", "Argentine", "Thaïlande", "USA", "Bresil", "France", "Japon", "Espagne"]
    room_types = ["Shared room", "Hotel room"]
    input_dict = input_data.dict()
    input_dict.update(one_hot_encode(input_data.country, country_list))
    input_dict.update(one_hot_encode(input_data.room_type, room_types))
    
    input_dict["neighbourhood"] = get_neighbourhood_mean_price(input_data.neighbourhood)
    input_dict["property_type"] = get_property_type_mean_price(input_data.property_type)
    
    predicted_price = apply_polynomial_model(input_dict, coef_dict)
    return {"predicted_price": round(predicted_price, 2)}


