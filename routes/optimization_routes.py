from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from services.optimization_service import (
    get_optimization_sessions_by_project_id,
    get_optimization_slices_by_session_id,
    get_optimization_sessions,
)
from services.optimization_service import (
    delete_optimization_session,
    save_optimization_session,
)
from optimization import run_optimization

optimization_routes = Blueprint("optimization_routes", __name__)


@optimization_routes.route("/optimization-sessions", methods=["GET"])
@cross_origin()
def optimization_sessions():
    optimization_sessions = get_optimization_sessions()
    return jsonify(optimization_sessions)


@optimization_routes.route(
    "/projects/<int:project_id>/optimization-sessions", methods=["GET"]
)
@cross_origin()
def get_optimization_sessions_by_project_id_server(project_id):
    optimization_sessions = get_optimization_sessions_by_project_id(project_id)
    return jsonify(optimization_sessions)


@optimization_routes.route("/optimization-sessions", methods=["POST"])
@cross_origin()
def create_optimization_session():
    data = request.get_json()
    name = data.get("name")
    details = data.get("details")
    project_id = data.get("project_id")
    result = save_optimization_session(name, details, project_id)
    return jsonify([dict(result)][0])


@optimization_routes.route("/optimization-sessions/<int:id>", methods=["GET"])
@cross_origin()
def optimization_session_slices(id):
    optimization_slices = get_optimization_slices_by_session_id(id)
    return jsonify(optimization_slices)


@optimization_routes.route("/optimization-sessions/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_optimization_session_server(id):
    delete_optimization_session(id)
    return jsonify({"message": "Optimization session deleted"})


@optimization_routes.route("/run-optimization", methods=["POST"])
@cross_origin()
def run_optimization_server():
    data = request.get_json()
    run_optimization(data)
    return jsonify(data)
