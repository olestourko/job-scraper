import unittest
from src import storage
from scrapy.loader import ItemLoader
from src.spiders.stackoverflow import JobPost
from os import path

class TestStorage(unittest.TestCase):

    def setUp(self):
        loader = ItemLoader(item=JobPost())
        loader.add_value(field_name='url', value='url_1')
        loader.add_value(field_name='job_title', value='job_title_1')
        loader.add_value(field_name='employer', value='employer_1')
        loader.add_value(field_name='technologies', value=['tech_1'])
        loader.add_value(field_name='description', value='description_1')
        loader.load_item()
        self.item = loader.item
        storage.reset()

    def test_store(self):
        storage.store(self.item)
        got_exception = False
        try:
            storage.store(self.item)
        except Exception as e:
            got_exception = True

        assert got_exception

    def test_write_to_disk(self):
        storage.store(self.item)
        with open('./tests/storage.pickle', 'wb') as file:
            storage.write_to_disk(file=file)
            assert path.exists('./tests/storage.pickle')

    def test_read_from_disk(self):
        storage.store(self.item)
        with open('./tests/storage.pickle', 'wb') as file:
            storage.write_to_disk(file=file)

        with open('./tests/storage.pickle', 'rb') as file:
            storage.read_from_disk(file=file)
            assert storage.get_count() == 1

if __name__ == '__main__':
    unittest.main()