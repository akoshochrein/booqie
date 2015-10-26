
import requests
import sys

from bs4 import BeautifulSoup
from collections import namedtuple
from fuzzywuzzy import fuzz

from providers.amazoncouk import ProviderAmazonCoUk
from providers.bookdepository import ProviderBookDepository


def main():

    search_term = sys.argv[1]
    result_books = []

    # bookdepository
    book_depository = ProviderBookDepository(search_term)
    result_books += book_depository.books

    # amazon.co.uk
    amazon_co_uk = ProviderAmazonCoUk(search_term)
    result_books += amazon_co_uk.books

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
