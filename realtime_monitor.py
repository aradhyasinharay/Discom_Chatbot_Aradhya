from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from pymongo.errors import PyMongoError

# Connect
client = MongoClient("mongodb://localhost:27017/")
db = client['power_theft']
collection = db['consumption_data']


# With your synthetic date:
today_str = "2021-06-15"  # ← or any other date in your synthetic dataset
#(while working with real time data keep changing the date)

# Only fetch today's data (or latest)
today = datetime.strptime(today_str, "%Y-%m-%d")

tomorrow = today + pd.Timedelta(days=1)

# Fetch records for today only
cursor = collection.find({
    "Timestamp": {"$gte": today, "$lt": tomorrow}
})
#fetch data
data = list(cursor)
# Convert to DataFrame
df = pd.DataFrame(data)

if df.empty:
    print("ℹ️ No new records found for today.")
else:
    # Clean and label
    df['Loss Percentage'] = pd.to_numeric(df['Loss Percentage'], errors='coerce')
    df['label'] = df['Loss Percentage'].apply(lambda x: 'potential theft' if x > 70 else 'normal')

    # Save to CSV (optional)
    df.to_csv(f"labeled_{today_str}.csv", index=False)

    # Update back to MongoDB
    from pymongo.errors import PyMongoError

    updated = 0
    for record in df[['_id', 'label']].to_dict(orient='records'):
        try:
            collection.update_one({'_id': record['_id']}, {'$set': {'label': record['label']}})
            updated += 1
        except PyMongoError as e:
            print(f"⚠️ Failed to update record {record['_id']}: {e}")

    print(f"✅ Updated {updated} MongoDB records with labels.")

    print(f"✅ Labeled {len(df)} records from {today_str} with potential theft flags.")

