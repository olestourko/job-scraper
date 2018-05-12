import unittest
from .context import src
from scrapy.loader import ItemLoader
from src.spiders.stackoverflow import JobPost

class TestJobHash(unittest.TestCase):
    def test_hash(self):
        loader_1 = ItemLoader(item=JobPost())
        loader_1.add_value(field_name='url', value='url_1')
        loader_1.add_value(field_name='job_title', value='job_title_1')
        loader_1.add_value(field_name='employer', value='employer_1')
        loader_1.add_value(field_name='technologies', value=['tech_1'])
        loader_1.add_value(field_name='description', value='description_1')

        loader_2 = ItemLoader(item=JobPost())
        loader_2.add_value(field_name='url', value='url_2')
        loader_2.add_value(field_name='job_title', value='job_title_2')
        loader_2.add_value(field_name='employer', value='employer_2')
        loader_2.add_value(field_name='technologies', value=['tech_2'])
        loader_2.add_value(field_name='description', value='description_2')

        loader_3 = ItemLoader(item=JobPost())
        loader_3.add_value(field_name='url', value='url_2')
        loader_3.add_value(field_name='job_title', value='job_title_2')
        loader_3.add_value(field_name='employer', value='employer_2')
        loader_3.add_value(field_name='technologies', value=['tech_2'])
        loader_3.add_value(field_name='description', value='description_2')

        print(JobPost.get_mutable_hash(loader_1))

        assert hash(loader_1) != hash(loader_2)
        assert hash(loader_2) != hash(loader_3)
        assert JobPost.get_mutable_hash(loader_1) != JobPost.get_mutable_hash(loader_2)
        assert JobPost.get_mutable_hash(loader_2) == JobPost.get_mutable_hash(loader_3)

if __name__ == '__main__':
    unittest.main()