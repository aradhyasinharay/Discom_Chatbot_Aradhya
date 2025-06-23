from flask import Flask, request, jsonify, make_response
import json
from flask_cors import CORS
import logging
from logger import logger
from response_router import get_response
from static_qa import match_static_qa, static_qa
from nlp_setup import normalize, preprocess
from normalizer import normalize
from preprocessor import preprocess
from date_utils import extract_date, extract_time, build_timestamp
from intent_handler import get_intent
from response_handler import generate_response
from plant_handler import handle_plant_info
from procurement_handler import handle_procurement_info



app = Flask("Aradhya")
CORS(app)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route("/get", methods=["GET"])
def handle_chat():
    try:
        user_input = request.args.get("msg", "").strip()
        if not user_input:
            return jsonify({"error": "Empty request"}), 400

        logger.info(f"Received request: {user_input}")
        resp_text = get_response(user_input)
        resp = make_response(json.dumps({"response": resp_text}, ensure_ascii=False))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    except Exception as e:
        logger.error(f"Error in handle_chat: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# ---------------------------
# Flask App Runner
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
