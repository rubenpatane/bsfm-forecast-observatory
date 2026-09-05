from bsfm.sources import sha

def test_sha_is_deterministic():
 assert sha(b'bsfm')==sha(b'bsfm')
 assert sha(b'bsfm')!=sha(b'BSFM')
