#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dhlexpress
----------------------------------

Tests for `dhlexpress` module.
"""

import pytest 	# noqa


def test_shipment_service(resp, dhlexpress):
    "test shipment service"
    shipment_resp = dhlexpress.shipment.shipment_service()
    assert shipment_resp['Rated'] == 'N'
