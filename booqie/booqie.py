
import requests
import sys

from bs4 import BeautifulSoup
from collections import namedtuple
from fuzzywuzzy import fuzz

from providers.bookdepository import ProviderBookDepository


def main():

    search_term = sys.argv[1]
    result_books = []

    # bookdepository
    book_depository = ProviderBookDepository(
        url_template='http://www.bookdepository.com/search?searchTerm={search_term}&search=Find+book',
        search_term=search_term
    )
    result_books += book_depository.books

    # amazon.co.uk
    url_template = 'http://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Dstripbooks&field-keywords={search_term}'
    response = requests.get(url_template.format(
        search_term=search_term
    ))
    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('div.s-item-container')

    for raw_book in raw_books:
        title_select = raw_book.select('a.s-access-detail-page')
        if title_select:
            title = title_select[0].text
            price_base_select = raw_book.select('span.s-price') or raw_book.select('span.a-color-price')
            match_rate = fuzz.ratio(search_term.lower(), title.lower())

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

    def book_filter(b):
        if b['price'] == '????':
            return False
        if float(b['price']) <= 0:
            return False
        if int(b['match_rate']) < 70:
            return False
        return True

    result_books = filter(book_filter, result_books)
    print result_books


if __name__ == '__main__':
    main()
