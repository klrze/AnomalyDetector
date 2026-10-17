import psycopg2


def initialize_database():
  conn = psycopg2.connect(
      dbname="postgres",
      user="postgres",
      password="Klarizzem22",  
      host="localhost",
      port="5432",
  )
  conn.autocommit = True
  cur = conn.cursor()

  cur.execute("SELECT 1 FROM pg_database WHERE datname = 'nasa_telemetry'")
  if not cur.fetchone():
    cur.execute("CREATE DATABASE nasa_telemetry;")
    print("Database 'nasa_telemetry' created successfully.")
  else:
    print("Database 'nasa_telemetry' already exists.")

  cur.close()
  conn.close()

  conn = psycopg2.connect(
      dbname="nasa_telemetry",
      user="postgres",
      password="Klarizzem22",
      host="localhost",
      port="5432",
  )
  cur = conn.cursor()

  sensor_columns = ", ".join([f"sensor_{i} FLOAT" for i in range(25)])
  telemetry_table_query = f"""
    CREATE TABLE IF NOT EXISTS telemetry_data (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        {sensor_columns}
    );
    """
  cur.execute(telemetry_table_query)

  anomaly_table_query = """
    CREATE TABLE IF NOT EXISTS anomaly_labels (
        id SERIAL PRIMARY KEY,
        channel_id VARCHAR(50) NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP NOT NULL,
        description TEXT
    );
    """
  cur.execute(anomaly_table_query)

  experiment_table_query = """
    CREATE TABLE IF NOT EXISTS experiment_log (
        id SERIAL PRIMARY KEY,
        run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        window_size INT NOT NULL,
        batch_size INT NOT NULL,
        learning_rate FLOAT NOT NULL,
        epochs INT NOT NULL,
        final_train_loss FLOAT NOT NULL,
        val_loss FLOAT NOT NULL,
        f1_score FLOAT,
        notes TEXT
    );
    """
  cur.execute(experiment_table_query)

  conn.commit()
  cur.close()
  conn.close()
  print("All database tables initialized successfully.")

if __name__ == "__main__":
  initialize_database()