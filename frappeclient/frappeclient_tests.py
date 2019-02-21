# -*- coding: utf-8 -*-
from frappeclient import FrappeClient
import urlparse
import httpretty
import unittest


class FrappeClientTest(unittest.TestCase):

    @httpretty.activate
    def setUp(self):
        httpretty.register_uri(httpretty.POST,
                               'https://example.com',
                               body='{"message":"Logged In"}',
                               content_type='application/json'
                               )
        self.frappe = FrappeClient('https://example.com',
                                   username='user@example.com',
                                   password='password')

    @httpretty.activate
    def test_get_doc_with_no_doc_name(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://example.com/api/resource/SomeDoc/',
            body='{"data": { "f1": "v1","f2": "v2"}}',
            content_type='application/json'
        )
        res = self.frappe.get_doc(
            'SomeDoc',
            filters=[['Note', 'title', 'LIKE', 'S%']],
            fields=['name', 'foo'])

        self.assertEquals(res, {'f1': 'v1', 'f2': 'v2'})

        request = httpretty.last_request()
        url = urlparse.urlparse(request.path)
        query_dict = urlparse.parse_qs(url.query)
        self.assertEquals(query_dict['fields'],
                          [u'["name", "foo"]'])
        self.assertEquals(query_dict['filters'],
                          [u'[["Note", "title", "LIKE", "S%"]]'])

    def test_token_auth(self):
        self.frappe = FrappeClient('https://example.com')
        self.frappe.authenticate('test_key', 'test_secret')
        auth_header = self.frappe.session.headers.get('Authorization')
        self.assertEquals(auth_header, 'Basic dGVzdF9rZXk6dGVzdF9zZWNyZXQ=')


if __name__ == '__main__':
    unittest.main()
