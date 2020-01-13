# -*- coding: utf-8 -*-
import unittest
from frappeclient import FrappeClient

test_config = dict(
	url = 'http://frappe.local:8000',
	username = 'Administrator',
	password = 'admin'
)

TXT = 'test content'

class TestFrappeClient(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.conn = FrappeClient(**test_config)

	def test_insert(self):
		doc = self.conn.insert(dict(doctype='Note', title='test note 1', content=TXT))
		self.assertEqual(self.conn.get_value('Note', 'content',
			dict(title='test note 1'))['content'], TXT)

		self.conn.delete(doctype='Note', name=doc.get('name'))

	def test_list(self):
		doc1 = self.conn.insert(dict(doctype='Note', title='apple', content=TXT))
		doc2 = self.conn.insert(dict(doctype='Note', title='banana', content=TXT))
		doc3 = self.conn.insert(dict(doctype='Note', title='carrot', content=TXT))

		notes = self.conn.get_list('Note', fields=['content', 'name'], filters=dict(title=['like', 'ap%']))
		self.assertEqual(len(notes), 1)
		self.assertEqual(notes[0].get('name'), doc1.get('name'))

		self.conn.delete(doctype='Note', name=doc1.get('name'))
		self.conn.delete(doctype='Note', name=doc2.get('name'))
		self.conn.delete(doctype='Note', name=doc3.get('name'))

	def test_token_auth(self):
		self.conn.authenticate('test_key', 'test_secret')
		auth_header = self.conn.session.headers.get('Authorization')
		self.assertEquals(auth_header, 'Basic dGVzdF9rZXk6dGVzdF9zZWNyZXQ=')


if __name__=='__main__':
	unittest.main()
