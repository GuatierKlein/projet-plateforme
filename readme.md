# Price prediction for airbnb rentals

## Front end

There are 2 webpages, they are simple HTML and vanilla js pages. You simply need to open them with your browser to open them. 
predict.html is a page that can send request to the polynomial model, without taking amenities into account.
predict_amenities.html is a page that can send requests to the random forest model, taking amenities into account. 

## Backend - Price Prediction API

This API allows predicting rental prices using either a **Polynomial Regression Model** or a **Random Forest Model**.

## Installation & Running the API

### Usage

**Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Run the API**
```bash
cd backend
uvicorn api:app 
```

### API Endpoints

#### `POST /predict`
**Description**: Predicts the price using a **Polynomial Regression Model**.

🔹 **Input (JSON)**:
```json
{
    "bathrooms": 1.0,
    "accomodate": 2,
    "bedrooms": 1,
    "beds": 1,
    "room_type": "Entire home/apt",
    "country": "France",
    "property_type": "Apartment",
    "neighbourhood": "Paris"
}
```

🔹 **Output (JSON)**:
```json
{
    "predicted_price": 150.75
}
```

---

#### `POST /predict_rf`
**Description**: Predicts the price using a **Random Forest Model**.

🔹 **Input (JSON)**:
```json
{
    "bathrooms": 1.0,
    "accomodate": 2,
    "bedrooms": 1,
    "beds": 1,
    "room_type": "Entire home/apt",
    "country": "France",
    "property_type": "Apartment",
    "neighbourhood": "Paris",
    "parking_gratuit": 1,
    "parking_payant": 0,
    "wifi": 1,
    "TV": 1,
    "microwave": 1,
    "dishwasher": 0,
    "clothes_washer": 1,
    "workspace": 1,
    "air_conditionner": 1,
    "heater": 1,
    "elevator": 1,
    "self_check_in": 0,
    "long_term_stay": 1,
    "bath_tub": 0,
    "coffee": 1,
    "luggage_storage": 0,
    "lockbox": 0,
    "security_cameras": 0,
    "host_greets_you": 0,
    "pets_allowed": 0,
    "view": 1,
    "smoking": 0,
    "pool": 0,
    "board_games": 0,
    "gym": 0,
    "fireplace": 0,
    "hot_tub": 0,
    "breakfast": 0
}
```

🔹 **Output (JSON)**:
```json
{
    "predicted_price": 180.50
}
```

---

## Notes
- The `/predict` endpoint uses a **Polynomial Regression Model** based on precomputed coefficients.
- The `/predict_rf` endpoint uses a **Random Forest Model** trained on tabular data including amenities.

---

## Author
Developed by **Gautier KLEIN** 