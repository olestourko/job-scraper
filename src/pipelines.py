from src import storage

class StoragePipeline(object):
    def process_item(self, item, spider):
        storage.store(item)
        return item
