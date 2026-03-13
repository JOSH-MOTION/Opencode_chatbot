from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import uuid
from main import index_urls, ask_question
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app)

# Store manifests in memory (in production, use Redis or database)
manifests = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/index', methods=['POST'])
def index_urls_api():
    try:
        data = request.get_json()
        urls = data.get('urls', '').strip()
        
        if not urls:
            return jsonify({'error': 'Please provide at least one URL'}), 400
        
        # Create unique session ID
        session_id = str(uuid.uuid4())
        
        # Index the URLs
        manifest = index_urls(urls)
        
        if not manifest.get('indexed_content'):
            return jsonify({'error': 'Failed to fetch content from the URLs'}), 400
        
        # Store manifest for this session
        manifests[session_id] = manifest
        
        num_pages = len(manifest.get('indexed_content', {}))
        
        return jsonify({
            'session_id': session_id,
            'message': f'Successfully indexed {num_pages} page(s)',
            'num_pages': num_pages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        query = data.get('query', '').strip()
        
        if not session_id or session_id not in manifests:
            return jsonify({'error': 'Invalid or expired session'}), 400
        
        if not query:
            return jsonify({'error': 'Please provide a question'}), 400
        
        manifest = manifests[session_id]
        result = ask_question(manifest, query)
        
        # Update manifest in case chat_active changed
        manifests[session_id] = manifest
        
        return jsonify({
            'response': result['response'],
            'chat_active': result['chat_active']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_session():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id in manifests:
            del manifests[session_id]
        
        return jsonify({'message': 'Session reset successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
