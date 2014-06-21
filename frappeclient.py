import requests
import json

class AuthError(Exception):
	pass

class FrappeException(Exception):
	pass

class FrappeClient(object):
	def __init__(self, url, username, password):
		self.session = requests.Session()
		self.url = url
		self.login(username, password)

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		self.logout()

	def login(self, username, password):
		r = self.session.post(self.url, data={
			'cmd': 'login',
			'usr': username,
			'pwd': password
		})

		if r.json().get('message') == "Logged In":
			return r.json()
		else:
			raise AuthError

	def logout(self):
		self.session.get(self.url, params={
			'cmd': 'logout',
		})

	def insert(self, doc):
		res = self.session.post(self.url + "/api/resource/" + doc.get("doctype"),
			data={"data":json.dumps(doc)})
		return self.post_process(res)

	def update(self, doc):
		url = self.url + "/api/resource/" + doc.get("doctype") + "/" + doc.get("name")
		res = self.session.put(url, data={"data":json.dumps(doc)})
		return self.post_process(res)

	def bulk_update(self, docs):
		return self.post_request({
			"cmd": "frappe.client.bulk_update",
			"docs": json.dumps(docs)
		})

	def delete(self, doctype, name):
		return self.post_request({
			"cmd": "frappe.model.delete_doc",
			"doctype": doctype,
			"name": name
		})

	def submit(self, doclist):
		return self.post_request({
			"cmd": "frappe.client.submit",
			"doclist": json.dumps(doclist)
		})

	def get_value(self, doctype, fieldname=None, filters=None):
		return self.get_request({
			"cmd": "frappe.client.get_value",
			"doctype": doctype,
			"fieldname": fieldname or "name",
			"filters": json.dumps(filters)
		})

	def set_value(self, doctype, docname, fieldname, value):
		return self.post_request({
			"cmd": "frappe.client.set_value",
			"doctype": doctype,
			"name": docname,
			"fieldname": fieldname,
			"value": value
		})

	def cancel(self, doctype, name):
		return self.post_request({
			"cmd": "frappe.client.cancel",
			"doctype": doctype,
			"name": name
		})

	def get_doc(self, doctype, name=None, filters=None):
		params = {}
		if filters:
			params["filters"] = json.dumps(filters)

		res = self.session.get(self.url + "/api/resource/" + doctype + "/" + name,
			params=params)

		return self.post_process(res)

	def rename_doc(self, doctype, old_name, new_name):
		params = {
			"cmd": "frappe.client.rename_doc",
			"doctype": doctype,
			"old_name": old_name,
			"new_name": new_name
		}
		return self.post_request(params)

	def get_request(self, params):
		res = self.session.get(self.url, params=self.preprocess(params))
		res = self.post_process(res)
		return res

	def post_request(self, data):
		res = self.session.post(self.url, data=self.preprocess(data))
		res = self.post_process(res)
		return res

	def preprocess(self, params):
		"""convert dicts, lists to json"""
		for key, value in params.iteritems():
			if isinstance(value, (dict, list)):
				params[key] = json.dumps(value)

		return params

	def post_process(self, response):
		try:
			rjson = response.json()
		except ValueError:
			print response.text
			raise

		if rjson and ("exc" in rjson) and rjson["exc"]:
			raise FrappeException(rjson["exc"])
		if 'message' in rjson:
			return rjson['message']
		elif 'data' in rjson:
			return rjson['data']
		else:
			return None
