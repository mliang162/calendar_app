from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'this works'})


if __name__ == '__main__':
    app.run(debug = True, port = 5000)