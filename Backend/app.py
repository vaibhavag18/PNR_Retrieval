# # # # import requests
# # # # import pickle
# # # # import cv2
# # # # import os
# # # # from flask import Flask, request, jsonify
# # # # from flask_cors import CORS

# # # # app = Flask(__name__)
# # # # CORS(app)
# # # # s = requests.Session()

# # # # # Load the pre-trained model
# # # # loaded_model = pickle.load(open("models/model.sav", "rb"))

# # # # # Proceed with the request
# # # # def download_image(url, save_path):
# # # #     try:
# # # #         response = s.get(url, stream=True, timeout=10)
# # # #         response.raise_for_status()
# # # #         with open(save_path + ".png", "wb") as file:
# # # #             for chunk in response.iter_content(chunk_size=8192):
# # # #                 file.write(chunk)
# # # #         print("Image downloaded successfully.")
# # # #         return True
# # # #     except requests.exceptions.SSLError as e:
# # # #         print(f"SSL Error occurred: {e}")
# # # #         return False
# # # #     except requests.exceptions.RequestException as e:
# # # #         print(f"Request Error occurred: {e}")
# # # #         return False


# # # # def segment(image, st):
# # # #     flag = 0
# # # #     flag2 = 0
# # # #     start = 0
# # # #     end = 0
# # # #     for i in range(st, 149):
# # # #         for j in range(30):
# # # #             if image[j, i] != 0:
# # # #                 flag = 1
# # # #                 if start == 0:
# # # #                     start = i - 2
# # # #                 flag2 = 1
# # # #         if flag == 0 and flag2 == 1:
# # # #             end = i + 2
# # # #             break
# # # #         flag = 0
# # # #     finalImage = image[:, start:end]
# # # #     return finalImage, end

# # # # def predict_number():
# # # #     dfX = []
# # # #     image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
# # # #     save_location = "predict/" + str(0)
    
# # # #     # Download the captcha image
# # # #     if not download_image(image_url, save_location):
# # # #         return "Error downloading image", 500

# # # #     # Read and preprocess the image
# # # #     image = cv2.imread("predict/0.png", cv2.IMREAD_UNCHANGED)
# # # #     trans_mask = image[:, :, 3] == 0
# # # #     image[trans_mask] = [255, 255, 255, 255]
# # # #     image = cv2.bitwise_not(image)
# # # #     image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
# # # #     image = cv2.resize(image, (150, 30))
# # # #     end = 0
# # # #     for i in range(6):
# # # #         finalImage, end = segment(image, end)
# # # #         finalImage = cv2.resize(finalImage, (25, 25))
# # # #         dummy = []
# # # #         finalImage = finalImage.flatten()
# # # #         dummy.append(finalImage)
# # # #         if loaded_model.predict(dummy) == [12]:
# # # #             break
# # # #         dfX.append(finalImage)

# # # #     # Prediction result
# # # #     y_pred = loaded_model.predict(dfX)
# # # #     plus = 0
# # # #     dig1 = 0
# # # #     dig = 0
# # # #     for i in y_pred:
# # # #         if i == 10 or i == 11:
# # # #             if i == 10:
# # # #                 plus = 1
# # # #             dig1 = dig
# # # #             dig = 0
# # # #         else:
# # # #             dig = dig * 10 + i
# # # #     if plus:
# # # #         dig1 += dig
# # # #     else:
# # # #         dig1 -= dig
# # # #     return dig1

# # # # def get_pnr_status(captcha, pnr_number):
# # # #     base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
# # # #     headers = {
# # # #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# # # #     }
# # # #     try:
# # # #         response = s.get(base_url, headers=headers, timeout=10)  # Timeout added to avoid hanging
# # # #         response.raise_for_status()
# # # #         return response.json()
# # # #     except requests.exceptions.RequestException as e:
# # # #         print(f"Failed to retrieve data: {e}")
# # # #         return None

# # # # @app.route("/finpredict", methods=["GET"])
# # # # def finpredict():
# # # #     captcha = predict_number()  # Captcha prediction logic
# # # #     if isinstance(captcha, tuple):
# # # #         return jsonify({'error': captcha[0]}), captcha[1]  # Error handling for image download

# # # #     pnr_number = request.args.get("pnrnumber")
# # # #     if not pnr_number:
# # # #         return jsonify({'error': 'PNR number is required'}), 400

