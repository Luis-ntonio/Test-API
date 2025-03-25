from flask import Flask, request, jsonify
import requests
import os
import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()

app = Flask(__name__)

@app.route('/get-token', methods=['POST'])
def get_token():
    """
    API endpoint to retrieve the token from the login route.
    """
    try:
        # Load sensitive data from environment variables
        password = os.getenv("PASSWORD", "string")
        kb = os.getenv("KB", "string")
        login = os.getenv("LOGIN", "string")
        lang = os.getenv("LANG", "string")

        # Login URL
        url = 'https://belcorptest.agiloft.com/ewws/alrest/Belcorp%20Test/login'

        # Set up headers and payload
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "password": password,
            "KB": kb,
            "login": login,
            "lang": lang
        }

        # Make a POST request to the login route
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()

        # Parse the response
        response_data = response.json()
        if 'result' in response_data and 'access_token' in response_data['result']:
            return jsonify({"token": response_data['result']['access_token']})
        else:
            return jsonify({"error": "Failed to retrieve token"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)