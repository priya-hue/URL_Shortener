from app.store import url_map, lock
from flask import request, jsonify, redirect
from datetime import datetime
from app.utils import generate_short_code, is_valid_url


def register_routes(app):

    @app.route('/api/shorten', methods=['POST'])
    def shorten_url():
        data = request.get_json(silent=True)
        if not data or "url" not in data:
            return jsonify({"error": "Invalid request body"}), 400

        long_url = data.get("url")

        if not long_url or not is_valid_url(long_url):
            return jsonify({"error": "Invalid URL"}), 400

        short_code = generate_short_code()

        with lock:
            while short_code in url_map:
                short_code = generate_short_code()

            url_map[short_code] = {
                "original_url": long_url,
                "clicks": 0,
                "created_at": datetime.utcnow()
            }

        return jsonify({
            "short_code": short_code,
            "short_url": f"http://localhost:5000/{short_code}"
        }), 200

    @app.route('/<short_code>', methods=['GET'])
    def redirect_short_url(short_code):
        with lock:
            data = url_map.get(short_code)

            if not data:
                return jsonify({"error": "Short code not found"}), 404

            data["clicks"] += 1
            return redirect(data["original_url"])

    @app.route('/api/stats/<short_code>', methods=['GET'])
    def get_stats(short_code):
        with lock:
            data = url_map.get(short_code)

            if not data:
                return jsonify({"error": "Short code not found"}), 404

            return jsonify({
                "url": data["original_url"],
                "clicks": data["clicks"],
                "created_at": data["created_at"].isoformat()
            }), 200
