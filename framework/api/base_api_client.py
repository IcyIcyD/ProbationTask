import allure
import requests

from framework.constants.common_constants import (HTTP_POST, HTTP_GET, TEMPLATE_REQUEST_RESPONSE,
                                                  TEMPLATE_PREPARED_REQUEST)


class BaseAPIClient:
    """Base class for API integration."""

    def __init__(self, url):
        """Create BaseAPIClient.

        @:param url (str): Base API url.
        """
        self.base_url = url
        self.session = requests.Session()

    @staticmethod
    def __form_attachment_prepared(req):
        """Creates attachment template with prepared API request info.

        @:param req (requests.PreparedRequest): Prepared API request.
        @:returns attach (str): Formatted string, attachment template.
        """
        attach = TEMPLATE_PREPARED_REQUEST.format(
            url=req.url,
            method=req.method,
            headers='\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            body=req.body
        )
        return attach

    @staticmethod
    def __form_attachment_response(resp):
        """Creates attachment template with API response info.

        @:param resp (requests.Response): API response.
        @:returns attach (str): Formatted string, attachment template.
        """
        attach = TEMPLATE_REQUEST_RESPONSE.format(
            url=resp.url,
            status_code=resp.status_code,
            headers='\r\n'.join('{}: {}'.format(k, v) for k, v in resp.headers.items()),
            body=resp.content
        )
        return attach

    def __send_request(self, prepared):
        """Sends prepared API request, attaches it to allure report.

        @:param req (requests.PreparedRequest): Prepared API request.
        @:returns response (requests.Response): API response.
        """
        attach_sent = self.__form_attachment_prepared(req=prepared)
        allure.attach(attach_sent, name="Sent")
        response = self.session.send(prepared)
        attach_resp = self.__form_attachment_response(resp=response)
        allure.attach(attach_resp, name="Received")
        response.raise_for_status()
        return response

    def _request_get(self, url):
        """Simple HTTP GET request.

        @:param url (str): Request url.
        @:returns response (requests.Response): API response.
        """
        url = self.base_url + url
        prepared = self.session.prepare_request(requests.Request(HTTP_GET, url))
        response = self.__send_request(prepared=prepared)
        return response

    def _request_post(self, url, headers=None, data=None, json=None):
        """Simple HTTP POST request.

        @:param url (str): Request url.
        @:param headers (dict): Custom request headers.
        @:param data (dict): `Form-data` parameters for request.
        @:param json (dict): JSON-type parameters for request.
        @:returns response (requests.Response): API response.
        """
        url = self.base_url + url
        prepared = self.session.prepare_request(requests.Request(HTTP_POST, url, headers=headers,
                                                                 data=data, json=json))
        response = self.__send_request(prepared=prepared)
        return response
