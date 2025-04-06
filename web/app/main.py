from flask import Flask, render_template, jsonify, request
from waitress import serve
import logging, requests

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

ANALYSIS_API_URL = "http://analysis:9090"

@app.route('/analysis/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def forward_request(path):
    try:
        url = f"{ANALYSIS_API_URL}/{path}"
        headers = dict(request.headers)
        if request.is_json:
            body = request.get_json()
        else:
            body = request.get_data()

        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=body,
        )
        response.raise_for_status()

        try:
            return jsonify(response.json()), response.status_code, dict(response.headers)
        except ValueError: 
            return response.content, response.status_code, dict(response.headers)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error forwarding request: {e}")
        return jsonify({"error": "Internal server error"}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/")
def overview():
    return render_template('overview.html')

if __name__ == "__main__":
    logging.info('Starting server')
    serve(app, host='0.0.0.0', port=9091)
