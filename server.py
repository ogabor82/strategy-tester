from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from routes.backtest_routes import backtest_routes
from routes.strategy_routes import strategy_routes
from routes.optimization_routes import optimization_routes
from controllers.project_controller import create_project, delete_project, get_projects
from controllers.timeframe_set_controller import (
    get_timeframe_sets,
    get_timeframe_sets_with_timeframes,
)
from controllers.ticker_set_controller import get_ticker_sets

app = Flask(__name__, static_folder="reports")
cors = CORS(app)

# Register the blueprints
app.register_blueprint(backtest_routes)
app.register_blueprint(strategy_routes)
app.register_blueprint(optimization_routes)


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


@app.route("/ticker-sets", methods=["GET"])
@cross_origin()
def ticker_sets():
    ticker_sets = get_ticker_sets()
    return jsonify(ticker_sets)


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
