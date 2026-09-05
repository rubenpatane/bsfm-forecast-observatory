from __future__ import annotations


def boeing_cohort(model):
    """Map supported Boeing commercial-jet model strings to preregistered cohorts."""
    m=str(model or '').upper().replace('BOEING','').strip()
    compact=m.replace(' ','').replace('_','-')
    if any(x in compact for x in ('737-100','737-200')): return '737-Classic'
    if any(x in compact for x in ('737-300','737-400','737-500')): return '737-Classic'
    if any(x in compact for x in ('737-600','737-700','737-800','737-900')): return '737-NG'
    if any(x in compact for x in ('737MAX','737-7MAX','737-8MAX','737-9MAX','737-10MAX')) or compact in {'737-7','737-8','737-9','737-10'}: return '737-MAX'
    for family in ('747','757','767','777','787'):
        if compact.startswith(family): return family
    return None
