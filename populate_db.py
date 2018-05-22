#! /usr/bin/env python
#-*- coding: utf-8 -*-
"""
Script performered to populate the database before the program can
be used to searched among the OpenFoodFacts Database.
"""

from api_manager import ApiManager
from constants import MIN_PRODUCTS_PER_CATEGORY, DATABASE, HOST, USER, PASSWORD
from mysql.connector import errorcode

import mysql.connector


def create_db(cursor, cnx):
    """
    Create the database if it does not exist
    """
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DATABASE)
        )
    except mysql.connector.Error as err:
        print("Oups, failed in creating {} with error: {}".format(DATABASE, err))

    try:
        cnx.database = DATABASE
        print("Database is ready.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Issue with the DATABASE")
        else:
            print(err)

def populate_tables(cursor):
    """
    SQL Instruction to generate the tables
    """

    tables = {}
    alterings = {}

    tables['category'] = (
        " CREATE TABLE IF NOT EXISTS `category` ("
        " `id` INT(10) UNSIGNED AUTO_INCREMENT,"
        " `name` TEXT NOT NULL,"
        " `url` TEXT,"
        " `tag` VARCHAR(100),"
        " PRIMARY KEY (`id`)"
        " )ENGINE=InnoDB")

    tables['product'] = (
        " CREATE TABLE IF NOT EXISTS `product` ("
        " `id` INT(10) UNSIGNED AUTO_INCREMENT,"
        " `name` TEXT NOT NULL,"
        " `description` TEXT,"
        " `stores` VARCHAR(100),"
        " `link` TEXT,"
        " `grade` VARCHAR(20),"
        " `fat` VARCHAR(10),"
        " `sugars` VARCHAR(10),"
        " `salt` VARCHAR(10),"
        " `saturated_fat` VARCHAR(10),"
        " PRIMARY KEY (`id`)"
        " )ENGINE=InnoDB")

    alterings['product'] = (
        " ALTER TABLE `product` "
        " ADD INDEX `name_index` (`name`)"
    )

    tables['substitute'] = (
        " CREATE TABLE IF NOT EXISTS `substitute` ("
        " `id` INT(10) UNSIGNED AUTO_INCREMENT,"
        " `name` VARCHAR(45) NOT NULL,"
        " `description` VARCHAR(45),"
        " PRIMARY KEY (`id`)"
        " )ENGINE=InnoDB")

    tables['categories_products'] = (
        " CREATE TABLE IF NOT EXISTS `categories_products` ("
        " `category_id` INT(10) UNSIGNED,"
        " `product_id` INT(10) UNSIGNED"
        " )ENGINE=InnoDB")

    alterings['categories_products'] = (
        " ALTER TABLE `categories_products` "
        " ADD CONSTRAINT `fk_category` FOREIGN KEY (`category_id`)"
        "   REFERENCES `category` (`id`) ON DELETE CASCADE,"
        " ADD CONSTRAINT `fk_product` FOREIGN KEY (`product_id`)"
        "   REFERENCES `product` (`id`) ON DELETE CASCADE"
    )

    tables['substitutes_products'] = (
        " CREATE TABLE IF NOT EXISTS `substitutes_products` ("
        " `substitute_id` INT(10) UNSIGNED,"
        " `product_name` TEXT NOT NULL"
        " )ENGINE=InnoDB")

    alterings['substitutes_products'] = (
        " ALTER TABLE `substitutes_products` "
        " ADD CONSTRAINT `fk_substitute` FOREIGN KEY (`substitute_id`)"
        "   REFERENCES `substitute` (`id`) ON DELETE CASCADE,"
        " ADD CONSTRAINT `fk_product_name` FOREIGN KEY (`product_name`)"
        "   REFERENCES `product` (`name`) ON DELETE CASCADE"
    )

    for name, ddl in tables.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("Table added.")

    for name, ddl in alterings.items():
        try:
            print("Altering table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("Table altered.")

def main():
    """
    Main part
    """

    ### Create Databases and tables ###

    cnx = mysql.connector.connect(user=USER, password=PASSWORD,host=HOST)
    cursor = cnx.cursor()

    create_db(cursor, cnx)
    populate_tables(cursor)

    ### Fetch the data from the API ###

    api_manager = ApiManager()
    categories = api_manager.categories()

    for category in categories:
        if category['products'] > MIN_PRODUCTS_PER_CATEGORY:

            ### Category ###
            cursor.execute("INSERT INTO `category` (name, url, tag) VALUES (%s, %s, %s)"
            ,(category['name'], category['url'], category['id']))
            category_index = cursor.lastrowid
            print("Category added ")
            cnx.commit()

            ### Products ###
            products = api_manager.category_products(category['id'])
            for product in products:
                try:
                    print(product['product_name'])
                    cursor.execute("INSERT INTO `product` (name, description, stores, grade, link, fat, sugars, salt, saturated_fat) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (product['product_name'], product['generic_name_fr'], product['stores'], \
                    product['nutrition_grades'], product['link'], product['nutrient_levels']['fat'], product['nutrient_levels']['sugars'], \
                    product['nutrient_levels']['salt'], product['nutrient_levels']['saturated-fat']))
                    product_index = cursor.lastrowid
                except KeyError:
                    pass
                print("Product added ")
                cnx.commit()

                ### Mutual table ###
                cursor.execute("INSERT INTO `categories_products` (category_id, product_id) \
                VALUES (%s, %s)", (category_index, product_index))

if __name__ == '__main__':
    main()
