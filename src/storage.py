import pickle
import hashlib

__items = dict()


def store(item):
    hash_algo = hashlib.md5()
    hash_algo.update(item['url'].encode('utf-8'))
    key = hash_algo.hexdigest()
    if key in __items:
        raise Exception('Item with hash {} already exists in storage.'.format(key))
    else:
        __items[key] = item


def reset():
    __items.clear()


def write_to_disk(file=None):
    if file is not None:
        pickle.dump(obj=__items, file=file)
    else:
        with open('./storage.pickle', 'wb') as file:
            pickle.dump(obj=__items, file=file)


def read_from_disk(file=None):
    global __items

    if file is not None:
        __items = pickle.load(file=file)
    else:
        with open('./storage.pickle', 'rb') as file:
            __items = pickle.load(file=file)


def get_count():
    return len(__items)