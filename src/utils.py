def get_inner_text(selector, seperator=' '):
    inner_text = ''

    first = True
    for text in selector.css('*::text').extract():
        if first:
            first = False
            inner_text = text
        else:
            inner_text = '%s%s%s' % (inner_text, seperator, text)

    return inner_text
