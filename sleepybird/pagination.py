import math
from flask import current_app


class Pagination:
    """Provide pagination support."""

    def __init__(self, page, count):
        self.page = page
        self.count = count
        self.visible_page_count = current_app.config['VISIBLE_PAGE_COUNT']
        self.page_size = current_app.config['PAGE_SIZE']
        self.pages = list()
        self.last_page = int(math.ceil(self.count / self.page_size))

    def get_pages(self):
        prev_navigation, next_navigation = self.get_navigation()
        self.prepare_visible_pages()
        self.pages = prev_navigation + self.pages + next_navigation
        return self.pages

    def get_navigation(self):
        prev_naviation = [{'page_label': '&laquo;',
                           'href': self.page - 1,
                           'class': 'disabled' if self.page == 1 else ''}]
        next_navigation = [{'page_label': '&raquo;',
                            'href': self.page + 1,
                            'class': 'disabled' if self.page >= self.last_page else ''}]
        return prev_naviation, next_navigation

    def prepare_visible_pages(self):
        if self.last_page > self.visible_page_count:
            self.prepare_first_pages()
            self.append_current_page()
            pages_left = self.visible_page_count - len(self.pages)
            self.prepare_last_pages(pages_left)
        else:
            self.prepare_full_range()

    def prepare_first_pages(self):
        middle_page = min(self.visible_page_count, self.last_page) // 2
        if self.page <= middle_page + 1:
            self.extend_by_range(1, self.page)
        else:
            first_visible_page = self.page - (middle_page - 2)
            self.prepend_first_page(first_visible_page)
            self.extend_by_range(first_visible_page, self.page)

    def append_current_page(self):
        self.pages.append({'page_label': self.page,
                           'href': self.page,
                           'class': 'active'})

    def prepare_last_pages(self, pages_left):
        if self.last_page - self.page <= pages_left:
            self.extend_by_range(self.page + 1, self.last_page + 1)

            if self.pages[1]['page_label'] == '...':
                while len(self.pages) < self.visible_page_count:
                    first_visible_page = self.pages[2]['page_label'] - 1
                    self.pages.insert(2, {'page_label': first_visible_page,
                                          'href': first_visible_page,
                                          'class': ''})
                    self.pages[1]['href'] = first_visible_page - 1
        else:
            last_visible_page = self.page + (pages_left - 2)
            self.extend_by_range(self.page + 1, last_visible_page + 1)
            self.append_last_page(last_visible_page)

    def extend_by_range(self, low_bound, high_bound):
        for p in range(low_bound, high_bound):
            self.pages.append({'page_label': p,
                               'href': p,
                               'class': ''})

    def prepend_first_page(self, first_visible_page):
        self.pages.append({'page_label': 1,
                           'href': 1,
                           'class': ''})
        self.pages.append({'page_label': '...',
                           'href': first_visible_page - 1,
                           'class': ''})

    def append_last_page(self, last_visible_page):
        self.pages.append({'page_label': '...',
                           'href': last_visible_page + 1,
                           'class': ''})
        self.pages.append({'page_label': self.last_page,
                           'href': self.last_page,
                           'class': ''})

    def prepare_full_range(self):
        self.extend_by_range(1, self.last_page + 1)
        self.pages[self.page - 1]['class'] = 'active'
