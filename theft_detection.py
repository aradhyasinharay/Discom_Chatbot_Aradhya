from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

def detect_theft(customer_id, date=None, time=None):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['power_theft']
    collection = db['consumption_data']

    # Validate minimum input
    if not date:
        print("❌ Please provide at least a date for analysis.")
        return None

    # Construct query
    if time:
        # 15-min block range
        timestamp_str = f"{date.strip()} {time.strip()}"
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("❌ Invalid date/time format. Please use YYYY-MM-DD and HH:MM:SS.")
            return None

        query = {
            "customer_id": customer_id,
            "Timestamp": {
                "$gte": timestamp,
                "$lt": timestamp + timedelta(minutes=15)
            }
        }
    else:
        # Daily range
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        next_day = date_obj + timedelta(days=1)
        query = {
            "customer_id": customer_id,
            "Timestamp": {
                "$gte": date_obj,
                "$lt": next_day
            }
        }

    # Fetch data
    data = list(collection.find(query))
    if not data:
        print("❌ No data found for given input.")
        return None

    df = pd.DataFrame(data)
    df['Loss Percentage'] = pd.to_numeric(df['Loss Percentage'], errors='coerce')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    if time:
        # Get full customer history
        full_data = list(collection.find({"customer_id": customer_id}))
        full_df = pd.DataFrame(full_data)
        full_df['Loss Percentage'] = pd.to_numeric(full_df['Loss Percentage'], errors='coerce')

        # Compute threshold using 95th percentile
        threshold = full_df['Loss Percentage'].quantile(0.95)
        print(f"📊 15-min Threshold (95th percentile): {threshold:.2f}%")

        # Flag suspicious records
        suspicious = df[df['Loss Percentage'] > threshold]

        if suspicious.empty:
            print("ℹ️ No theft detected in this 15-min block.")
            print("Loss Percentages in this block:")
            print(df[['Timestamp', 'Loss Percentage']])
            return None
        else:
            return suspicious

    else:
        # Daily average logic
        daily_avg = df['Loss Percentage'].mean()
        std = df['Loss Percentage'].std()
        threshold = daily_avg + 2 * std
        print(f"📊 Daily Avg: {daily_avg:.2f}%, Threshold: {threshold:.2f}%")

        return pd.DataFrame([{
            "customer_id": customer_id,
            "date": date,
            "avg_loss_percentage": daily_avg,
            "is_suspicious": daily_avg > threshold
        }])



app = Flask(__name__)

@app.route('/detect_theft', methods=['GET'])
def theft_api():
    customer_id = request.args.get('customer_id')
    date = request.args.get('date')
    time = request.args.get('time')  # optional

    result = detect_theft(customer_id, date=date, time=time)

    if result is None:
        # Fetch the actual block-level values just for feedback
        from datetime import datetime, timedelta
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/")
        db = client['power_theft']
        collection = db['consumption_data']

        try:
            timestamp = datetime.strptime(f"{date.strip()} {time.strip()}", "%Y-%m-%d %H:%M:%S")
        except:
            return jsonify({"error": "Invalid date/time format."}), 400

        block_data = list(collection.find({
            "customer_id": customer_id,
            "Timestamp": {
                "$gte": timestamp,
                "$lt": timestamp + timedelta(minutes=15)
            }
        }))

        # Format it
        cleaned = [
            {
                "Timestamp": str(doc["Timestamp"]),
                "Loss Percentage": round(float(doc.get("Loss Percentage", 0)), 2)
            }
            for doc in block_data
        ]

        return jsonify({
            "message": "No theft detected in this 15-min block.",
            "loss_percentages": cleaned
        }), 200

    return result.to_json(orient="records"), 200


if __name__ == '__main__':
    app.run(port=8000, debug=True)
