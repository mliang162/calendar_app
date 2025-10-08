import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'this works'})

@app.route('/api/wiki/<page_title>', methods=['GET'])
def get_wiki_page(page_title):
    """Fetch Wikipedia page content in HTML format"""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        
        # API parameters
        params = {
            'action': 'parse',
            'page': page_title,
            'format': 'json',
            'prop': 'text' 
        }
        
        # User-Agent header
        headers = {
            'User-Agent': 'WikiApp/1.0 (your-email@example.com)'
        }
        
        # Make request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if page exists
        if 'error' in data:
            return jsonify({
                'error': data['error']['info'],
                'code': data['error']['code']
            }), 404
        
        return jsonify({
            'title': data['parse']['title'],
            'pageid': data['parse']['pageid'],
            'html': data['parse']['text']['*']
        })
        
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wiki/summary/<page_title>', methods=['GET'])
def get_wiki_summary(page_title):
    """Fetch Wikipedia page summary (first section only)"""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            'action': 'parse',
            'page': page_title,
            'format': 'json',
            'prop': 'text',
            'section': 0  
        }
        
        # User-Agent header 
        headers = {
            'User-Agent': 'WikiApp/1.0 (your-email@example.com)'
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if 'error' in data:
            return jsonify({
                'error': data['error']['info']
            }), 404
        
        return jsonify({
            'title': data['parse']['title'],
            'summary': data['parse']['text']['*']
        })
        
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)