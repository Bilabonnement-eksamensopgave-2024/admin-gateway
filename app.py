from flask import Flask, jsonify, request, make_response
import requests
import os
from flasgger import swag_from
from dotenv import load_dotenv
from swagger.config import init_swagger


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MICROSERVICES:
MICROSERVICES = {
    "abonnement": os.getenv("ABONNEMENT_MICROSERVICE_URL", "http://localhost:5002"),
    "user": os.getenv("USER_MICROSERVICE_URL", "http://localhost:5005"),
    "skade": os.getenv("SKADE_MICROSERVICE_URL", "http://localhost:5006"),
    "car": os.getenv("CAR_MICROSERVICE_URL", "http://localhost:5007"),
}

# Initialize Swagger
init_swagger(app)

# ----------------------------------------------------- ENDPOINTS /service/path
@app.route('/<service>/<path:path>', methods=['GET', 'PATCH', 'DELETE'])
def gateway_service(service, path):
    if service not in MICROSERVICES:
        return jsonify({"error": "Service not found"}), 404
    
    # Get the full URL for the microservice
    url = f"{MICROSERVICES[service]}/{path}"

    print(url)

    # Set Content-Type to application/json for methods that typically have a body 
    headers = {}
    if request.method in ['POST', 'PATCH', 'PUT']: 
        headers['Content-Type'] = 'application/json'

    # Forward request with appropriate HTTP method
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    # Pass response back to client
    return (response.content, response.status_code, response.headers.items())

# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# ----------------------------------------------------- Catch-all route for unmatched endpoints 
@app.errorhandler(404)
def page_not_found_404(e):
    return jsonify({"message": "Endpoint does not exist"})

@app.errorhandler(405)
def page_not_found_405(e):
    return jsonify({"message": "Method not allowed - double check the method you are using"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
