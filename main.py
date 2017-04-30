"""A main module - Lord of the modules

   This is the module handling all main stuff.
   What it does:
   - gets a raw data from kiwi.com(cities info).
   - from the raw data it gets cities sorted by the country.
   - gets airports for all coutries, airports to the proper city.
   - stores info to a directories/files tree as jsons.

   To start it just write 'python main.py' to command line and hit an enter.
"""

import logging
import os
import re
import sys
from modules.airports import Airports
from modules.cities import Cities
from modules.my_json import to_dictionary
from modules.my_json import to_JSON
from modules.store_info import StoreInfo
from modules.url_reader import URLReader

__all__ = ["Main"]

class Main:
    def __init__(self):
        self.kiwi_info = {}
        self.cities_by_countries = {}

    # A main function to call.
    def get_airports_data(self, url):
        self.URL_reader = URLReader()
        self._get_kiwi_info(url)
        self._get_cities_by_countries()
        self._get_airports_by_city()

    # Download data from kiwi.com page.
    def _get_kiwi_info(self, url):
        self.kiwi_info = self.URL_reader.get_url_response(url)
        if self.kiwi_info['status'] != 200:
            logging.error("Get informations from kiwi.com failed!!!")
            self._exit()
        else:
            self.kiwi_info['body'] = to_JSON(self.kiwi_info['body'])
            logging.info("Get informations from kiwi.com succeeded.")

    # Sorts all cities(airports supported by kiwi.com) by countries.
    def _get_cities_by_countries(self):
        self.cities = Cities()
        self.cities_by_countries = self.cities.get_cities(self.kiwi_info)

    def _get_airports_by_city(self):
        """Walking through cities and airports and trying to assign a proper 
           airport to a proper city.
        """
        self.airports = Airports()
        self.store_info = StoreInfo()
        for country in self.cities_by_countries:
            self.store_info.country_tree(country)
            airports = self.airports.get_airports_by_country(country)
            for city_i in range(0, len(self.cities_by_countries[country])):
                city_name = self.cities_by_countries[country][city_i]['city']
                city_airports = self.airports.get_airports_by_cities(airports,
                                                                     city_name)
                self.store_info.store_info(city_airports, city_name, country)

    # End it.
    def _exit(self):
        logging.error("Can not continue, stopping.")
        sys.exit()

if __name__=='__main__':
    url = 'https://api.skypicker.com/places?v=2&active=0&type=2'
    data = Main()
    data.get_airports_data(url)
