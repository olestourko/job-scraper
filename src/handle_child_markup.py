from scrapy.selector import Selector
from .utils import get_inner_text

# Running (from above src/ directory):
# python -m src.handle_child_markup

if __name__ == '__main__':
    body = '<div class="parent">A<br>B</div>'
    print(get_inner_text(Selector(text=body).css('.parent *::text')))