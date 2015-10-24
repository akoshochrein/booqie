
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def main():

    # bookdepository
    search_term = 'The Martian'
    response = requests.get('http://www.bookdepository.com/search?searchTerm={search_term}&search=Find+book'.format(
        search_term=search_term
    ))
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.select('div.book-item')

    for book in books:
        info = book.select('.item-info')[0]
        title = info.select('h3.title a')[0].text.strip()
        match_rate = fuzz.ratio(search_term, title)
        price = ' '.join(info.select('p.price')[0].text.encode('ascii', 'ignore').split()[:2])
        print match_rate, title, price


if __name__ == '__main__':
    main()
