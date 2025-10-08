from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/subscription/attr-change', methods=['POST'])
def attr_change():
    if not request.is_json:
        abort(400, description="Request payload must be JSON")
    data = request.get_json()
    print(json.dumps(data, indent=2))
    return {'status': 'received'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)


