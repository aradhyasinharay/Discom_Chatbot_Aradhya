import re


# ---------------------------
# Static Knowledge Base
# ---------------------------
static_qa = {
    "Hi": "Hello! How can I assist you today?",
    "Explain about yourself": "Hi I am Aradhya, your virtual assistant. I can help you with information about electricity demand, MOD prices, IEX rate. Just ask me anything related to power and energy!",
    "what is the definition of moment of dispatch price": "The Moment of Dispatch (MOD) price refers to the cost of electricity at a specific 15-minute time block when it is dispatched to meet demand. It is used in electricity markets and grid operations to determine the economic value or cost of delivering electricity at a given moment, based on real-time supply and demand conditions.",
    "what is the indian energy exchange price definition": "The Indian Energy Exchange (IEX) price refers to the market-determined clearing price of electricity traded on the Indian Energy Exchange for specific time blocks during the day.",
    "what is the definition of mod": "MOD (Moment of Dispatch) refers to the specific point in time when electricity is actually dispatched (sent out) from the generation source to meet the demand on the grid.",
    "what is iex": "Indian Energy Exchange (IEX) is India’s premier electricity trading platform...",
    "error": "Sorry, I am unable to understand your requirement."
}

def match_static_qa(user_input):
    cleaned = re.sub(r'[^\w\s]', '', user_input.lower().strip())
    keyword_map = {
        "fuck you": static_qa["error"],
        "hi": static_qa["Hi"],
        "hello": static_qa["Hi"],
        "hey": static_qa["Hi"],
        "love you": static_qa["error"],
        "explain about yourself": static_qa["Explain about yourself"],
        "tell me about yourself": static_qa["Explain about yourself"],
        "definition of mod": static_qa["what is the definition of mod"],
        "what is iex": static_qa["what is iex"],
        "what is mod": static_qa["what is the definition of mod"],
        "definition of iex": static_qa["what is iex"],
        "what is moment of dispatch price": static_qa["what is the definition of moment of dispatch price"],
        "what is moment of dispatch rate": static_qa["what is the definition of moment of dispatch price"],
        "what is indian energy exchange price": static_qa["what is the indian energy exchange price definition"],
        "what is indian energy exchange rate": static_qa["what is the indian energy exchange price definition"],
        "what is iex price": static_qa["what is the indian energy exchange price definition"],
        "what is mod price": static_qa["what is the definition of moment of dispatch price"],
        "what is mod rate": static_qa["what is the definition of moment of dispatch price"],
        "what is iex rate": static_qa["what is the indian energy exchange price definition"],
        "what is the definition of moment of dispatch price": static_qa[
            "what is the definition of moment of dispatch price"],
        "what is the definition of moment of dispatch rate": static_qa[
            "what is the definition of moment of dispatch price"],
        "what is the definition of indian energy exchange price": static_qa[
            "what is the indian energy exchange price definition"],
        "what is the definition of indian energy exchange rate": static_qa[
            "what is the indian energy exchange price definition"],
        "what is the definition of IEX rate": static_qa["what is the indian energy exchange price definition"],
        "what is the definition of IEX price": static_qa["what is the indian energy exchange price definition"],
        "what is the definition of MOD price": static_qa["what is the definition of moment of dispatch price"],
        "what is the definition of MOD rate": static_qa["what is the definition of moment of dispatch price"],
        "what is indian energy exchange price definition": static_qa[
            "what is the indian energy exchange price definition"],
        "what is indian energy exchange rate definition": static_qa[
            "what is the indian energy exchange price definition"],
        "what is moment of dispatch price definition": static_qa["what is the definition of moment of dispatch price"],
        "what is moment of dispatch rate definition": static_qa["what is the definition of moment of dispatch price"],
        "what is the definition of mod": static_qa["what is the definition of mod"],
        "definition of moment of dispatch": static_qa["what is the definition of mod"],
        "what is the definition of moment of dispatch": static_qa["what is the definition of mod"],
        "what is the definition iex": static_qa["what is iex"],
        "what is the definition indian energy exchange": static_qa["what is iex"],
        "what is indian energy exchange": static_qa["what is iex"],
    }
    for keyword, resp in sorted(keyword_map.items(), key=lambda x: -len(x[0])):
        if keyword in cleaned:
            return resp
    return None
