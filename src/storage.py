from .spiders.stackoverflow import JobPost
import pickle

__items = dict()


def store(item):
    key = JobPost.get_mutable_hash(item)
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
            print('A')


def read_from_disk(file=None):
    if file is not None:
        __items = pickle.load(file=file)
    else:
        with open('./storage.pickle', 'rb') as file:
            __items = pickle.load(file=file)


def get_count():
    return len(__items)