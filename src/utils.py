def get_inner_text(selector):
    inner_text = ''
    for child in selector:
        inner_text = '%s %s' % (inner_text, child.extract())

    return inner_text
