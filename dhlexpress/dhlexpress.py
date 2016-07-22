# -*- coding: utf-8 -*-

import requests
import json

from helpers import (
    quote_req, quote_resp,
    shipment_req, shipment_resp
)


class DHLExpressClient(object):
    TEST_URL = "https://xmlpitest-ea.dhl.com/XMLShippingServlet"
    PROD_URL = "https://xmlpi-ea.dhl.com/XMLShippingServlet"

    def __init__(self, siteId, password, accountNo, test_mode=False):
        self.siteId = siteId
        self.password = password
        self.accountNo = accountNo
        self.test_mode = test_mode
        self.session = requests.Session()
        self.session.headers.update({'content-type': 'text/xml'})

    @property
    def quote(self):
        return Quote(connection=self)

    @property
    def shipment(self):
        return Shipment(connection=self)


class Resource(object):
    """
    A base class for all Resources to extend
    """

    def __init__(self, connection):
        self.connection = connection


class Quote(Resource):
    """
    A Quote Resource class
    """

    def quote_service(self):
        # TODO Error handling
        url = self.connection.TEST_URL if self.connection.test_mode else \
                self.connection.PROD_URL  # noqa
        payload = quote_req(
            self.connection.siteId,
            self.connection.password
        )
        response = self.connection.session.post(
            url,
            data=payload
        )
        return json.dumps(
            quote_resp(response.content),
            indent=4,
            sort_keys=True
        )


class Shipment(Resource):
    """
    A Shipment Resource class
    """

    def shipment_service(self):
        # TODO Error handling
        url = self.connection.TEST_URL if self.connection.test_mode else \
                self.connection.PROD_URL  # noqa
        payload = shipment_req(
            self.connection.siteId,
            self.connection.password,
            self.connection.accountNo
        )
        response = self.connection.session.post(
            url,
            data=payload
        )
        return json.dumps(
            shipment_resp(response.content),
            indent=4,
            sort_keys=True
        )


if __name__ == '__main__':
    client = DHLExpressClient('siteId', 'password', 'accountNo')
    client.test_mode = True
    # TODO Take request from user
    # response = client.quote.quote_service()
    response = client.shipment.shipment_service()
    print response
