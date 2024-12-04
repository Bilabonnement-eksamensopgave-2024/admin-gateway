from flask import Flask, jsonify, request, make_response
import requests
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from dotenv import load_dotenv
import threading
import time
from swagger.config import init_swagger


app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Load environment variables from .env file
load_dotenv()

# MICROSERVICES:
MICROSERVICES = {
    "abonnement_microservice": os.getenv("ABONNEMENT_MICROSERVICE_URL", "http://localhost:5002"),
    "login_microservice": os.getenv("LOGIN_MICROSERVICE_URL", "http://localhost:5003"),
}

ENDPOINTS = {} 

# Initialize Swagger
init_swagger(app)

def update_endpoints():
    while True:
        for service, url in MICROSERVICES.items(): 
            try: 
                response = requests.get(f"{url}/routes") 
                routes = response.json() 
                for route in routes: 
                    for method in route["methods"]:
                        key = f"{method}_{route['path'].strip('/')}"
                        ENDPOINTS[key] = f"{url}{route['path']}"
            except requests.exceptions.ConnectionError as e: 
                print(f"Connection error for {service}: {e}") 
            except Exception as e: 
                print(f"Error updating routes for {service}: {e}") 
                time.sleep(60*5) # Update every 60 seconds 

threading.Thread(target=update_endpoints, daemon=True).start() 

# ----------------------------------------------------- ENDPOINTS
@app.route('/<path:path>', methods=['GET', 'POST', 'PATCH', 'DELETE']) 
def gateway(path): 
    key = f"{request.method}_{path}" 
    if key not in ENDPOINTS: 
        return jsonify({"error": "Endpoint not found"}), 404 
    
    # Get the full URL for the specific endpoint 
    url = ENDPOINTS[key]

    #headers = {key: value for key, value in request.headers.items()} 
    
    #print(f"Headers for {request.method} request: {headers}")

    # Forward request with appropriate HTTP method
    response = requests.request( 
        method=request.method, 
        url=url, 
        headers={"Authorization": "Bearer 1234"},
        params=request.args, 
        data=request.get_data(), 
        allow_redirects=False 
    )
    
    # Pass response back to client
    return response.content, response.status_code, response.headers.items()

# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
