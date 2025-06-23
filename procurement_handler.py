import re
import requests
from datetime import datetime
from logger import logger
from normalizer import normalize
from urllib.parse import quote
from utils import fuzzy_match


def handle_procurement_info(original_message, date_str, time_obj):
    try:
        from urllib.parse import quote

        start_timestamp = f"{date_str} {time_obj.strftime('%H:%M:%S')}"
        url = f"http://127.0.0.1:5000/procurement?start_date={quote(start_timestamp)}&price_cap=10"
        response = requests.get(url)

        if response.status_code != 200:
            return "Failed to fetch procurement data."

        data = response.json()

        # Combine Must_Run and Remaining_Plants if they exist
        all_plants = data.get("Must_Run", []) + data.get("Remaining_Plants", [])

        if not all_plants:
            return "No procurement data available for the given time."

        # Add cost_generated (Generated_Cost) field
        for plant in all_plants:
            vc = plant.get("Variable_Cost", 0.0)
            gen = plant.get("generated_energy", 0.0)
            plant["Generated_Cost"] = round(vc * gen, 2)

        message = normalize(original_message)

        field_map = {
            "banking unit": "Banking_Unit",
            "banked unit": "Banking_Unit",
            "generated energy": "generated_energy",
            "banking": "Banking_unit",
            "banking contribution": "Banking_unit",
            "energy": "Generated_Energy",
            "energy generated": "generated_Energy",
            "energy generation": "generated_Energy",
            "banked contribution": "Banking_unit",
            "banked": "Banking_unit",
            "demand banked": "Banking_unit",
            "energy banked": "Banking_unit",
            "generated cost": "Generated_Cost",
            "generation cost": "Generated_Cost",
            "cost generated": "Generated_Cost",
            "cost generation": "Generated_Cost",
        }

        requested_field = None
        for k in field_map:
            if k in message:
                requested_field = field_map[k]
                break

        if not requested_field:
            return "Please specify whether you want IEX cost, generated energy, banking unit or cost generated"

        if requested_field in data:
            return f"{requested_field.replace('_', ' ').capitalize()} at {start_timestamp}: {data[requested_field]}"

        match = re.search(r"(?:by|for|of)\s+([a-z0-9\s\-&/]+?)(?=\s+(?:on|at)\s+|[\?\.!]|$)", message)

        if match:
            print("🧠 Raw match group:", match.group(1))
            plant_query = normalize(match.group(1).replace('/', ' '))
            for plant in all_plants:
                if fuzzy_match(normalize(plant["plant_name"]), plant_query):
                    if requested_field not in plant:
                        return f"{requested_field.replace('_', ' ').capitalize()} not available for {plant['plant_name']} at {start_timestamp}."

                    value = plant[requested_field]
                    return f"{requested_field.replace('_', ' ').capitalize()} for {plant['plant_name']} at {start_timestamp}: {value}"

            return f"No plant found matching '{match.group(1)}'."

        else:
            lines = []
            for plant in all_plants:
                value = plant.get(requested_field, 'N/A')
                lines.append(f"{plant['plant_name']} ({requested_field.replace('_', ' ')}): {value}")
            return f"{requested_field.replace('_', ' ').capitalize()} values for all plants at {start_timestamp}:\n" + "\n".join(lines)

    except Exception as e:
        logger.error(f"Procurement API error: {e}")
        return "Error fetching procurement data."

