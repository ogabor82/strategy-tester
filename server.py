from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from controllers.backtest_controller import get_backtest_slices, get_backtest_sessions, get_backtest_slices_by_session_id, get_backtest_slices_by_strategy_id
from controllers.optimization_controller import get_optimization_slices_by_session_id, get_optimization_sessions
from controllers.timeframe_set_controller import get_timeframe_sets
from controllers.strategy_controller import create_strategy, get_strategies

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
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)