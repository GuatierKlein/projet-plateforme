# 🏠 Real Estate Price Prediction API

This project is a **FastAPI-based machine learning application** that predicts the price of a property based on input features such as **bathrooms, bedrooms, accommodations, beds, room type, and country**.

It includes:
- A **FastAPI backend** for handling price prediction requests.
- A **frontend web page** built with **HTML, CSS, and JavaScript** to interact with the API.
- A **trained linear regression model** with coefficients stored in a CSV file.

---

## 🚀 Features
✅ **FastAPI** backend to handle price predictions.  
✅ **CORS enabled** for frontend communication.  
✅ **Interactive web interface** to input features and get price predictions.  
✅ **Machine Learning Model** trained and exported as coefficients.  
✅ **JSON-based API** for easy integration.  

---

## 🐂 Project Structure

```
/real-estate-price-prediction/
│── api.py           # FastAPI backend
│── coefficients.csv # Trained model coefficients
│── index.html       # Frontend UI
│── script.js        # JavaScript for frontend API calls
│── styles.css       # CSS for styling the frontend
│── README.md        # Project documentation
│── requirements.txt # Python dependencies
```

---

## 🛠️ Installation & Setup

### 1️⃣ **Clone the repository**
```sh
git clone https://github.com/yourusername/real-estate-price-prediction.git
cd real-estate-price-prediction
```

### 2️⃣ **Create a virtual environment (Optional but recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ **Install dependencies**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Run the FastAPI Server**
```sh
uvicorn api:app --reload
```
✅ The API will be available at: **http://127.0.0.1:8000**  

---

## 🌍 Using the Web App
1. **Start the API server** (`uvicorn api:app --reload`).
2. **Open `index.html` in a browser**.
3. **Fill in the property details** and click `Predict Price`.
4. The predicted price will be displayed below the button.

---

## 🛠️ API Endpoints

### 🔹 **POST /predict**
📝 **Predicts the price of a property.**  

📥 **Request Body (JSON)**:
```json
{
    "bathrooms": 2,
    "accomodate": 4,
    "bedrooms": 2,
    "beds": 3,
    "room_type": "Shared room",
    "country": "USA"
}
```

📤 **Response (JSON)**:
```json
{
    "predicted_price": 250.75
}
```

---

## ⚙️ Configuration (CORS, Security, etc.)
- **CORS is enabled** to allow frontend and API communication.
- To restrict CORS in production, update `api.py`:
  ```python
  allow_origins=["https://yourdomain.com"]
  ```