# # # #     # Fetch PNR status using the predicted captcha and provided PNR number
# # # #     json_data = get_pnr_status(captcha, pnr_number)
# # # #     if json_data:
# # # #         return jsonify(json_data)
# # # #     else:
# # # #         return jsonify({'error': 'Failed to fetch PNR status'}), 500

# # # # if __name__ == "__main__":
# # # #     if not os.path.exists("predict"):
# # # #         os.makedirs("predict")  # Ensure the 'predict' directory exists

# # # #     app.run(host="0.0.0.0", port=8080, debug=True)



# # # import requests
# # # import pickle
# # # import cv2
# # # from flask import Flask, request, jsonify
# # # from flask_cors import CORS

# # # app = Flask(__name__)
# # # CORS(app)
# # # s = requests.Session()
# # # loaded_model = pickle.load(open("models/model.sav", "rb"))


# # # def download_image(url, save_path):
# # #     try:
# # #         response = s.get(url, stream=True,verify=False)
# # #         response.raise_for_status()
# # #         with open(save_path + ".png", "wb") as file:
# # #             for chunk in response.iter_content(chunk_size=8192):
# # #                 file.write(chunk)

# # #         print("Image downloaded successfully.")
# # #         return True

# # #     except requests.exceptions.RequestException as e:
# # #         print(f"Error occurred: {e}")
# # #         return False


# # # def segment(image, st):
# # #     flag = 0
# # #     flag2 = 0
# # #     start = 0
# # #     end = 0
# # #     for i in range(st, 149):
# # #         for j in range(30):
# # #             if image[j, i] != 0:
# # #                 flag = 1
# # #                 if start == 0:
# # #                     start = i - 2
# # #                 flag2 = 1
# # #         if flag == 0 and flag2 == 1:
# # #             end = i + 2
# # #             break
# # #         flag = 0
# # #     finalImage = image[:, start:end]
# # #     return finalImage, end


# # # def predict_number():
# # #     dfX = []
# # #     image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
# # #     save_location = "predict/" + str(0)
# # #     download_image(image_url, save_location)
# # #     image = cv2.imread("predict/0.png", cv2.IMREAD_UNCHANGED)
# # #     trans_mask = image[:, :, 3] == 0
# # #     image[trans_mask] = [255, 255, 255, 255]
# # #     image = cv2.bitwise_not(image)
# # #     image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
# # #     image = cv2.resize(image, (150, 30))
# # #     end = 0
# # #     for i in range(6):
# # #         finalImage, end = segment(image, end)
# # #         finalImage = cv2.resize(finalImage, (25, 25))
# # #         dummy = []
# # #         finalImage = finalImage.flatten()
# # #         dummy.append(finalImage)
# # #         if loaded_model.predict(dummy) == [12]:
# # #             break
# # #         dfX.append(finalImage)
# # #     y_pred = loaded_model.predict(dfX)
# # #     plus = 0
# # #     dig1 = 0
# # #     dig = 0
# # #     for i in y_pred:
# # #         if i == 10 or i == 11:
# # #             if i == 10:
# # #                 plus = 1
# # #             dig1 = dig
# # #             dig = 0

# # #         else:
# # #             dig = dig * 10 + i
# # #     if plus:
# # #         dig1 += dig
# # #     else:
# # #         dig1 -= dig
# # #     return dig1


# # # def get_pnr_status(captcha, pnr_number):
# # #     base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
# # #     headers = {
# # #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# # #     }
# # #     response = s.get(base_url, headers=headers)
# # #     if response.status_code == 200:
# # #         return response.json()
# # #     else:
# # #         print(f"Failed to retrieve data. Status code: {response.status_code}")
# # #         s.close()
# # #         return None


# # # @app.route("/finpredict", methods=["GET"])
# # # def finpredict():
# # #     captcha = predict_number()  # Replace with your desired captcha value
# # #     pnr_number = int(
# # #         request.args.get("pnrnumber")
# # #     )  # Replace with your desired PNR number

# # #     json_data = get_pnr_status(captcha, pnr_number)

# # #     return json_data


# # # if __name__ == "__main__":
# # #     app.run(host="0.0.0.0", port=8080, debug=True)





# # import os
# # import requests
# # import pickle
# # import cv2
# # from flask import Flask, request, jsonify
# # from flask_cors import CORS

