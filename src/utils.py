import hashlib
from .constants import \
    OWN_REPLAY_TAG, \
    BENCH_REPLAY_TAG


def get_file_hash(filedata):
    return hashlib.md5(filedata).hexdigest()


def valid_names(request):
    """checks whether incoming data has correct key names"""
    if OWN_REPLAY_TAG not in request.files:
        return False
    elif BENCH_REPLAY_TAG not in request.files:
        return False
    else:
        return True


def add_if_key_exists(dictionary: dict, key: str, value: int):
    if key in dictionary.keys():
        dictionary[key] += value
    else:
        dictionary[key] = value
