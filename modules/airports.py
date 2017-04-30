"""A module to gets informations about airports
   from http://www.airlines-inform.com

   It is neccesary to do few 'steps' before you get what you wanted.
   - gets records for country(links to airports, feedbacks, etc.).
   - sorted it, gets only airports links.
   - gets informations you wanted(name, IATA, ICAO, web).

   WARNING: It is not entirely "ethical" and "legal"(licence agreement, etc.).
   So consider this as an example, NO OFFICIAL PUBLIC USE.

   TODO: Find different sources for extracting airports web pages.
         More sources -> more reliable data.

   Possible sources: wikipedia, google.com, kiwi databases, IATA.org, etc.
"""

import json
import logging
import os
import re
from modules.airport_info import AirportInfo
from modules.info_format import airport_format
from modules.info_format import city_format
from modules.url_reader import URLReader

__all__ = ["Airports"]

# Global variables(help to put together regex, encondig, etc.)
AICOM_AIRPORTS = "https://www.airlines-inform.com/search/index.php?"
ENCODING_AICOM = 'windows-1251'
REGEX_AIRPORTS_LINKS = r"https://airport.airlines-inform.com/[\w\s\-]+\.html"
LAST_PAGE = r"PAGEN_1=(\w+)\">Last"

class Airports():
    def __init__(self):
        self.reader = URLReader()

    # A main function, main crossroad. Get country, get airport, all together.
    def get_airports_by_country(self, country):
        airports_links = []
        pages = 1
        country_airports = [] 
        country_link = self._search_link_to_country_info_AICOM(country)
        first_page = self.reader.get_url_response(url_link=country_link,
                                                  encoding=ENCODING_AICOM)
        if first_page['status'] == 200 and first_page['body']:
            pages = self._get_pages_count_AICOM(first_page['body'])
        airports_links = self._find_links_airports_AICOM(first_page['body'])
        if pages > 1:
            for page in range(2, pages+1):
                country_link = self._search_link_to_country_info_AICOM(country,
                                                                       page)
                airports_links += self._get_links_to_airports_info(country_link)
        airport_info = AirportInfo()
        for airport_item in airports_links:
            airport = airport_info.get_airport_info(airport_item,
                                                    country)
            country_airports.append(airport)
        return country_airports

    def get_airports_by_cities(self, airports, city):
        """Sorts airports by a city(compare airport name against city name). 
           Based on an assumption that airport name contains name of the city 
           where is located. 
        """
        city_airports = []
        for airport_item in range(0, len(airports)):
            if city.lower() in airports[airport_item]['airport'].lower():
                airports[airport_item]['city'] = city 
                city_airports.append(airports[airport_item])
        return city_airports

    # A Link to country, find links to airports.
    def _get_links_to_airports_info(self, country_link):
        country_airports_links = []
        try:
            info = self.reader.get_url_response(url_link=country_link,
                                                encoding=ENCODING_AICOM)
            if info['status'] == 200 and info['body']:
                country_airports_links = (
                            self._find_links_airports_AICOM(info['body']))
        except:
            logging.info("Link %s can not be proceed." % country_link)
        return country_airports_links

    # Puts together a url link to country "search" for records.
    def _search_link_to_country_info_AICOM(self, country, page=1):
        prepared_country_name = re.sub(" ", "+", country)
        link = "%sq=%s&s=Search&PAGEN_1=%s" % (AICOM_AIRPORTS,
                                               prepared_country_name,
                                               page)
        return link

    # Finding links on the page(links to airports closer informations).
    def _find_links_airports_AICOM(self, info):
        links = re.findall(REGEX_AIRPORTS_LINKS, info)
        return links

    # How many pages It will be looking on.
    def _get_pages_count_AICOM(self, raw_text):
        pages_count = 1
        pages = re.findall(r"PAGEN_1=(\d+)\">Last", raw_text)
        if pages:
            pages_count = int(pages[0])
        return pages_count
