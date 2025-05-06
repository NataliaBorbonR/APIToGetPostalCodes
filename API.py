from flask import Flask, jsonify, request
from get_geographic_data import get_postal_code
app = Flask(__name__)

@app.route('/getpostalcodes', methods=['GET'])
def get_postal_codes():
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Missing address'}), 400
    result = get_postal_code(address)
    return  result



if __name__ == '__main__':
    app.run(debug=True)
