from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from backtest import run_backtest
from controllers.backtest_controller import (
    get_backtest_session_stats,
    get_backtest_sessions_by_project_id,
    get_backtest_slices,
    get_backtest_sessions,
    get_backtest_slices_by_session_id,
    get_backtest_slices_by_strategy_id,
)
from controllers.optimization_controller import (
    get_optimization_sessions_by_project_id,
    get_optimization_slices_by_session_id,
    get_optimization_sessions,
)
from controllers.project_controller import create_project, delete_project, get_projects
from controllers.timeframe_set_controller import (
    get_timeframe_sets,
    get_timeframe_sets_with_timeframes,
)
from controllers.strategy_controller import create_strategy, get_strategies
from controllers.ticker_set_controller import get_ticker_sets
from create_optimization_session import (
    delete_optimization_session,
    save_optimization_session,
)
from create_session import (
    delete_backtest_session,
    save_session as save_backtest_session,
)
from optimization import run_optimization

# app = Flask(__name__)
app = Flask(__name__, static_folder="reports")

cors = CORS(app)


@app.route("/backtest-results", methods=["GET"])
@cross_origin()
def sample():
    results = get_backtest_slices()
    return jsonify(results)


@app.route("/backtest-sessions", methods=["GET"])
@cross_origin()
def backtest_sessions():
    sessions = get_backtest_sessions()
    return jsonify([dict(session) for session in sessions])


@app.route("/backtest-sessions", methods=["POST"])
@cross_origin()
def create_backtest_session():
    data = request.get_json()
    result = save_backtest_session(data["name"], data["details"], data["project_id"])
    return jsonify([dict(result)][0])


@app.route("/backtest-sessions/<int:id>", methods=["GET"])
@cross_origin()
def backtest_session(id):
    sessions = get_backtest_slices_by_session_id(id)
    return jsonify([dict(session) for session in sessions])


@app.route("/backtest-sessions/<int:id>/stats", methods=["GET"])
@cross_origin()
def backtest_session_stats(id):
    stats = get_backtest_session_stats(id)
    return jsonify(stats)


@app.route("/projects/<int:project_id>/backtest-sessions", methods=["GET"])
@cross_origin()
def get_backtest_session_by_project_id(project_id):
    sessions = get_backtest_sessions_by_project_id(project_id)
    return jsonify([dict(session) for session in sessions])


@app.route("/backtest-sessions/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_backtest_session_server(id):
    delete_backtest_session(id)
    return jsonify({"message": "Backtest session deleted"})


@app.route("/strategies", methods=["GET"])
@cross_origin()
def strategies():
    strategies = get_strategies()
    return jsonify(strategies)


@app.route("/strategies", methods=["POST"])
@cross_origin()
def create_new_strategy():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    create_strategy(name, description)
    return jsonify({"message": "Strategy created"})


@app.route("/strategies/<int:id>", methods=["GET"])
@cross_origin()
def strategy(id):
    sessions = get_backtest_slices_by_strategy_id(id)
    return jsonify([dict(session) for session in sessions])


@app.route("/timeframe-sets", methods=["GET"])
@cross_origin()
def timeframe_sets():
    timeframe_sets = get_timeframe_sets()
    return jsonify(timeframe_sets)


@app.route("/timeframe-sets-with-timeframes", methods=["GET"])
@cross_origin()
def timeframe_sets_with_timeframes():
    timeframe_sets = get_timeframe_sets_with_timeframes()
    return jsonify(timeframe_sets)


@app.route("/optimization-sessions", methods=["GET"])
@cross_origin()
def optimization_sessions():
    optimization_sessions = get_optimization_sessions()
    return jsonify(optimization_sessions)


@app.route("/projects/<int:project_id>/optimization-sessions", methods=["GET"])
@cross_origin()
def get_optimization_sessions_by_project_id_server(project_id):
    optimization_sessions = get_optimization_sessions_by_project_id(project_id)
    return jsonify(optimization_sessions)


@app.route("/optimization-sessions", methods=["POST"])
@cross_origin()
def create_optimization_session():
    data = request.get_json()
    name = data.get("name")
    details = data.get("details")
    project_id = data.get("project_id")
    result = save_optimization_session(name, details, project_id)
    return jsonify([dict(result)][0])


@app.route("/optimization-sessions/<int:id>", methods=["GET"])
@cross_origin()
def optimization_session_slices(id):
    optimization_slices = get_optimization_slices_by_session_id(id)
    return jsonify(optimization_slices)


@app.route("/optimization-sessions/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_optimization_session_server(id):
    delete_optimization_session(id)
    return jsonify({"message": "Optimization session deleted"})


@app.route("/ticker-sets", methods=["GET"])
@cross_origin()
def ticker_sets():
    ticker_sets = get_ticker_sets()
    return jsonify(ticker_sets)


@app.route("/run-backtest", methods=["POST"])
@cross_origin()
def run_backtest_server():
    data = request.get_json()
    run_backtest(data)
    return jsonify(data)


@app.route("/run-optimization", methods=["POST"])
@cross_origin()
def run_optimization_server():
    data = request.get_json()
    run_optimization(data)
    return jsonify(data)


@app.route("/projects", methods=["GET"])
@cross_origin()
def projects():
    projects = get_projects()
    return jsonify(projects)


@app.route("/projects", methods=["POST"])
@cross_origin()
def create_project_server():
    data = request.get_json()
    result = create_project(data["name"], data["goal"], data["details"])
    return jsonify([dict(result)][0])


@app.route("/projects/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_project_server(id):
    delete_project(id)
    return jsonify({"message": "Project deleted"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
