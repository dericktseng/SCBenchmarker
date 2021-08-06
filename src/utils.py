import hashlib
import concurrent.futures
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


def to_MM_SS(time_in_seconds):
    time_in_seconds = round(time_in_seconds)
    mm = str(time_in_seconds // 60).zfill(2)
    ss = str(time_in_seconds % 60).zfill(2)
    return "{}:{}".format(mm, ss)


def multiprocessMap(
        func,
        lst: list,
        allow_multiprocess: bool,
        max_workers: int):
    """ Maps func to each element in lst.

    parameters:
        func - the unary function to apply
        lst - list of elements to apply function to.
        allow_multiprocess - whether to use multiprocessing or not
        max_workers - max number of multiprocess workers

    returns:
        iterable where func is applied to every element
    """
    # uses multiprocess to load in parallel.
    if allow_multiprocess:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, path) for path in lst]
        return [f.result() for f in futures]
    else:
        return map(func, lst)
