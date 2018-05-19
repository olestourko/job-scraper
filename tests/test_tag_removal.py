import unittest
from scrapy.selector import Selector
from src import utils


class TestTagRemoval(unittest.TestCase):
    def test_tag_removal(self):
        markup = '<div id="parent">A<div>B<div>C</div><div>D</div></div></div>'
        expected = 'A B C D'
        selector = Selector(text=markup)
        result = utils.get_inner_text(selector.css('#parent'))
        assert result == expected

if __name__ == '__main__':
    unittest.main()