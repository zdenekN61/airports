"""Format of object to store informations"""

import os
import re

__all__ = ["city_format", "airport_format"]

def city_format():
    """City format

    Example:
    {
        "country": "...",
        "country_id": "...",
        "city": "...",
        "airports": []
    }
    """
    city = {"country": "", "country_id": "", "city": "", "airports": []}
    return city

def airport_format():
    """Airport format

    Example:
    {
        "airport": "...",
        "ICAO": "...",
        "IATA": "...",
        "web": "...",
        "country": "...",
        "city": ""
    }
    """
    airport = {"airport": "", "ICAO": "", "IATA": "", "web": "",
               "country": "", "city": ""}
    return airport
