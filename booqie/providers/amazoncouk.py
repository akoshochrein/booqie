from .provider_base import ProviderBase
from cached_property import cached_property
from fuzzywuzzy import fuzz


class ProviderAmazonCoUk(ProviderBase):

    def __init__(self, search_term):
        url_template = 'http://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Dstripbooks&field-keywords={search_term}'
        super(ProviderAmazonCoUk, self).__init__(url_template, search_term)
        self.raw_books = self.soup.select('div.s-item-container')

    @cached_property
    def books(self):
        result_books = []
        for raw_book in self.raw_books:
            title_select = raw_book.select('a.s-access-detail-page')
            if title_select:
                title = title_select[0].text
                price_base_select = raw_book.select('span.s-price') or raw_book.select('span.a-color-price')
                match_rate = fuzz.ratio(self.search_term.lower(), title.lower())

                try:
                    author = raw_book.select('div.a-row.a-spacing-none')[0].select('span')[1].text
                except IndexError:
                    author = '????'

                try:
                    price = '{0:.2f}'.format(float(price_base_select[0].text.encode('ascii', 'ignore')))
                except IndexError:
                    price = '????'

                result_books.append({
                    'title': title,
                    'author': author,
                    'match_rate': match_rate,
                    'price': price
                })
        return result_books
