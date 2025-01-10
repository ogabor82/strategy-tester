from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from services.project_service import create_project, delete_project, get_projects

project_routes = Blueprint("project_routes", __name__)


@project_routes.route("/projects", methods=["GET"])
@cross_origin()
def projects():
    projects = get_projects()
    return jsonify(projects)


@project_routes.route("/projects", methods=["POST"])
@cross_origin()
def create_project_server():
    data = request.get_json()
    result = create_project(data["name"], data["goal"], data["details"])
    return jsonify([dict(result)][0])


@project_routes.route("/projects/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_project_server(id):
    delete_project(id)
    return jsonify({"message": "Project deleted"})
