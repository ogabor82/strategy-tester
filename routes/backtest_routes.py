from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from controllers.backtest_controller import (
    get_backtest_session_stats,
    get_backtest_sessions_by_project_id,
    get_backtest_slices,
    get_backtest_sessions,
    get_backtest_slices_by_session_id,
)
from controllers.backtest_controller import (
    delete_backtest_session,
    save_session as save_backtest_session,
)
from backtest import run_backtest


backtest_routes = Blueprint("backtest_routes", __name__)


@backtest_routes.route("/backtest-results", methods=["GET"])
@cross_origin()
def sample():
    results = get_backtest_slices()
    return jsonify(results)


@backtest_routes.route("/backtest-sessions", methods=["GET"])
@cross_origin()
def backtest_sessions():
    sessions = get_backtest_sessions()
    return jsonify([dict(session) for session in sessions])


@backtest_routes.route("/backtest-sessions", methods=["POST"])
@cross_origin()
def create_backtest_session():
    data = request.get_json()
    result = save_backtest_session(data["name"], data["details"], data["project_id"])
    return jsonify([dict(result)][0])


@backtest_routes.route("/backtest-sessions/<int:id>", methods=["GET"])
@cross_origin()
def backtest_session(id):
    sessions = get_backtest_slices_by_session_id(id)
    return jsonify([dict(session) for session in sessions])


@backtest_routes.route("/backtest-sessions/<int:id>/stats", methods=["GET"])
@cross_origin()
def backtest_session_stats(id):
    stats = get_backtest_session_stats(id)
    return jsonify(stats)


@backtest_routes.route("/projects/<int:project_id>/backtest-sessions", methods=["GET"])
@cross_origin()
def get_backtest_session_by_project_id(project_id):
    sessions = get_backtest_sessions_by_project_id(project_id)
    return jsonify([dict(session) for session in sessions])


@backtest_routes.route("/backtest-sessions/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_backtest_session_server(id):
    delete_backtest_session(id)
    return jsonify({"message": "Backtest session deleted"})


@backtest_routes.route("/run-backtest", methods=["POST"])
@cross_origin()
def run_backtest_server():
    data = request.get_json()
    run_backtest(data)
    return jsonify(data)
