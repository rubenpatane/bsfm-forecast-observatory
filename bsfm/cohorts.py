from __future__ import annotations
import re


_ICAO_EQUIPMENT_COHORTS = {
    # 727
    'B721': '727', 'B722': '727', 'B72Q': '727',
    # 737 Original / Classic / NG / MAX
    'B731': '737-Original', 'B732': '737-Original',
    'B733': '737-Classic', 'B734': '737-Classic', 'B735': '737-Classic',
    'B736': '737-NG', 'B737': '737-NG', 'B738': '737-NG', 'B739': '737-NG',
    'B37M': '737-MAX', 'B38M': '737-MAX', 'B39M': '737-MAX',
    # 747
    'B741': '747', 'B742': '747', 'B743': '747', 'B744': '747',
    'B748': '747', 'B74S': '747',
    # 757 / 767 / 777 / 787
    'B752': '757', 'B753': '757',
    'B762': '767', 'B763': '767', 'B764': '767',
    'B772': '777', 'B773': '777', 'B77L': '777', 'B77W': '777',
    'B788': '787', 'B789': '787', 'B78X': '787',
}


def cohort_from_icao_equipment(code):
    """Map a specific ICAO aircraft type designator to a BSFM exposure cohort.

    This mapping is deliberately allowlisted. Generic/ambiguous designators and
    future designators not explicitly reviewed return None rather than being
    inferred from fleet shares or string resemblance.
    """
    key = str(code or '').upper().strip()
    return _ICAO_EQUIPMENT_COHORTS.get(key)


def _737_series(model: str):
    """Return the 737 series bucket from canonical or customer-code variants.

    Examples: 737-236A -> 200, 737-8K5 -> 800, 737-7H4 -> 700.
    MAX designations are handled before this helper.
    """
    m = str(model or '').upper().replace('BOEING', '').strip().replace(' ', '')
    hit = re.search(r'737-([1-9])', m)
    if not hit:
        return None
    lead = hit.group(1)
    return {
        '1': '100', '2': '200', '3': '300', '4': '400', '5': '500',
        '6': '600', '7': '700', '8': '800', '9': '900',
    }.get(lead)


def boeing_cohort(model):
    """Map supported Boeing commercial-jet model strings to explicit cohorts.

    737 Original and Classic are intentionally distinct. Customer-code model
    strings (e.g. 737-236A, 737-8K5) are mapped by series. Unknown or ambiguous
    model strings fail closed rather than being forced into an exposure cohort.
    """
    m = str(model or '').upper().replace('BOEING', '').strip()
    compact = m.replace(' ', '').replace('_', '-')

    # MAX must be resolved before generic 737 series parsing because 737-8/9 are
    # used as MAX marketing/type designations when no legacy customer code follows.
    if '737MAX' in compact or re.search(r'737-(?:7|8|9|10)MAX', compact):
        return '737-MAX'
    if compact in {'737-7', '737-8', '737-9', '737-10'}:
        return '737-MAX'

    series = _737_series(compact)
    if series in {'100', '200'}:
        return '737-Original'
    if series in {'300', '400', '500'}:
        return '737-Classic'
    if series in {'600', '700', '800', '900'}:
        return '737-NG'

    if compact.startswith('727'):
        return '727'
    for family in ('747', '757', '767', '777', '787'):
        if compact.startswith(family):
            return family
    return None
