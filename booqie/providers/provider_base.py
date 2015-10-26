import requests

from bs4 import BeautifulSoup
from cached_property import cached_property


class ProviderBase(object):

    def __init__(self, url_template, search_term):
        self.url_template = url_template
        self.search_term = search_term
        response = requests.get(url_template.format(search_term=search_term))
        self.soup = BeautifulSoup(response.text, 'lxml')

    @cached_property
    def books(self):
        raise NotImplementedError
