from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from backtest import run_backtest
from controllers.backtest_controller import get_backtest_slices, get_backtest_sessions, get_backtest_slices_by_session_id, get_backtest_slices_by_strategy_id
from controllers.optimization_controller import get_optimization_slices_by_session_id, get_optimization_sessions
from controllers.timeframe_set_controller import get_timeframe_sets, get_timeframe_sets_with_timeframes
from controllers.strategy_controller import create_strategy, get_strategies
from controllers.ticker_set_controller import get_ticker_sets
from create_optimization_session import save_session

# app = Flask(__name__)
app = Flask(__name__, static_folder='reports')

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

@app.route('/backtest-sessions', methods=['POST'])
@cross_origin()
def create_backtest_session():
    data = request.get_json()
    save_session(data["name"], data["details"])
    return jsonify(data)

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

@app.route('/strategies', methods=['POST'])
@cross_origin()
def create_new_strategy():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    create_strategy(name, description)
    return jsonify({"message": "Strategy created"})

@app.route('/strategies/<int:id>', methods=['GET'])
@cross_origin()
def strategy(id):
    sessions = get_backtest_slices_by_strategy_id(id)
    return jsonify([dict(session) for session in sessions])

@app.route('/timeframe-sets', methods=['GET'])
@cross_origin()
def timeframe_sets():
    timeframe_sets = get_timeframe_sets()
    return jsonify(timeframe_sets)

@app.route('/timeframe-sets-with-timeframes', methods=['GET'])
@cross_origin()
def timeframe_sets_with_timeframes():
    timeframe_sets = get_timeframe_sets_with_timeframes()
    return jsonify(timeframe_sets)

@app.route('/optimization-sessions', methods=['GET'])
@cross_origin()
def optimization_sessions():
    optimization_sessions = get_optimization_sessions()
    return jsonify(optimization_sessions)

@app.route('/optimization-sessions/<int:id>', methods=['GET'])
@cross_origin()
def optimization_session_slices(id):
    optimization_slices = get_optimization_slices_by_session_id(id)
    return jsonify(optimization_slices)

@app.route('/ticker-sets', methods=['GET'])
@cross_origin()
def ticker_sets():
    ticker_sets = get_ticker_sets()
    return jsonify(ticker_sets)

@app.route('/run-backtest', methods=['POST'])
@cross_origin()
def run_backtest_server():
    data = request.get_json()
    run_backtest(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)