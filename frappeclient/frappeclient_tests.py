# -*- coding: utf-8 -*-
from frappeclient import FrappeClient
import urlparse
import httpretty
import unittest


class FrappeClientTest(unittest.TestCase):

    @httpretty.activate
    def setUp(self):
        httpretty.register_uri(httpretty.POST,
                               "http://example.com",
                               body='{"message":"Logged In"}',
                               content_type="application/json"
                               )
        self.frappe = FrappeClient("http://example.com",
                                   "user@example.com",
                                   "password")

    @httpretty.activate
    def test_get_doc_with_no_doc_name(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://example.com/api/resource/SomeDoc/",
            body='{"data": { "f1": "v1","f2": "v2"}}',
            content_type="application/json"
        )
        res = self.frappe.get_doc(
            "SomeDoc",
            filters=[["Note", "title", "LIKE", "S%"]],
            fields=["name", "foo"])

        self.assertEquals(res, {'f1': 'v1', 'f2': 'v2'})

        request = httpretty.last_request()
        url = urlparse.urlparse(request.path)
        query_dict = urlparse.parse_qs(url.query)
        self.assertEquals(query_dict['fields'],
                          [u'["name", "foo"]'])
        self.assertEquals(query_dict['filters'],
                          [u'[["Note", "title", "LIKE", "S%"]]'])
