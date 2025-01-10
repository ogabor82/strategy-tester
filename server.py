from flask import Flask
from flask_cors import CORS
from routes.backtest_routes import backtest_routes
from routes.strategy_routes import strategy_routes
from routes.optimization_routes import optimization_routes
from routes.timeframe_set_routes import timeframe_set_routes
from routes.ticker_set_routes import ticker_set_routes
from routes.project_routes import project_routes

app = Flask(__name__, static_folder="reports")
cors = CORS(app)

# Register the blueprints
app.register_blueprint(backtest_routes)
app.register_blueprint(strategy_routes)
app.register_blueprint(optimization_routes)
app.register_blueprint(timeframe_set_routes)
app.register_blueprint(ticker_set_routes)
app.register_blueprint(project_routes)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
