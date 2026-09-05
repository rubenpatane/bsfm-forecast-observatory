from __future__ import annotations

from .integrity import digest


def build_model_record(model_id, model, training_snapshot, evaluation, status='candidate'):
    """Build a content-addressed model registry record.

    Promotion is a status recorded only after the independent promotion gate;
    this helper never promotes by inference.
    """
    if status not in {'candidate','promoted','rejected'}:
        raise ValueError('invalid model status')
    if not str(model_id).strip():
        raise ValueError('model_id required')
    record={
        'schema':'bsfm.model-registry-record.v1',
        'model_id':str(model_id),
        'status':status,
        'model_hash':digest(model),
        'training_snapshot_hash':digest(training_snapshot),
        'evaluation_hash':digest(evaluation),
    }
    record['record_hash']=digest(record)
    return record


def promote_record(record, promotion_gate):
    """Return a promoted derivative only when the explicit gate passed."""
    if promotion_gate.get('pass') is not True:
        raise ValueError('promotion gate is closed')
    promoted=dict(record); promoted['status']='promoted'; promoted.pop('record_hash',None)
    promoted['record_hash']=digest(promoted)
    return promoted
