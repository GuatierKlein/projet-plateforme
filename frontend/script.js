async function sendPredictionRequest(withreviews) {
    url = "predict"

    // Get input values
    let bathrooms = parseFloat(document.getElementById("bathrooms").value);
    let accomodate = parseInt(document.getElementById("accomodate").value);
    let bedrooms = parseInt(document.getElementById("bedrooms").value);
    let beds = parseInt(document.getElementById("beds").value);

    let room_type = document.getElementById("room_type").value;
    let country = document.getElementById("country").value;

    let review_scores_rating 
    let review_scores_accuracy 
    let review_scores_cleanliness 
    let review_scores_checkin 
    let review_scores_communication
    let review_scores_location 

    let data = {
        "bathrooms": bathrooms,
        "accomodate": accomodate,
        "bedrooms": bedrooms,
        "beds": beds,
        "room_type": room_type,
        "country": country
    };

    if(withreviews) {
        review_scores_rating = parseFloat(document.getElementById("review_scores_rating").value);
        review_scores_accuracy = parseFloat(document.getElementById("review_scores_accuracy").value);
        review_scores_cleanliness = parseFloat(document.getElementById("review_scores_cleanliness").value);
        review_scores_checkin = parseFloat(document.getElementById("review_scores_checkin").value);
        review_scores_communication = parseFloat(document.getElementById("review_scores_communication").value);
        review_scores_location = parseFloat(document.getElementById("review_scores_location").value);

        data["review_scores_rating"] = review_scores_rating
        data["review_scores_accuracy"] = review_scores_accuracy
        data["review_scores_cleanliness"] = review_scores_cleanliness
        data["review_scores_checkin"] = review_scores_checkin
        data["review_scores_communication"] = review_scores_communication
        data["review_scores_location"] = review_scores_location

        url = "predict_with_reviews"
    }


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
