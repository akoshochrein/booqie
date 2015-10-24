
import requests
from bs4 import BeautifulSoup


def main():

    # bookdepository
    response = requests.get('http://www.bookdepository.com/search?searchTerm=martian&search=Find+book')
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.select('div.book-item')

    for book in books:
        info = book.select('.item-info')[0]
        title = info.select('h3.title a')[0].text.strip()
        price = ' '.join(info.select('p.price')[0].text.encode('ascii', 'ignore').split()[:2])
        print title, price


if __name__ == '__main__':
    main()
