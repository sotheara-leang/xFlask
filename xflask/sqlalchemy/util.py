class Page(object):

    def __init__(self, page=None, per_page=None, total_page=None, total=None, items=None):
        self.page = page
        self.per_page = per_page
        self.total_page = total_page
        self.total = total
        self.items = items

    @staticmethod
    def from_pagination(obj):
        return Page(page=obj.page, per_page=obj.per_page, total_page=obj.pages, total=obj.total, items=obj.items)
