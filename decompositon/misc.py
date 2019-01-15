from joblib import Parallel, delayed
from tqdm import tqdm
import time
from typing import Iterable


def parallel(function, input : Iterable, total : int, cores : int = 4):
    """
    Helper  function
    :param function: funkcija, ki jo bomo izvajali
    :param input: iterable kosov na katerih bomo izvajali funkcijo
    :param total: dolžina input
    :param cores: število fork procesov
    :return:
    """
    p = Parallel(n_jobs=cores)(delayed(function)(x) for x in tqdm(input, total=total))
    return p


def timing(f):
    """
    Decorator za funkcije. Ob koncu izvajanja izpiše kako dolgo je funkcija trajala
    """
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))

        return ret

    return wrap
