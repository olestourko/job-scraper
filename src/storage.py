import pickle

__items = dict()


def store(item):
    key = item.get_mutable_hash()
    if key in __items:
        raise Exception('The item has already been stored previously.')
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
    if file is not None:
        __items = pickle.load(file=file)
    else:
        with open('./storage.pickle', 'rb') as file:
            __items = pickle.load(file=file)


def get_count():
    return len(__items)