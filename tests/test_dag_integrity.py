"""DAG integrity test (provided — do not delete).

The 20-line safety net from Chapter 6 ("Testing DAGs"). It loads every
DAG in ``dags/`` and fails if any of them has an import error, which is
the failure mode that silently drops a DAG from the scheduler without a
red run to warn you.

Run it locally before every push:

    astro dev pytest tests/test_dag_integrity.py --args "-v"

Required for all tiers. Keep it passing.
"""

from airflow.models import DagBag


def _make_dag_bag():
    """Build a DagBag across Airflow versions with differing signatures."""
    try:
        return DagBag(dag_folder="dags", include_examples=False)
    except TypeError:
        return DagBag(dag_folder="dags")


def test_no_import_errors():
    """Every .py in dags/ must import cleanly."""
    dag_bag = _make_dag_bag()
    assert dag_bag.import_errors == {}, (
        f"DAG import errors: {dag_bag.import_errors}"
    )


def test_every_dag_has_tags():
    """Light convention check so DAGs are discoverable via the UI tag filter."""
    dag_bag = _make_dag_bag()
    for dag_id, dag in dag_bag.dags.items():
        assert dag.tags, f"DAG {dag_id} is missing tags"
