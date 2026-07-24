# RUNBOOK

## How to trigger the DAG manually

Open the Airflow UI, find dag_id `hannahwn_taxi_pipeline`, unpause it if needed,
then use Trigger DAG. For a specific month, set a logical date on the first of
that month (for example 2024-01-01 for January 2024). Confirm the run appears
under Grid / Graph and watch ingest_taxi_month first.

## How to run a backfill

From the Airflow host (with max_active_runs already set to 1 on the DAG):

```bash
airflow dags backfill hannahwn_taxi_pipeline \
  --start-date 2024-01-01 \
  --end-date 2024-03-01
```

Keep max-active-runs at 1 so months do not overlap on the shared Postgres schema.
Do not raise concurrency while a backfill is in progress.

## How to inspect task logs

In the UI open Grid for `hannahwn_taxi_pipeline`, click the failed or running
task square, then Log. Locally with Astro you can also use
`astro dev logs` or `docker compose logs` for the scheduler/worker. Look for the
printed partition `YYYY-MM` and any Postgres or HTTP errors from ingest.

## Top 3 likely failures and first response

1. TLC download 404 or timeout — check year_month from the logical date and retry;
   confirm the green_tripdata parquet exists for that month on the TLC CDN.
2. Postgres connection / permission errors — verify `azure_pg` conn in Airflow
   and that schema `airflow_hannahwn` exists and is writable by the login user.
3. dbt task fails after ingest — open the BashOperator log, confirm DBT_DIR path
   and PG_* env from the connection, then re-run the failed task only.
