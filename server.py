from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from controllers.backtest_controller import get_backtest_slices, get_backtest_sessions, get_backtest_slices_by_session_id, get_backtest_slices_by_strategy_id, get_strategies

app = Flask(__name__)
cors = CORS(app) 

@app.route('/backtest-results', methods=['GET'])
@cross_origin()
def sample():
    results = get_backtest_slices()
    return jsonify(results)

@app.route('/backtest-sessions', methods=['GET'])
@cross_origin()
def backtest_sessions():
    sessions = get_backtest_sessions()
    return jsonify([dict(session) for session in sessions])

@app.route('/backtest-sessions/<int:id>', methods=['GET'])
@cross_origin()
def backtest_session(id):    
    sessions = get_backtest_slices_by_session_id(id)
    return jsonify([dict(session) for session in sessions])

@app.route('/strategies', methods=['GET'])
@cross_origin()
def strategies():
    strategies = get_strategies()
    return jsonify(strategies)

@app.route('/strategies/<int:id>', methods=['GET'])
@cross_origin()
def strategy(id):
    sessions = get_backtest_slices_by_strategy_id(id)
    return jsonify([dict(session) for session in sessions])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)