# # app = Flask(__name__)
# # CORS(app)
# # s = requests.Session()

# # # Load the model
# # MODEL_PATH = os.path.join("models", "model.sav")
# # loaded_model = pickle.load(open(MODEL_PATH, "rb"))

# # # Create the predict folder if it doesn't exist
# # os.makedirs("predict", exist_ok=True)

# # @app.route("/")
# # def home():
# #     return "API is running!", 200


# # def download_image(url, save_path):
# #     try:
# #         response = s.get(url, stream=True, verify=False)  # Avoid SSL error
# #         response.raise_for_status()
# #         with open(save_path + ".png", "wb") as file:
# #             for chunk in response.iter_content(chunk_size=8192):
# #                 file.write(chunk)
# #         print("Image downloaded successfully.")
# #         return True
# #     except requests.exceptions.RequestException as e:
# #         print(f"Error occurred: {e}")
# #         return False


# # def segment(image, st):
# #     flag = 0
# #     flag2 = 0
# #     start = 0
# #     end = 0
# #     for i in range(st, 149):
# #         for j in range(30):
# #             if image[j, i] != 0:
# #                 flag = 1
# #                 if start == 0:
# #                     start = i - 2
# #                 flag2 = 1
# #         if flag == 0 and flag2 == 1:
# #             end = i + 2
# #             break
# #         flag = 0
# #     finalImage = image[:, start:end]
# #     return finalImage, end


# # def predict_number():
# #     dfX = []
# #     image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
# #     save_location = os.path.join("predict", str(0))
# #     if not download_image(image_url, save_location):
# #         return None
# #     image = cv2.imread(save_location + ".png", cv2.IMREAD_UNCHANGED)
# #     trans_mask = image[:, :, 3] == 0
# #     image[trans_mask] = [255, 255, 255, 255]
# #     image = cv2.bitwise_not(image)
# #     image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
# #     image = cv2.resize(image, (150, 30))
# #     end = 0
# #     for i in range(6):
# #         finalImage, end = segment(image, end)
# #         finalImage = cv2.resize(finalImage, (25, 25))
# #         dummy = []
# #         finalImage = finalImage.flatten()
# #         dummy.append(finalImage)
# #         if loaded_model.predict(dummy) == [12]:
# #             break
# #         dfX.append(finalImage)
# #     y_pred = loaded_model.predict(dfX)
# #     plus = 0
# #     dig1 = 0
# #     dig = 0
# #     for i in y_pred:
# #         if i == 10 or i == 11:
# #             if i == 10:
# #                 plus = 1
# #             dig1 = dig
# #             dig = 0
# #         else:
# #             dig = dig * 10 + i
# #     if plus:
# #         dig1 += dig
# #     else:
# #         dig1 -= dig
# #     return dig1


# # def get_pnr_status(captcha, pnr_number):
# #     base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
# #     headers = {
# #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# #     }
# #     response = s.get(base_url, headers=headers)
# #     if response.status_code == 200:
# #         return response.json()
# #     else:
# #         print(f"Failed to retrieve data. Status code: {response.status_code}")
# #         s.close()
# #         return None


# # @app.route("/finpredict", methods=["GET"])
# # def finpredict():
# #     captcha = predict_number()
# #     if captcha is None:
# #         return jsonify({"error": "Failed to predict captcha"}), 500

# #     pnr_number = int(request.args.get("pnrnumber"))
# #     json_data = get_pnr_status(captcha, pnr_number)
# #     if json_data is None:
# #         return jsonify({"error": "Failed to retrieve PNR status"}), 500

# #     return jsonify(json_data)


# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=8080)



# import os
# import requests
# import pickle
# import cv2
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# # Initialize Flask App
# app = Flask(__name__)
# CORS(app)

# # Set up paths for models and predict folder
# MODEL_PATH = os.path.join(os.getcwd(), "models", "model.sav")
# PREDICT_PATH = os.path.join(os.getcwd(), "predict")

# # Ensure predict folder exists
# if not os.path.exists(PREDICT_PATH):
#     os.makedirs(PREDICT_PATH)

# # Load the pre-trained model
# loaded_model = pickle.load(open(MODEL_PATH, "rb"))

# # Function to download an image from a URL
# def download_image(url, save_path):
#     try:
#         response = requests.get(url, stream=True)
#         response.raise_for_status()
#         with open(save_path + ".png", "wb") as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)

