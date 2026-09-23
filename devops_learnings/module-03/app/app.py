from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Docker Module 3 Demo_NEW"

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
