import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Charger les données depuis un fichier CSV
data = pd.read_csv("data.csv")  # Remplacez "data.csv" par le nom de votre fichier

# Supprimer les colonnes non pertinentes
# columns_to_drop = ["price (Out-of-bag)", "price (Out-of-bag) (Prediction Variance)", "model count"]
# data = data.drop(columns=columns_to_drop, errors='ignore')

# Séparer les features (X) et la cible (y)
X = data.drop(columns=["price"])  # Toutes les colonnes sauf "price"
y = data["price"]

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialiser et entraîner le modèle Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)
rf_model.fit(X_train, y_train)

# Prédictions sur l'ensemble de test
y_pred = rf_model.predict(X_test)

# Évaluer les performances du modèle
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Afficher les résultats
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R2): {r2}")
print(f"Out-of-Bag Score: {rf_model.oob_score_}")


