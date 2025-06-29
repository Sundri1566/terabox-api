import os
from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/api/terabox', methods=['POST'])
def terabox_handler():
    data = request.get_json()
    url = data.get("url")
    
    if not url or "teraboxapp.com" not in url:
        return jsonify({"error": "Invalid TeraBox URL"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(url, headers=headers)
        html = r.text

        match = re.search(r'"httpsDownloadUrl":"(.*?)"', html)
        if not match:
            return jsonify({"error": "Download link not found"}), 404

        download_url = match.group(1).replace('\\u002F', '/')

        preview_match = re.search(r'"playUrl":"(.*?)"', html)
        preview_url = preview_match.group(1).replace('\\u002F', '/') if preview_match else None

        return jsonify({
            "download_url": download_url,
            "preview_url": preview_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
