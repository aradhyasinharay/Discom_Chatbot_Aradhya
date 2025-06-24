import requests
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

from logger import logger
from date_utils import build_timestamp


# ---------------------------
# Dynamic Response Handler (API-based)
# ---------------------------
def generate_response(intent, date_str, time_obj, original_message=""):

    try:
        ts = build_timestamp(date_str, time_obj)
        iso_ts = ts.isoformat()

        if intent == "mod":
            try:
                start_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                mod_api_url = f"http://127.0.0.1:5000/procurement?start_date={start_str}&price_cap=10"
                response = requests.get(mod_api_url)

                logger.debug(f"MOD API status: {response.status_code}")
                logger.debug(f"MOD API response text: {response.text}")

                if response.status_code != 200:
                    return "Failed to fetch MOD price data."

                result = response.json()

                # Access Last_Price directly
                last_price = result.get("Last_Price", None)

                if last_price is not None:
                    return f"The MOD price at {ts.time()} on {ts.date()} is ₹{last_price} per unit."
                else:
                    return "MOD price data not available for that time."

            except Exception as e:
                logger.error(f"MOD API error: {e}")
                return "Error fetching MOD data."



        elif intent == "cost per block":
            try:
                ts = build_timestamp(date_str, time_obj)
                formatted_ts = ts.strftime("%Y-%m-%d %H:%M:%S")  # Adjusted format

                url = f"http://127.0.0.1:5000/procurement?start_date={formatted_ts}&price_cap=10"
                logger.debug(f"🔍 Procurement API URL: {url}")

                response = requests.get(url)
                logger.debug(f"🌐 API status: {response.status_code}")
                logger.debug(f"📦 Raw response JSON: {response.json()}")

                if response.status_code != 200:
                    return "Failed to fetch cost per block data."

                data = response.json()

                if not data or "Cost_Per_Block" not in data:
                    return "No data found for that time."

                cost = data["Cost_Per_Block"]

                return f"At {ts.time()} on {ts.date()}, the cost per block was ₹{cost}."

            except Exception as e:
                logger.error(f"Procurement API error: {e}")
                return "Error fetching cost per block data."



        elif intent == "iex":
            try:
                iex_api_url = f"http://localhost:5000/iex/range?start={ts.isoformat()}&end={(ts + timedelta(minutes=1)).isoformat()}"
                response = requests.get(iex_api_url)

                logger.debug(f"IEX API status: {response.status_code}")
                logger.debug(f"IEX API response text: {response.text}")

                if response.status_code != 200:
                    return "Failed to fetch IEX price data."

                result = response.json()
                data = result.get("data", [])

                logger.debug(f"Looking for ISO timestamp: {iso_ts}")

                matched = None
                for item in data:
                    try:
                        api_ts = parsedate_to_datetime(item["TimeStamp"]).replace(tzinfo=None)
                        logger.debug(f"Comparing API timestamp {api_ts} with target {ts}")
                        if api_ts == ts:
                            matched = item
                            break
                    except Exception as e:
                        logger.warning(f"Skipping item due to timestamp error: {e}")

                if matched:
                    return f"The IEX market rate at {ts.time()} on {ts.date()} is ₹{matched['predicted']} per unit."
                else:
                    return "No IEX data found for that time."

            except Exception as e:
                logger.error(f"IEX API error: {e}")
                return "Error fetching IEX data."


        elif intent == "demand":
            try:
                target_ts = build_timestamp(
                    (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
                    time_obj
                )
                start_ts = target_ts.isoformat()
                end_ts = (target_ts + timedelta(minutes=1)).isoformat()
                demand_api_url = f"http://localhost:5000/demand/range?start={start_ts}&end={end_ts}"
                response = requests.get(demand_api_url)
                if response.status_code != 200:
                    return "Failed to fetch demand data."
                data = response.json().get("data", [])
                if not data:
                    return "No demand data found for that time."
                avg_demand = sum(row["predicted"] for row in data) / len(data)
                return f"The average demand for {target_ts.time()} on {target_ts.date()} is {round(avg_demand, 2)} kWh"
            except Exception as e:
                logger.error(f"Demand API error: {e}")
                return "Error fetching demand data."

        return "Sorry, I don't have data for that request."

    except Exception as e:
        logger.error(f"generate_response error: {e}")
        return "Internal error while processing the request."

