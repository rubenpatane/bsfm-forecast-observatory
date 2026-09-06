#!/usr/bin/env python3
"""Download year-scoped official BTS T-100 extracts with hash manifests."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import http.cookiejar
import json
from pathlib import Path
import urllib.parse
import urllib.request


URL = 'https://www.transtats.bts.gov/DL_SelectFields.aspx?QO_fu146_anzr=Nv4Pn&gnoyr_VQ=FMG'
FIELDS = ('DEPARTURES_PERFORMED', 'AIRCRAFT_TYPE', 'YEAR', 'MONTH', 'CLASS')


class _HiddenFields(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'input' and values.get('type') == 'hidden' and values.get('name'):
            self.values[values['name']] = values.get('value', '')


def _opener():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def download_year(year, output_dir):
    year = int(year)
    if year < 1990:
        raise ValueError('T-100 year must be 1990 or later')
    client = _opener()
    request = urllib.request.Request(URL, headers={'User-Agent': 'BSFM-public-research/1.0'})
    with client.open(request, timeout=60) as response:
        page = response.read().decode('utf-8')
    parser = _HiddenFields()
    parser.feed(page)
    form = {
        **parser.values,
        'cboGeography': 'All',
        'cboYear': str(year),
        'cboPeriod': 'All',
        'btnDownload': 'Download',
        **{field: 'on' for field in FIELDS},
    }
    post = urllib.parse.urlencode(form).encode('ascii')
    request = urllib.request.Request(
        URL, data=post,
        headers={'User-Agent': 'BSFM-public-research/1.0', 'Content-Type': 'application/x-www-form-urlencoded'},
    )
    with client.open(request, timeout=300) as response:
        content = response.read()
        content_type = response.headers.get('Content-Type', '')
        disposition = response.headers.get('Content-Disposition', '')
    if not content.startswith(b'PK'):
        raise RuntimeError(f'BTS did not return a ZIP archive (content-type={content_type!r})')

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f'bts-t100-segment-all-carriers-{year}.zip'
    archive.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()
    manifest = {
        'schema': 'bsfm.bts-download-manifest.v1',
        'publisher': 'U.S. Department of Transportation / Bureau of Transportation Statistics',
        'dataset': 'T-100 Segment (All Carriers)',
        'source_url': URL,
        'query': {'year': year, 'period': 'All', 'geography': 'All', 'fields': list(FIELDS)},
        'retrieved_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'response_content_type': content_type,
        'response_content_disposition': disposition,
        'filename': archive.name,
        'bytes': len(content),
        'sha256': digest,
    }
    manifest_path = archive.with_suffix('.manifest.json')
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('years', nargs='+', type=int)
    parser.add_argument('--output-dir', default='data/cache/bts-t100')
    args = parser.parse_args()
    for year in args.years:
        print(json.dumps(download_year(year, args.output_dir), sort_keys=True))


if __name__ == '__main__':
    main()
