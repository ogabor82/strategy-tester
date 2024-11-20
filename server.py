from flask import Flask, jsonify

from controllers.backtest_controller import get_backtest_slices

app = Flask(__name__)


@app.route('/backtest-results', methods=['GET'])
def sample():
    results = get_backtest_slices()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)