"""A module to get countries names, cities names, ids, etc.

   It extracts cities informations (from a kiwi raw data).

   Example:
   {
       'Germany' :
          [{
             'city' = 'Stuttgart',
             'country_id' = 'DE',
             'country' = 'Germany'
          }],
        '...' :
          ...
   }
"""

import json
import os
import re
from modules.info_format import airport_format
from modules.info_format import city_format

__all__ = ["Cities"]

class Cities:
    def get_cities(self, response_dict):
        cities_by_countries = {}
        for item in response_dict['body']:
            city_info = city_format()
            city_country_temp = re.findall("(.*?) \((.*?)\)", item['value'])
            city_country_temp = list(city_country_temp[0])
            country_id = item['parentId']
            country = city_country_temp[1]
            city = city_country_temp[0]
            city_info['country'] = country
            city_info['city'] = city
            city_info['country_id'] = country_id
            if city_info['country'] in cities_by_countries:
                cities_by_countries[city_info['country']].append(city_info)
            else:
                cities_by_countries[city_info['country']] = [city_info]

        return cities_by_countries
