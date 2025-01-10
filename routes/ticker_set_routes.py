from flask import Blueprint, jsonify
from flask_cors import cross_origin
from services.ticker_set_service import get_ticker_sets

ticker_set_routes = Blueprint("ticker_set_routes", __name__)


@ticker_set_routes.route("/ticker-sets", methods=["GET"])
@cross_origin()
def ticker_sets():
    ticker_sets = get_ticker_sets()
    return jsonify(ticker_sets)
