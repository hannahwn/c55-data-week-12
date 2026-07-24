# AI assistance log

## Use 1

**Prompt I sent:** My Week 12 DAG calls `_partition_date()` inside ingest but the
helper is missing and the grader wants the partition from the run context, not a
hard-coded date. How do I get the logical date with Airflow 3 / `airflow.sdk`
without using the old `{{ ds }}` template in a TaskFlow task?

**What the model answered:** Import `get_current_context` from `airflow.sdk`,
call it inside the task, read `context["dag_run"]`, then use
`logical_date` (or `run_after` as fallback) and format with `strftime("%Y-%m-%d")`.
Keep that helper next to the DAG so every task can share the same partition
string for TLC URLs and Postgres loads.

**What I kept, changed, or discarded, and why:** I kept the small
`_partition_date` helper and the `get_current_context` import. I discarded
suggestions to hard-code a month or to pass `ds` only via Jinja on BashOperator,
because the ingest task is Python TaskFlow and needs the date in-process. No
connection strings or passwords were pasted into the chat.
