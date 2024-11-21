from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/mock_pnr", methods=["GET"])
def mock_pnr():
    mock_data = {
        "pnr": "1234567890",
        "status": "Confirmed",
        "train": "12345",
        "arrivalDate": "2024-11-30",
        "passengerList": [
            {
                "serialNo": 1,
                "bookingBerthCode": "S1",
                "bookingBerthNo": "23",
                "bookingCoachId": "SL",
                "bookingStatus": "CNF"
            },
            {
                "serialNo": 2,
                "bookingBerthCode": "S2",
                "bookingBerthNo": "24",
                "bookingCoachId": "SL",
                "bookingStatus": "CNF"
            }
        ]
    }
    return jsonify(mock_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
