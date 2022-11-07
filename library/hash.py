import hashlib

from kikiutils.string import s2b
from typing import Callable


def hash(fnc: Callable, text: str | bytes, return_bytes: bool) -> str | bytes:
    return fnc(s2b(text)).digest() if return_bytes else fnc(s2b(text)).hexdigest()


def md5(text: str | bytes, return_bytes: bool = False):
    return hash(hashlib.md5, text, return_bytes)


def sha3_224(text: str | bytes, return_bytes: bool = False):
    return hash(hashlib.sha3_224, text, return_bytes)


def sha3_256(text: str | bytes, return_bytes: bool = False):
    return hash(hashlib.sha3_256, text, return_bytes)


def sha3_384(text: str | bytes, return_bytes: bool = False):
    return hash(hashlib.sha3_384, text, return_bytes)


def sha3_512(text: str | bytes, return_bytes: bool = False):
    return hash(hashlib.sha3_512, text, return_bytes)