#         print("Image downloaded successfully.")
#         return True

#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")
#         return False

# # Function to segment an image
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

# # Function to predict captcha numbers
# def predict_number():
#     dfX = []
#     image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
#     save_location = os.path.join(PREDICT_PATH, "0")
#     download_image(image_url, save_location)
#     image = cv2.imread(save_location + ".png", cv2.IMREAD_UNCHANGED)
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

# # Function to get PNR status
# def get_pnr_status(captcha, pnr_number):
#     base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
#     }
#     response = requests.get(base_url, headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to retrieve data. Status code: {response.status_code}")
#         return {"error": "Failed to retrieve data", "status_code": response.status_code}

# # Route for predicting PNR status
# @app.route("/finpredict", methods=["GET"])
# def finpredict():
#     try:
#         captcha = predict_number()  # Predict the captcha
#         pnr_number = int(
#             request.args.get("pnrnumber")
#         )  # Get the PNR number from the query params
#         json_data = get_pnr_status(captcha, pnr_number)
#         return jsonify(json_data)
#     except Exception as e:
#         return jsonify({"error": str(e)})

# # Main entry point
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)



import requests
import pickle
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize session and model
s = requests.Session()
loaded_model = pickle.load(open("models/model.sav", "rb"))

# Function to download captcha image
def download_image(url, save_path):
    try:
        response = s.get(url, stream=True)
        response.raise_for_status()
        with open(save_path + ".png", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("Image downloaded successfully.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False

# Function to segment the image
def segment(image, st):
    flag = 0
    flag2 = 0
    start = 0
    end = 0
    for i in range(st, 149):
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
    finalImage = image[:, start:end]
    return finalImage, end

# Function to predict the captcha value
def predict_number():
    dfX = []
    image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
    save_location = "predict/" + str(0)
    download_image(image_url, save_location)
    image = cv2.imread("predict/0.png", cv2.IMREAD_UNCHANGED)
    trans_mask = image[:, :, 3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    image = cv2.bitwise_not(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    image = cv2.resize(image, (150, 30))
    end = 0
    for i in range(6):
        finalImage, end = segment(image, end)
        finalImage = cv2.resize(finalImage, (25, 25))
        dummy = []
        finalImage = finalImage.flatten()
        dummy.append(finalImage)
        if loaded_model.predict(dummy) == [12]:
            break
        dfX.append(finalImage)
    y_pred = loaded_model.predict(dfX)
    plus = 0
    dig1 = 0
    dig = 0
    for i in y_pred:
        if i == 10 or i == 11:
            if i == 10:
                plus = 1
            dig1 = dig
            dig = 0
        else:
            dig = dig * 10 + i
    if plus:
        dig1 += dig
    else:
        dig1 -= dig
    print(f"Predicted captcha: {dig1}")  # Debugging the predicted captcha
    return dig1

# Function to retrieve PNR status
def get_pnr_status(captcha, pnr_number):
    # Use a persistent session to maintain the state
    # session = requests.Session()  # Fresh session
    # base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    #     "Accept": "application/json",  # Accept JSON responses
    #     "Content-Type": "application/json"  # Ensure JSON format
    # }

    base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = s.get(base_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        s.close()
        return None

    # Send the request with the correct headers
    # response = session.get(base_url, headers=headers)
    # print(f"PNR Request URL: {base_url}")  # Debugging URL
    # print(f"Response Status Code: {response.status_code}")  # Debugging response status code
    # print(f"Response Body: {response.text}")  # Debugging response body

    # if response.status_code == 200:
    #     # Debug the returned response
    #     return response.json()  # Parse the response as JSON
    # else:
    #     print(f"Failed to retrieve data. Status code: {response.status_code}")
    #     return None

@app.route("/finpredict", methods=["GET"])
def finpredict():
    captcha = predict_number()  # Get the captcha value
    pnr_number = int(request.args.get("pnrnumber"))  # Get PNR number from request

    json_data = get_pnr_status(captcha, pnr_number)

    if json_data:
        return jsonify(json_data)
    else:
        return jsonify({
            "errorMessage": "Session out or Invalid Request",
            "generatedTimeStamp": {
                "day": 22,
                "hour": 23,
                "minute": 9,
                "second": 36,
                "month": 11,
                "year": 2024
            },
            "serverId": "appserver"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


