import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Charger les données (exemple fictif)
df = pd.read_csv("datalinreg_withreviews.csv")

# Séparer X et y
y = df['price']  # Variable cible
X = df.drop(columns=['price'])  # Variables explicatives

# Normaliser les variables numériques
data_to_normalize = ["bathrooms", "accomodate", "bedrooms", "beds", "review_scores_rating","review_scores_accuracy","review_scores_cleanliness","review_scores_checkin","review_scores_communication","review_scores_location"]
scaler = StandardScaler()
X[data_to_normalize] = scaler.fit_transform(X[data_to_normalize])

# Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Analyser la performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Coefficients : {model.coef_}")
print(f"✅ Intercept : {model.intercept_}")
print(f"📉 MSE (Mean Squared Error) : {mse:.2f}")
print(f"📊 R² Score : {r2:.2f}")

# Exporter les coefficients dans un fichier CSV
coefficients = pd.DataFrame({
    "Variable": X.columns,
    "Coefficient": model.coef_
})

# Ajouter l'intercept
intercept_df = pd.DataFrame({"Variable": ["Intercept"], "Coefficient": [model.intercept_]})

# Concaténer les coefficients et l'intercept
coefficients = pd.concat([intercept_df, coefficients], ignore_index=True)

# Sauvegarder dans un fichier CSV
coefficients.to_csv("coefficients_withreviews.csv", index=False)

print("Coefficients exportés dans 'coefficients_withreviews.csv'")

