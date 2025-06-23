import re
import requests
from logger import logger
from normalizer import normalize  # if normalize is in a separate file
from datetime import datetime
from utils import fuzzy_match


def handle_plant_info(date_str, time_obj, original_message):
    try:
        start_timestamp = f"{date_str} {time_obj.strftime('%H:%M:%S')}"
        plant_api_url = "http://127.0.0.1:5000/plant/"
        response = requests.get(plant_api_url)

        if response.status_code != 200:
            return "Failed to fetch plant details."

        data = response.json()
        all_plants = data.get("must_run", []) + data.get("other", [])

        if not all_plants:
            return "No plant data available."

        message = normalize(original_message)

        plant_field_map = {
            "plf": "PLF",
            "plant load factor": "PLF",
            "paf": "PAF",
            "plant availability factor": "PAF",
            "variable cost": "Variable_Cost",
            "aux consumption": "Aux_Consumption",
            "auxiliary consumption": "Aux_Consumption",
            "max power": "Max_Power",
            "min power": "Min_Power",
            "rated capacity": "Rated_Capacity",
            "type": "Type",
            "technical minimum": "Technical_Minimum",
            "aux usage": "Aux_Consumption",
            "auxiliary usage": "Aux_Consumption",
            "var cost": "Variable_Cost"
        }

        requested_field = None
        for k in plant_field_map:
            if k in message:
                requested_field = plant_field_map[k]
                break

        if not requested_field:
            return "Please specify whether you want PLF, PAF, variable cost, or some other technical parameter."

        # Try to match plant name from message
        match = re.search(r"(?:by|for|of)\s+([a-z0-9\s\-&/]+?)(?=\s+(?:on|at)\s+|[\?\.!]|$)", message, re.IGNORECASE)

        if match:
            print("🧠 Raw match group:", match.group(1))
            plant_query = normalize(match.group(1).replace('/', ' '))
            for plant in all_plants:
                plant_name = plant.get("name", "Unknown Plant")  # Changed from "plant_name" to "name"
                print(f"🔍 Comparing user input '{plant_query}' with plant '{plant_name}'")
                if fuzzy_match(normalize(plant_name), plant_query):
                    if requested_field not in plant:
                        return f"{requested_field.replace('_', ' ').capitalize()} not available for {plant_name} at {start_timestamp}."
                    value = plant[requested_field]
                    return f"{requested_field.replace('_', ' ').capitalize()} for {plant_name} at {start_timestamp}: {value}"
            return f"No plant found matching '{match.group(1)}'. Available plants: {[p.get('name', 'Unknown') for p in all_plants]}"
        else:
            return "Could not identify plant name in your query. Please try again specifying the plant name."

    except Exception as e:
        print(f"Error processing plant info: {str(e)}")
        return "An error occurred while processing your request."
