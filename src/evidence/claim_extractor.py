"""Ekstraksi evidence claim menjadi schema bersama.

BUKAN novelty (publication boundary). Ekstraktor dibekukan sebelum held-out
dan versinya dicatat di setiap claim agar extraction error dapat dipisahkan
dari routing error saat failure analysis.
"""
from src.evidence.support_span import has_valid_support_span

EXTRACTOR_VERSION = "v1"


def build_claim(
    claim_id,
    entity_id,
    attribute,
    normalized_value,
    source_id,
    source_family,
    representation_type,
    published_or_observed_at,
    raw_value=None,
    story_lineage_id=None,
    url_or_reference=None,
    snapshot_id=None,
    support_span=None,
    fetched_at=None,
):
    """Rakit satu claim sesuai schemas/evidence_claim.schema.json."""
    claim = {
        "claim_id": claim_id,
        "entity_id": entity_id,
        "attribute": attribute,
        "raw_value": raw_value,
        "normalized_value": normalized_value,
        "source_id": source_id,
        "source_family": source_family,
        "story_lineage_id": story_lineage_id,
        "representation_type": representation_type,
        "published_or_observed_at": published_or_observed_at,
        "fetched_at": fetched_at,
        "url_or_reference": url_or_reference,
        "snapshot_id": snapshot_id,
        "support_span": support_span,
        "extractor_version": EXTRACTOR_VERSION,
    }
    claim["support_valid"] = has_valid_support_span(claim)
    return claim


def extract_from_structured(record, mapping):
    """Ubah satu baris structured (JADESTA/Wikidata) menjadi claim.

    Implementasikan dengan mapping atribut yang sudah dibekukan di
    configs/claim_extraction.yaml sebelum held-out.
    """
    raise NotImplementedError("Implementasikan setelah atribut final dibekukan (H7).")


def extract_from_text(document, entity_id, attribute):
    """Ekstrak claim dari artikel/teks, beserta supporting span-nya.

    Wajib mengembalikan support_span; tanpa itu claim akan ditandai unsupported
    dan tidak dihitung sebagai corroboration.
    """
    raise NotImplementedError("Implementasikan rule-based extractor pada H5-H6.")
