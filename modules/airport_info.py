"""Gets airport informations, stores it.

   As a parametr it accepts link to more detailed page and as a second
   parametr accepts name country(to specified to which pool of 
   airports it belongs),

   Info about airport(a dictionary):
   - name
   - ICAO
   - IATA
   - web(if exists)
   - country   
"""

import json
import os
import re
from modules.info_format import airport_format
from modules.info_format import city_format
from modules.url_reader import URLReader

__all__ = ["AirportInfo"]

ENCODING_AICOM = 'windows-1251'

class AirportInfo():
    def __init__(self):
        # An object handling url processing
        self.reader = URLReader()

    def get_airport_info(self, airport_link, country):
        airport_raw = self.reader.get_url_response(airport_link,
                                            encoding=ENCODING_AICOM)

        # An object to store airport informations(info_format.py)
        airport_info = airport_format()
        if airport_raw['status'] == 200:
            airport_info['airport'] = self._airport_name(airport_raw['body'])
            airport_info['ICAO'] = self._airport_ICAO(airport_raw['body'])
            airport_info['IATA'] = self._airport_IATA(airport_raw['body'])
            airport_info['web'] = self._airport_web(airport_raw['body'])
            airport_info['country'] = country
        return airport_info

    # Extracts an airport name from page title.
    def _airport_name(self, raw_text):
        name = 'N/A'
        founded = re.findall(r'<title>(.*?)</title>', raw_text)
        if founded:
            name = founded[0]
        return name

    # A ICAO shortcut.
    def _airport_ICAO(self, raw_text):
        icao = 'N/A'
        founded = re.findall(r'<b>ICAO code:</b>&nbsp;(.*?)<br>', raw_text)
        if founded:
            icao = founded[0]
        return icao

    # A IATA shortcut.
    def _airport_IATA(self, raw_text):
        iata = 'N/A'
        founded = re.findall(r'<b>IATA code:</b>&nbsp;(.*?)<br>', raw_text)
        if founded:
            iata = founded[0]
        return iata

    # A link to airport webside, if exists on the page.
    def _airport_web(self, raw_text):
        web = 'N/A'
        rex = r'<b>Web-site:</b>&nbsp;<a \w+="\w+"  \w+="(.*?)">'
        founded = re.findall(rex, raw_text)
        if founded:
            web = founded[0]
        return web
