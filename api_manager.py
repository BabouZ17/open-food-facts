#! /usr/bin/env python
#-*- coding: utf-8 -*-
# Model managing the queries to the open food facts api
"""
Model managing the queries made to the API
"""

import requests
import json

from constants import OPEN_FOOD_FACTS_API_URL

class ApiManager():
    """

    """
    def __init__(self, url=OPEN_FOOD_FACTS_API_URL):
        """
        Main constructor
        """
        self.url = url
        self.result = ''

    def __repr__(self):
        """
        Magic method the represent the model
        """
        return 'API Manager Instance'

    def product(self, id=0):
        """
        Look for a product regarding the given id
        """
        searched = 0
        try:
            searched = int(id)
            self.result = requests.get(url=OPEN_FOOD_FACTS_API_URL + 'api/v0/produit/' + \
            str(searched) + '.json').json()
        except (TypeError, json.decoder.JSONDecodeError):
            print('Issue with the given parameter')

    def categories(self):
        """
        Fetch all the categories
        """
        try:
            self.result = requests.get(url=OPEN_FOOD_FACTS_API_URL + 'categories' + \
            '.json').json()['tags']
        except json.decoder.JSONDecodeError:
            print('Issue while decoding')

    def category_products(self, filter=None):
        """
        Fetch the products belonging to a category
        """
        try:
            self.result = requests.get(url=OPEN_FOOD_FACTS_API_URL + 'categorie/' + \
            str(filter) + '.json').json()['products']
            #self.result = requests.get(url='https://world.openfoodfacts.org/cgi/search.pl?/search_terms=' + \
            #str(filter) + '&search_simple=1&action=process&json=1&page_size=1000')
        except json.decoder.JSONDecodeError:
            print('Issue with the filter parameter')
