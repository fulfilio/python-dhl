import os
import pytest
import responses
import json
from dhlexpress import DHLExpressClient


@pytest.fixture
def fp():
    def wrapper(rel_path):
        "return the full path of given rel_path"
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                rel_path
            )
        )
    return wrapper


@pytest.fixture
def dhlexpress():
    return DHLExpressClient(
        'siteId', 'password',
        'accountNo', test_mode=True
    )


@pytest.yield_fixture
def resp(fp):
    rsps = responses.RequestsMock(False)
    rsps.start()

    "Shipment"
    def request_callback(request):
        payload = open(fp('responses/shipment_req.xml'), 'r').read()  # noqa
        resp_body = open(fp('responses/shipment_resp.json'), 'r').read()
        return (200, json.dumps(resp_body))

    rsps.add_callback(
        responses.POST, 'https://xmlpitest-ea.dhl.com/XMLShippingServlet',
        callback=request_callback,
        content_type='text/xml',
    )

    yield rsps

    rsps.stop()
    rsps.reset()
