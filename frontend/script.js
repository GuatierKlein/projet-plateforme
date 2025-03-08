async function sendPredictionRequest() {
    url = "predict"

    // Get input values
    let bathrooms = parseFloat(document.getElementById("bathrooms").value);
    let accomodate = parseInt(document.getElementById("accomodate").value);
    let bedrooms = parseInt(document.getElementById("bedrooms").value);
    let beds = parseInt(document.getElementById("beds").value);
    let room_type = document.getElementById("room_type").value;
    let country = document.getElementById("country").value;
    let property_type = document.getElementById("property_type").value;
    let neighbourhood = document.getElementById("neighbourhood").value;

    let data = {
        "bathrooms": bathrooms,
        "accomodate": accomodate,
        "bedrooms": bedrooms,
        "beds": beds,
        "room_type": room_type,
        "country": country,
        "property_type": property_type,
        "neighbourhood": neighbourhood
    };

    try {
        let response = await fetch(`http://127.0.0.1:8000/${url}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        let result = await response.json();
        document.getElementById("result").innerHTML = "💰 Predicted Price: " + result.predicted_price + " €";
    } catch (error) {
        document.getElementById("result").innerHTML = "❌ Error: " + error.message;
    }
}