"""Saves informations about cities, airports to directories/files/jsons tree"""

import logging
import os
import re
import shutil
from modules.my_json import to_dictionary
from modules.my_json import to_JSON

__all__ = ["StoreInfo"]

ROOT_DIR = r"./countries"

class StoreInfo:
    def __init__(self):
        self._root_directory()

    # Saves informations to a proper 'tree'.
    def store_info(self, airports, city, country):
        country_name = self._sub_in_name(" ", "_", country)
        city_name = self._sub_in_name(" ", "_", city)
        city_path = self._city_directory(country_name, city_name)
        for airport in airports:
            self._airport_file(city_path, airport)

    # Creates a 'country' directory.
    def country_tree(self, country):
        country_name = self._sub_in_name(" ", "_", country)
        country_path = r"%s/%s" % (ROOT_DIR, country_name)
        if not os.path.exists(country_path):
            self._create_dir(country_path)

    # Creates a 'root' directory.
    def _root_directory(self):
        if os.path.exists(ROOT_DIR):
            try:
                shutil.rmtree(ROOT_DIR)
            except:
                logging.error("""Something is holding path %s open(handlers,
                                 you), please step off.""" % ROOT_DIR)
        try:
            self._create_dir(ROOT_DIR)
        except:
            logging.error("""Can not continue to save informations, 
                             can not create root directory, stopping""")
            self._end()

    # Creates a 'airport' file and fills it.
    def _airport_file(self, city, airport):
        airport_name = self._sub_in_name("[\ \/]+", "_", airport['airport'])
        airport_path = r"%s/%s.json"% (city, airport_name)
        airport_json = to_dictionary(airport)
        if not os.path.exists(airport_path) and os.path.exists(city):
            f_in = open(airport_path, "w")
            f_in.write(airport_json)
            f_in.close()

    # Creates a 'city' directory if does not exists.
    def _city_directory(self, country, city):
        city_path = r"%s/%s/%s" % (ROOT_DIR, country, city)
        if not os.path.exists(city_path):
            self._create_dir(city_path)
        return city_path

    # Replaces 'sub' in 'text' by 'sub_by'.
    def _sub_in_name(self, sub, sub_by, text):
        substited = re.sub(sub, sub_by, text)
        return substited

    # Creates a directory.
    def _create_dir(self, path):
        try:
            os.mkdir(path)
        except:
            logging.error("Directory %s can not be create." % path)

    # Ends it.
    def _exit(self):
        logging.error("Can not continue, stoping.")
        sys.exit()

