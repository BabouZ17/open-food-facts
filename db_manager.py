#! /usr/bin/env python
#-*- coding: utf-8 -*-
# Database Manager object which deals with the queries
"""
Database Manager class used to deal with the queries performered to the db
"""

import mysql.connector

from constants import USER, PASSWORD, HOST, DATABASE

class DbManager():
    """
    Mysql connector wrapper
    """
    def __init__(self, host=HOST, user=USER, password=PASSWORD, database=DATABASE):
        """
        Main constructor
        """
        self.client = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        self.cursor = self.client.cursor()
        self.query_result = ''

    def __repr__(self):
        """
        Magic method to represent the object
        """
        return '{}'.format(self.client)

    def category_products(self, id=0):
        """
        Return a join query result regarding the category id provided
        """
        assert type(id) is int
        query = ("SELECT id, name, description FROM `product` WHERE id IN "
        " (SELECT product_id FROM `categories_products` "
        " WHERE category_id = (SELECT id FROM `category` WHERE id = {}))".format(id))
        self.cursor.execute(query)

    def close_cursor(self):
        """
        Close the cursor
        """
        self.cursor.close()

    def close_client(self):
        """
        Close the client connexion
        """
        self.client.close()
