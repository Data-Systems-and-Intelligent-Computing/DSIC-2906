"""DAG akuisisi -> Gold untuk DSIC-2906.

Opsional: jalur setara tersedia lewat scripts/ + Makefile. DAG ini memanggil
script yang sama persis agar kedua jalur menghasilkan hasil identik.

DAG berhenti di build_gold. Held-out freeze, eksperimen utama, dan analisis
dijalankan manual karena tiap tahap punya quality gate yang harus diperiksa
manusia lebih dulu.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

REPO = "/opt/airflow/repo"

DEFAULT_ARGS = {
    "owner": "dsic2906",
    "retries": 1,
    "depends_on_past": False,
}

# Akuisisi sengaja tidak dijadwalkan berulang: source cutoff harus dibekukan,
# dan penambahan sumber setelah cutoff membatalkan hasil held-out.
with DAG(
    dag_id="dsic2906_acquisition_to_gold",
    description="Raw -> Bronze -> Silver -> Gold untuk DSIC-2906",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    tags=["dsic2906", "lakehouse"],
) as dag:

    steps = [
        ("ingest_jadesta", "01_ingest_jadesta.sh"),
        ("acquire_wikimedia", "02_acquire_wikimedia.sh"),
        ("acquire_news", "03_acquire_news.sh"),
        ("freeze_sources", "04_freeze_sources.sh"),
        ("build_bronze", "05_build_bronze.sh"),
        ("build_silver", "06_build_silver.sh"),
        ("build_gold", "07_build_gold.sh"),
    ]

    previous = None
    for task_id, script in steps:
        task = BashOperator(
            task_id=task_id,
            bash_command=f"cd {REPO} && bash scripts/{script}",
        )
        if previous:
            previous >> task
        previous = task
