import pickle
import hashlib
from scrapy.loader import ItemLoader
from src.spiders.stackoverflow import JobPost

__items = dict()


def dict_to_item(item_dict):
    item_loader = ItemLoader(item=JobPost())
    for key in item_dict:
        item_loader.add_value(key, item_dict[key])

    return item_loader.load_item()


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
    items_as_dicts = {key: dict(item) for key, item in __items.items()}
    if file is not None:
        pickle.dump(obj=items_as_dicts, file=file)
    else:
        with open('./storage.pickle', 'wb') as file:
            pickle.dump(obj=items_as_dicts, file=file)


def read_from_disk(file=None):
    global __items

    if file is not None:
        items_as_dicts = pickle.load(file=file)
    else:
        with open('./storage.pickle', 'rb') as file:
            items_as_dicts = pickle.load(file=file)

    __items = {key: dict_to_item(item) for key, item in items_as_dicts.items()}


def get_count():
    return len(__items)