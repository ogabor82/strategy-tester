from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from controllers.strategy_controller import create_strategy, get_strategies
from controllers.backtest_controller import get_backtest_slices_by_strategy_id

strategy_routes = Blueprint("strategy_routes", __name__)


@strategy_routes.route("/strategies", methods=["GET"])
@cross_origin()
def strategies():
    strategies = get_strategies()
    return jsonify(strategies)


@strategy_routes.route("/strategies", methods=["POST"])
@cross_origin()
def create_new_strategy():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    create_strategy(name, description)
    return jsonify({"message": "Strategy created"})


@strategy_routes.route("/strategies/<int:id>", methods=["GET"])
@cross_origin()
def strategy(id):
    sessions = get_backtest_slices_by_strategy_id(id)
    return jsonify([dict(session) for session in sessions])
