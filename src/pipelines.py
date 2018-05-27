from src import storage
import logging

class StoragePipeline(object):
    def process_item(self, item, spider):
        try:
            storage.store(item)
        except Exception as e:
            logging.debug(msg=e)

        return item
