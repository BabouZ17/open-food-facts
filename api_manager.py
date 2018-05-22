#! /usr/bin/env python
#-*- coding: utf-8 -*-
# Model managing the queries to the open food facts api
"""
Model managing the queries made to the API
"""

import requests
import json

from constants import OPEN_FOOD_FACTS_API_URL, OPEN_FOOD_FACTS_SEARCH_URL

class ApiManager():
    """

    """
    def __init__(self, url=OPEN_FOOD_FACTS_API_URL):
        """
        Main constructor
        """
        self.url = url

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
        except json.decoder.JSONDecodeError:
            print('Issue with the given parameter')

    def categories(self):
        """
        Fetch all the categories
        """
        result = ''
        try:
            result = requests.get(url=OPEN_FOOD_FACTS_API_URL + 'categories' + \
            '.json').json()
        except (json.decoder.JSONDecodeError, TypeError):
            print('Issue with the result of the request')
        try:
            result = result['tags']
        except KeyError:
            print('Issue with the key!')
        return result

    def category_products(self, filter=None):
        """
        Fetch the products belonging to a category
        """
        result = ''
        try:
            result = requests.get(url=OPEN_FOOD_FACTS_API_URL + 'categorie/' + \
            str(filter) + '.json').json()
        except json.decoder.JSONDecodeError:
            print('Issue with the result of the request')
        try:
            result = result['products']
        except KeyError:
            print('Issue with the key!')
        return result

    def search(self, filter, max_results=100, page=1):
        """
        Run a search query
        """
        result = ''
        try:
            result = requests.get(url=OPEN_FOOD_FACTS_SEARCH_URL + str(filter) + \
            '&search_simple=1&action=process&json=1&page_size=' + str(max_results) + \
            '&page=' + str(page)).json()
        except json.decoder.JSONDecodeError:
            print('Issue with the result of the request')
        try:
            result = result['products']
        except KeyError:
            print('Issue with the key!')
        return result
