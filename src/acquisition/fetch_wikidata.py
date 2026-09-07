"""Akuisisi Wikidata via SPARQL/API.

Peran: structured corroboration. Family lineage `wikimedia` dibagi dengan
Wikipedia agar keduanya tidak terhitung dua sumber independen.
"""
from src.utils.logging import get_logger

log = get_logger(__name__)

SOURCE_ID = "wikidata"
SOURCE_FAMILY = "wikimedia"

# Ambil entitas as-of cutoff, bukan revisi terbaru saat analisis dijalankan.
SPARQL_TEMPLATE = """
SELECT ?item ?itemLabel ?coord ?instanceOfLabel WHERE {
  VALUES ?item { %s }
  OPTIONAL { ?item wdt:P625 ?coord. }
  OPTIONAL { ?item wdt:P31 ?instanceOf. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "id,en". }
}
"""


def fetch(qids, user_agent, cutoff=None):
    raise NotImplementedError("Implementasikan pada H3-H4 (scripts/02_acquire_wikimedia.sh).")
