from flask import Blueprint, jsonify
from flask_cors import cross_origin
from services.timeframe_set_service import (
    get_timeframe_sets,
    get_timeframe_sets_with_timeframes,
)

timeframe_set_routes = Blueprint("timeframe_set_routes", __name__)


@timeframe_set_routes.route("/timeframe-sets", methods=["GET"])
@cross_origin()
def timeframe_sets():
    timeframe_sets = get_timeframe_sets()
    return jsonify(timeframe_sets)


@timeframe_set_routes.route("/timeframe-sets-with-timeframes", methods=["GET"])
@cross_origin()
def timeframe_sets_with_timeframes():
    timeframe_sets = get_timeframe_sets_with_timeframes()
    return jsonify(timeframe_sets)
