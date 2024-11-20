from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from controllers.backtest_controller import get_backtest_slices

app = Flask(__name__)
cors = CORS(app) 

@app.route('/backtest-results', methods=['GET'])
@cross_origin()
def sample():
    results = get_backtest_slices()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)