async function sendPredictionRequest() {
    // Get input values
    let bathrooms = parseFloat(document.getElementById("bathrooms").value);
    let accomodate = parseInt(document.getElementById("accomodate").value);
    let bedrooms = parseInt(document.getElementById("bedrooms").value);
    let beds = parseInt(document.getElementById("beds").value);
    let room_type = document.getElementById("room_type").value;
    let country = document.getElementById("country").value;
    let property_type = document.getElementById("property_type").value;
    let neighbourhood = document.getElementById("neighbourhood").value;

    // List of amenities
    let amenities = [
        "parking_gratuit", "parking_payant", "wifi", "TV", "microwave", "dishwasher", "clothes_washer", "workspace",
        "air_conditionner", "heater", "elevator", "self_check_in", "long_term_stay", "bath_tub", "coffee", "luggage_storage",
        "lockbox", "security_cameras", "host_greets_you", "pets_allowed", "view", "smoking", "pool", "board_games", "gym",
        "fireplace", "hot_tub", "breakfast"
    ];

    // Convert checkboxes to int values
    let amenitiesData = {};
    amenities.forEach(amenity => {
        amenitiesData[amenity] = document.getElementById(amenity).checked ? 1 : 0;
    });

    let data = {
        "bathrooms": bathrooms,
        "accomodate": accomodate,
        "bedrooms": bedrooms,
        "beds": beds,
        "room_type": room_type,
        "country": country,
        "property_type": property_type,
        "neighbourhood": neighbourhood,
        ...amenitiesData
    };

    console.log(data)

    try {
        let response = await fetch(`http://127.0.0.1:8000/predict_rf`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        console.log(JSON.stringify(data));

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        let result = await response.json();
        document.getElementById("result").innerHTML = "💰 Predicted Price: " + result.predicted_price + " $";
    } catch (error) {
        document.getElementById("result").innerHTML = "❌ Error: " + error.message;
    }
}
