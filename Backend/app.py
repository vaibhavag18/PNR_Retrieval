# import requests
# import pickle
# import cv2
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os

# app = Flask(__name__)
# CORS(app)
# s = requests.Session()
# loaded_model = pickle.load(open("models/model.sav", "rb"))


# def download_image(url, save_path):
#     try:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#         }
#         response = s.get(url, headers=headers, stream=True)
#         # response = s.get(url, headers=headers, stream=True)
#         response.raise_for_status()
#         os.makedirs(os.path.dirname(save_path), exist_ok=True)
#         with open(save_path, "wb") as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)
#         print("Image downloaded successfully.")
#         return True
#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")
#         return False


# def segment(image, st):
#     flag = 0
#     flag2 = 0
#     start = 0
#     end = 0
#     for i in range(st, 149):
#         for j in range(30):
#             if image[j, i] != 0:
#                 flag = 1
#                 if start == 0:
#                     start = i - 2
#                 flag2 = 1
#         if flag == 0 and flag2 == 1:
#             end = i + 2
#             break
#         flag = 0
#     finalImage = image[:, start:end]
#     return finalImage, end


# def predict_number():
#     dfX = []
#     image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
#     save_location = "predict/0.png" 
#     download_image(image_url, save_location)

#     image = cv2.imread("predict/0.png", cv2.IMREAD_UNCHANGED)
#     trans_mask = image[:, :, 3] == 0
#     image[trans_mask] = [255, 255, 255, 255]
#     image = cv2.bitwise_not(image)
#     image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
#     image = cv2.resize(image, (150, 30))
#     end = 0
#     for i in range(6):
#         finalImage, end = segment(image, end)
#         finalImage = cv2.resize(finalImage, (25, 25))
#         dummy = []
#         finalImage = finalImage.flatten()
#         dummy.append(finalImage)
#         if loaded_model.predict(dummy) == [12]:
#             break
#         dfX.append(finalImage)
#     y_pred = loaded_model.predict(dfX)
#     plus = 0
#     dig1 = 0
#     dig = 0
#     for i in y_pred:
#         if i == 10 or i == 11:
#             if i == 10:
#                 plus = 1
#             dig1 = dig
#             dig = 0

#         else:
#             dig = dig * 10 + i
#     if plus:
#         dig1 += dig
#     else:
#         dig1 -= dig
#     return dig1


# def get_pnr_status(captcha, pnr_number):
#     base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#     }
#     response = s.get(base_url, headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to retrieve data. Status code: {response.status_code}")
#         s.close()
#         return None


# @app.route("/finpredict", methods=["GET"])
# def finpredict():
#     captcha = predict_number()  # Replace with your desired captcha value

#     pnr_number = int(
#         request.args.get("pnrnumber")
#     )  # Replace with your desired PNR number

#     json_data = get_pnr_status(captcha, pnr_number)

#     return json_data


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)



import requests
import pickle
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Initialize session and model
s = requests.Session()
loaded_model = pickle.load(open("models/model.sav", "rb"))

# Add retry strategy to the session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],  # Updated from 'method_whitelist' to 'allowed_methods'
)
adapter = HTTPAdapter(max_retries=retry_strategy)
s.mount("https://", adapter)


def download_image(url, save_path):
    """Downloads an image from a given URL and saves it to the specified path."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = s.get(url, headers=headers, stream=True, verify=False)  # Bypass SSL verification
        response.raise_for_status()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the image
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Validate image integrity
        if cv2.imread(save_path, cv2.IMREAD_UNCHANGED) is None:
            print("Downloaded file is not a valid image.")
            return False

        print("Image downloaded successfully.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error during image download: {e}")
        return False


def segment(image, start_index):
    """Segments characters in the CAPTCHA image."""
    flag, flag2, start, end = 0, 0, 0, 0
    for i in range(start_index, 149):
        for j in range(30):
            if image[j, i] != 0:
                flag = 1
                if start == 0:
                    start = i - 2
                flag2 = 1
        if flag == 0 and flag2 == 1:
            end = i + 2
            break
        flag = 0
    final_image = image[:, start:end]
    return final_image, end


def predict_number():
    """Processes the CAPTCHA image and predicts the number."""
    image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png"
    save_location = "predict/0.png"

    # Download the CAPTCHA image
    if not download_image(image_url, save_location):
        print("Failed to download CAPTCHA image.")
        return None

    # Load and process the image
    image = cv2.imread(save_location, cv2.IMREAD_UNCHANGED)
    if image is None:
        print("Failed to load CAPTCHA image.")
        return None

    try:
        trans_mask = image[:, :, 3] == 0
        image[trans_mask] = [255, 255, 255, 255]
        image = cv2.bitwise_not(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        image = cv2.resize(image, (150, 30))
    except Exception as e:
        print(f"Error during image processing: {e}")
        return None

    dfX = []
    end = 0
    for _ in range(6):
        final_image, end = segment(image, end)
        final_image = cv2.resize(final_image, (25, 25))
        dummy = [final_image.flatten()]
        if loaded_model.predict(dummy) == [12]:
            break
        dfX.append(dummy[0])

    # Predict the digits
    y_pred = loaded_model.predict(dfX)
    plus, dig1, dig = 0, 0, 0
    for i in y_pred:
        if i in [10, 11]:
            if i == 10:
                plus = 1
            dig1, dig = dig, 0
        else:
            dig = dig * 10 + i
    return dig1 + dig if plus else dig1 - dig


def get_pnr_status(captcha, pnr_number):
    """Fetches PNR status using the predicted CAPTCHA."""
    base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = s.get(base_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving PNR status: {e}")
        return None


@app.route("/finpredict", methods=["GET"])
def finpredict():
    """API endpoint to predict the PNR status."""
    captcha = predict_number()
    if captcha is None:
        return jsonify({"error": "Failed to generate CAPTCHA or process the image."}), 500

    pnr_number = request.args.get("pnrnumber")
    if not pnr_number or not pnr_number.isdigit():
        return jsonify({"error": "Invalid or missing PNR number."}), 400

    json_data = get_pnr_status(captcha, int(pnr_number))
    if json_data is None:
        return jsonify({"error": "Failed to retrieve PNR status."}), 500

    return jsonify(json_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
