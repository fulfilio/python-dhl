# -*- coding: utf-8 -*-

import requests

class DHLExpressClient(object):

    def __init__(self, siteId, password, accountNo):
        self.base_url = "https://xmlpitest-ea.dhl.com/XMLShippingServlet"
        self.siteId = siteId
        self.password = password
        self.accountNo = accountNo
        self.session = requests.Session()
        self.session.headers.update({'content-type': 'text/xml'})

    def quote_service():
        # TODO Build xml using elementtree
        pass

if __name__ == '__main__':
    client = DHLExpressClient('site_id', 'password', 'acc_no')
    client.quote_service()
