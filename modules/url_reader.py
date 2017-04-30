"""A module providing support for url/api request processing.

   Return a dictionary of three keys. A 'status' with a classic html 
   response code(200, 400, etc.). An 'error' containing reason what happend if 
   something happend(in our case a exception text). And last one a 'body'
   with an original response body.
"""

import os
import re
import urllib.error as error
import urllib.request as url

__all__ = ["UrlReader"]

ENCODING = 'UTF-8'

class URLReader:
    # Starts it.
    def get_url_response(self, url_link, data=None, headers={},
                         encoding=ENCODING, method='GET'):
        self.encoding = encoding
        response = self._send_request(url_link, data, headers, method)
        return response

    # Sends the request, read the answer, transform it to "readable object".
    def _send_request(self, url_link, data, headers, method):
        request = self._create_request(url_link, data, headers, method)
        response = {'status': 400, # Default - bad request
                      'error': None,
                      'body': None}
        try:
            opener = url.urlopen(request)
            response['status'] = opener.status
            response['error'] = opener.reason
            response['body'] = opener.read()
            response['body'] = response['body'].decode(self.encoding)
        except error.URLError as e:
            response['error'] = e.reason
        except error.HTTPError as e:
            response['error'] = e.reason
            response['status'] = e.code
        return response

    # Puts the request together, add headers.
    def _create_request(self, url_link, data_in, headers, method):
        _method = self._method(method)
        request = url.Request(url=url_link, data=data_in, method=_method)
        for header_item in headers:
            request.add_header(header_item, headers[header_item])
        return request

    # Supported method(easier to extend).
    def _method(self, method):
        method_name = 'GET'
        if (method.lower() == 'get'):
            method_name = 'GET'
        elif (method.lower() == 'post'):
            method_name = 'POST'
        elif (method.lower() == 'put'):
            method_name = 'PUT'
        return method_name
