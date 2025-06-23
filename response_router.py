from static_qa import match_static_qa
from nlp_setup import preprocess
from normalizer import normalize
from plant_handler import handle_plant_info
from procurement_handler import handle_procurement_info
from intent_handler import get_intent
from response_handler import generate_response
from logger import logger
from preprocessor import preprocess
from date_utils import extract_date, extract_time, build_timestamp


# ---------------------------
# Chat Interface
# ---------------------------
def get_response(user_input):
    static = match_static_qa(user_input)
    if static:
        return static

    toks, matched_keywords = preprocess(user_input)
    print("🔍 Tokens:", toks)
    print("✅ Matched Keywords:", matched_keywords)

    # Extract date and time once
    date_str = extract_date(user_input)
    time_obj = extract_time(user_input)

    # PLANT INFO check
    if any(k in matched_keywords for k in [
        'plf', 'paf', 'variable cost', 'aux consumption', 'max power', 'min power',
        'rated capacity', 'technical minimum', 'type', 'maximum power', 'minimum power',
        'auxiliary consumption', 'plant load factor', 'plant availability factor',
        'aux usage', 'auxiliary usage', 'var cost'
    ]):
        if not date_str or not time_obj:
            return "Please specify both date and time for the plant information."
        return handle_plant_info(date_str, time_obj, user_input)

    # PROCUREMENT check
    if any(k in matched_keywords for k in [
        'banking', 'banking unit','banked', 'energy generated','banked unit','banking contribution',
        'generated energy', 'procurement price', 'energy', 'iex cost', 'demand banked',
        'cost generated', 'generated cost', 'generation cost', 'generated cost'
    ]):
        print("📅 Extracted date:", date_str)
        print("⏰ Extracted time:", time_obj)

        if not date_str or not time_obj:
            return "Sorry, I couldn't understand your request."
        return handle_procurement_info(user_input, date_str, time_obj)

    # FALLBACK for other intents like demand, iex, mod
    if not time_obj:
        return "Sorry, I couldn't understand your request."

    intent = get_intent(toks, user_input)
    if not intent:
        return "Sorry, I couldn't understand your request."

    if intent == "procurement":
        return handle_procurement_info(user_input, date_str, time_obj)

    return generate_response(intent, date_str, time_obj)
