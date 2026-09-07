"""Bronze -> Silver: canonical entities + evidence claims.

Silver adalah tempat normalisasi, entity linking, ekstraksi claim, dan
supporting span bertemu dalam satu schema bersama.
"""
from src.utils.logging import get_logger

log = get_logger(__name__)


def materialize_entities(bronze_rows, table="iceberg.silver.entities"):
    raise NotImplementedError("Implementasikan dengan Spark pada H5-H6 (scripts/06_build_silver.sh).")


def materialize_claims(bronze_rows, table="iceberg.silver.evidence_claims"):
    raise NotImplementedError("Implementasikan dengan Spark pada H5-H6 (scripts/06_build_silver.sh).")
