async function sendPredictionRequest() {
    // Get input values
    let bathrooms = parseFloat(document.getElementById("bathrooms").value);
    let accomodate = parseInt(document.getElementById("accomodate").value);
    let bedrooms = parseInt(document.getElementById("bedrooms").value);
    let beds = parseInt(document.getElementById("beds").value);

    let room_type = document.getElementById("room_type").value;
    let country = document.getElementById("country").value;

    let data = {
        "bathrooms": bathrooms,
        "accomodate": accomodate,
        "bedrooms": bedrooms,
        "beds": beds,
        "room_type": room_type,
        "country": country
    };

    try {
        let response = await fetch("http://127.0.0.1:8000/predict", {
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
