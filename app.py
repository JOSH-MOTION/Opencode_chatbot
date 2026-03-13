from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid
import traceback
from main import index_urls, ask_question
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'nexus-secret-key-2024'
CORS(app)

# Store manifests in memory
manifests = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/index', methods=['POST', 'GET', 'OPTIONS'])
def index_urls_api():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'message': 'Nexus API is running'})

    try:
        data = request.get_json(silent=True) or {}
        urls = data.get('urls', '').strip()

        if not urls:
            return jsonify({'error': 'Please provide at least one URL'}), 400

        session_id = str(uuid.uuid4())
        manifest = index_urls(urls)

        if not manifest.get('indexed_content'):
            return jsonify({'error': 'Failed to fetch content from the URLs. Make sure they are accessible.'}), 400

        manifests[session_id] = manifest
        num_pages = len(manifest.get('indexed_content', {}))

        return jsonify({
            'session_id': session_id,
            'message': f'Successfully indexed {num_pages} page(s)',
            'num_pages': num_pages
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat_api():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get('session_id')
        query = data.get('query', '').strip()

        if not session_id or session_id not in manifests:
            return jsonify({'error': 'Invalid or expired session. Please re-index your URLs.'}), 400

        if not query:
            return jsonify({'error': 'Please provide a question'}), 400

        manifest = manifests[session_id]
        result = ask_question(manifest, query)
        manifests[session_id] = manifest

        return jsonify({
            'response': result['response'],
            'chat_active': result['chat_active']
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST', 'OPTIONS'])
def reset_session():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json(silent=True) or {}
        session_id = data.get('session_id')

        if session_id in manifests:
            del manifests[session_id]

        return jsonify({'message': 'Session reset successfully'})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)