import ast
import datetime
import os
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def ingest_data(channel_id="P-1", data_dir="data"):
  conn = psycopg2.connect(
      dbname="nasa_telemetry",
      user="postgres",
      password="Klarizzem22", 
      host="localhost",
      port="5432",
  )
  cur = conn.cursor()

  cur.execute(
      "ALTER TABLE telemetry_data ADD COLUMN IF NOT EXISTS channel_id"
      " VARCHAR(50);"
  )

  base_time = datetime.datetime(2026, 1, 1, 0, 0, 0)

  npy_path = os.path.join(data_dir, "test", f"{channel_id}.npy")
  raw_telemetry = np.load(npy_path)

  telemetry_rows = []
  for row_idx, sensor_values in enumerate(raw_telemetry):
    current_time = base_time + datetime.timedelta(minutes=row_idx)
    row_tuple = (current_time, channel_id) + tuple(sensor_values.tolist())
    telemetry_rows.append(row_tuple)

  sensor_cols = ", ".join([f"sensor_{i}" for i in range(25)])
  insert_telemetry_query = f"""
        INSERT INTO telemetry_data (timestamp, channel_id, {sensor_cols})
        VALUES %s
    """
  execute_values(cur, insert_telemetry_query, telemetry_rows)
  print(
      f"Ingested {len(telemetry_rows)} telemetry rows for channel {channel_id}."
  )

  csv_path = os.path.join(data_dir, "labeled_anomalies.csv")
  df_anomalies = pd.read_csv(csv_path)

  channel_anomalies = df_anomalies[df_anomalies["chan_id"] == channel_id]

  anomaly_rows = []
  for _, row in channel_anomalies.iterrows():

    sequences = ast.literal_eval(row["anomaly_sequences"])
    raw_class = str(row["class"]).strip("[]")
    anomaly_classes = [c.strip(" \"'") for c in raw_class.split(",")]

    for (start_idx, end_idx), anom_class in zip(sequences, anomaly_classes):
      start_time = base_time + datetime.timedelta(minutes=int(start_idx))
      end_time = base_time + datetime.timedelta(minutes=int(end_idx))
      description = f"Anomaly type: {anom_class} (indices {start_idx} to {end_idx})"

      anomaly_rows.append((channel_id, start_time, end_time, description))

  insert_anomaly_query = """
        INSERT INTO anomaly_labels (channel_id, start_time, end_time, description)
        VALUES %s
    """
  if anomaly_rows:
    execute_values(cur, insert_anomaly_query, anomaly_rows)
    print(
        f"Ingested {len(anomaly_rows)} anomaly intervals for channel"
        f" {channel_id}."
    )

  conn.commit()
  cur.close()
  conn.close()
  print("Database ingestion complete and committed.")

if __name__ == "__main__":
  ingest_data()