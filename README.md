# End-to-End Data Engineering & Analysis Pipeline

An end-to-end pipeline that streams real-world product recall data (French government "RappelConso" API) through **Kafka**, processes it with **Spark**, orchestrates everything with **Airflow**, stores it in **PostgreSQL**, and finishes with a **Python/pandas analysis layer** that turns the raw data into insights and charts.

## Tech Stack

| Layer | Tool |
|---|---|
| Message Queue | Apache Kafka |
| Stream Processing | Apache Spark (PySpark) |
| Orchestration | Apache Airflow |
| Storage | PostgreSQL |
| Analysis | Python, pandas, matplotlib |
| Containerization | Docker / docker-compose |

## Architecture

```
API (data.economie.gouv.fr)
      │
      ▼
  Kafka topic ──▶ Spark job ──▶ PostgreSQL ──▶ analysis/analyze_recalls.py ──▶ charts & stats
      ▲
      │
  Airflow DAG (daily schedule, orchestrates the streaming + processing steps)
```

## How It Works

1. **Data Streaming** — a Kafka producer pulls product recall records from the RappelConso public API and publishes them to a Kafka topic ([src/kafka_client/kafka_stream_data.py](src/kafka_client/kafka_stream_data.py)). Records are cleaned/normalized before being sent ([src/kafka_client/transformations.py](src/kafka_client/transformations.py)).
2. **Data Processing** — a Spark structured streaming job consumes from the Kafka topic and writes the data into PostgreSQL ([src/spark_pgsql/spark_streaming.py](src/spark_pgsql/spark_streaming.py)).
3. **Orchestration** — an Airflow DAG runs the streaming and Spark steps on a daily schedule ([airflow_resources/dags/dag_kafka_spark.py](airflow_resources/dags/dag_kafka_spark.py)). In a production setting the Kafka producer would run continuously instead of on a schedule.
4. **Analysis** — once data lands in Postgres, [analysis/analyze_recalls.py](analysis/analyze_recalls.py) queries it and produces:
   - Top recalled product categories
   - Recall trend over time (by month)
   - Most common recall reasons
   - Console summary stats

   Charts are saved to `analysis/output/`.

Everything runs in Docker via `docker-compose`.

## Data Source

Data comes from the [RappelConso](https://www.data.gouv.fr/) open dataset — official French government records of product recalls, including product category, recall reason, health risks, and consumer safety recommendations.

## Project Structure

```
src/
  kafka_client/       # Kafka producer + data transformations
  spark_pgsql/        # Spark job that writes to Postgres
  constants.py         # API URL, DB fields, column config
airflow_resources/
  dags/                # Airflow DAG definition
scripts/
  create_table.py      # Creates the Postgres table
analysis/
  analyze_recalls.py   # Post-pipeline analysis & charts
docker-compose.yml           # Kafka + Kafka UI + docker-proxy
docker-compose-airflow.yaml  # Airflow services
```

## Getting Started

1. Set up a `.env` with `POSTGRES_PASSWORD` and any other required variables.
2. Start Kafka: `docker-compose up -d`
3. Start Airflow: `docker-compose -f docker-compose-airflow.yaml up -d`
4. Create the Postgres table: `python scripts/create_table.py`
5. Trigger the `kafka_spark_dag` DAG from the Airflow UI (`localhost:8080`) to run the pipeline.
6. Once data has landed in Postgres, run the analysis: `python analysis/analyze_recalls.py`
