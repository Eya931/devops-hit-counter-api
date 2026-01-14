from flask import Flask, request, jsonify, render_template_string, send_from_directory
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from pythonjsonlogger import jsonlogger
import logging
import json
import os
from datetime import datetime
import time

app = Flask(__name__)

# ===== LOGGING STRUCTURÉ =====
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ===== MÉTRIQUES PROMETHEUS =====
request_count = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
request_duration = Histogram('api_request_duration_seconds', 'API request duration', ['endpoint'])
hit_counter = Counter('page_hits_total', 'Total hits per page', ['page_name'])

# ===== DONNÉES EN MÉMOIRE =====
pages_data = {
    1: {"id": 1, "name": "Home page", "hits": 4850, "created_at": datetime.now().isoformat()},
    2: {"id": 2, "name": "Login / Sign up", "hits": 1320, "created_at": datetime.now().isoformat()},
    3: {"id": 3, "name": "Shop / Products listing", "hits": 2940, "created_at": datetime.now().isoformat()},
    4: {"id": 4, "name": "Product details page", "hits": 6780, "created_at": datetime.now().isoformat()},
    5: {"id": 5, "name": "Search results page", "hits": 1150, "created_at": datetime.now().isoformat()},
    6: {"id": 6, "name": "Cart page", "hits": 620, "created_at": datetime.now().isoformat()},
    7: {"id": 7, "name": "Checkout page", "hits": 310, "created_at": datetime.now().isoformat()},
    8: {"id": 8, "name": "Payment page", "hits": 245, "created_at": datetime.now().isoformat()},
    9: {"id": 9, "name": "Order confirmation page", "hits": 230, "created_at": datetime.now().isoformat()},
    10: {"id": 10, "name": "User profile / Account", "hits": 410, "created_at": datetime.now().isoformat()},
    11: {"id": 11, "name": "Wishlist / Favorites", "hits": 180, "created_at": datetime.now().isoformat()},
    12: {"id": 12, "name": "About us", "hits": 260, "created_at": datetime.now().isoformat()},
    13: {"id": 13, "name": "Contact us", "hits": 140, "created_at": datetime.now().isoformat()},
    14: {"id": 14, "name": "FAQ / Help", "hits": 195, "created_at": datetime.now().isoformat()},
    15: {"id": 15, "name": "Admin dashboard", "hits": 85, "created_at": datetime.now().isoformat()}
}

# ===== MIDDLEWARE POUR TRACER LES REQUÊTES =====
@app.before_request
def before_request():
    request.start_time = time.time()
    request_id = request.headers.get('X-Request-ID', f"req-{datetime.now().timestamp()}")
    request.request_id = request_id
    logger.info(f"Incoming request", extra={
        "method": request.method,
        "path": request.path,
        "request_id": request_id
    })

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    endpoint = request.path.split('/')[1] or 'root'
    request_count.labels(method=request.method, endpoint=endpoint).inc()
    request_duration.labels(endpoint=endpoint).observe(duration)
    logger.info(f"Request completed", extra={
        "status": response.status_code,
        "duration_ms": round(duration * 1000, 2),
        "request_id": request.request_id
    })
    return response

# ===== ROUTES API =====

@app.route('/', methods=['GET'])
def dashboard():
    """Serve the dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), 'static', 'dashboard.html')
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/static/<path:filename>', methods=['GET'])
def static_files(filename):
    """Serve static files (CSS, JS)"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_dir, filename)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/pages', methods=['GET'])
def get_pages():
    return jsonify(list(pages_data.values())), 200

@app.route('/api/pages', methods=['POST'])
def create_page():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "name required"}), 400
    
    page_id = len(pages_data) + 1
    pages_data[page_id] = {
        "id": page_id,
        "name": data['name'],
        "hits": 0,
        "created_at": datetime.now().isoformat()
    }
    return jsonify(pages_data[page_id]), 201

@app.route('/api/pages/<int:page_id>/hits', methods=['GET'])
def get_hits(page_id):
    if page_id not in pages_data:
        return jsonify({"error": "page not found"}), 404
    return jsonify({"hits": pages_data[page_id]['hits']}), 200

@app.route('/api/pages/<int:page_id>/hit', methods=['POST'])
def increment_hit(page_id):
    if page_id not in pages_data:
        return jsonify({"error": "page not found"}), 404
    
    pages_data[page_id]['hits'] += 1
    hit_counter.labels(page_name=pages_data[page_id]['name']).inc()
    logger.info(f"Hit recorded", extra={
        "page_id": page_id,
        "page_name": pages_data[page_id]['name'],
        "total_hits": pages_data[page_id]['hits']
    })
    return jsonify(pages_data[page_id]), 200

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(REGISTRY), 200

# ===== ERROR HANDLING =====
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found", extra={"path": request.path})
    return jsonify({"error": "not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"500 Server Error", extra={"error": str(error)})
    return jsonify({"error": "internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)