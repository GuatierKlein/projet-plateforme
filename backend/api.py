from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from randomforest_reg import rf_model
from models import PredictionInput, PredictionInputAmenities

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

# Convertir les coefficients en dictionnaire avec gestion des multiples exposants
coef_dict = {}
for _, row in coefficients.iterrows():
    variable = row["Variable"]
    exponent = int(row["Exponent"]) if not pd.isna(row["Exponent"]) else 1
    coef = row["Coeff."]
    
    if variable not in coef_dict:
        coef_dict[variable] = []
    coef_dict[variable].append((coef, exponent))

neighbourhood_dict = dict(zip(neighbourhood_prices["neighbourhood"], neighbourhood_prices["Mean(price)"]))
property_dict = dict(zip(property_prices["property_type"], property_prices["Mean(price)"]))

print(coef_dict)

def get_neighbourhood_mean_price(neighbourhood):
    return neighbourhood_dict.get(neighbourhood, neighbourhood_dict.get("Unknown", 0))

def get_property_type_mean_price(property_type):
    return property_dict.get(property_type, 0)

def apply_polynomial_model(input_data, coef_dict):
    """Applique les coefficients d'un modèle de régression polynomiale à un ensemble de données d'entrée."""
    price = sum(coef for coef, _ in coef_dict.get("Intercept", [(0, 1)]))
    
    for var, terms in coef_dict.items():
        if var == "Intercept":
            continue
        
        if var in input_data:
            for coef, exponent in terms:
                price += coef * (float(input_data[var]) ** exponent)
    
    return price

def one_hot_encode(category, cat_list):
    """Encode en one-hot encoding en fonction de la liste donnée."""
    return {c: 1 if c == category else 0 for c in cat_list}

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
    
    print(input_dict)
    
    predicted_price = apply_polynomial_model(input_dict, coef_dict)
    print("predicted : ", predicted_price)
    return {"predicted_price": round(predicted_price, 2)}

@app.post("/predict_rf")
async def predict_rf(input_data: PredictionInputAmenities):
    print("Input data:", input_data)

    country_list = ["Australie", "Argentine", "Thaïlande", "USA", "Bresil", "France", "Japon", "Espagne"]
    room_types = ["Shared room", "Hotel room"]
    input_dict = input_data.dict()
    input_dict.update(one_hot_encode(input_data.country, country_list))
    input_dict.update(one_hot_encode(input_data.room_type, room_types))
    
    input_dict["neighbourhood"] = get_neighbourhood_mean_price(input_data.neighbourhood)
    input_dict["property_type"] = get_property_type_mean_price(input_data.property_type)

    del input_dict["country"]
    del input_dict["room_type"]
    
    # Convertir l'entrée en DataFrame
    input_df = pd.DataFrame([input_dict])

    # Vérifier et réorganiser les colonnes
    expected_columns = rf_model.feature_names_in_
    input_df = pd.DataFrame([input_dict]).reindex(columns=expected_columns, fill_value=0)

    print(input_dict)
    
    # Faire la prédiction
    predicted_price = rf_model.predict(input_df)[0]
    
    return {"predicted_price": round(predicted_price, 2)}