import requests
import json
from StringIO import StringIO

class AuthError(Exception):
	pass

class FrappeException(Exception):
	pass

class NotUploadableException(FrappeException):
	def __init__(self, doctype):
		self.message = "The doctype `{1}` is not uploadable, so you can't download the template".format(doctype)

CAN_DOWNLOAD = []

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
		global CAN_DOWNLOAD
		r = self.session.post(self.url, data={
			'cmd': 'login',
			'usr': username,
			'pwd': password
		})

		if r.json().get('message') == "Logged In":
			CAN_DOWNLOAD = []
			return r.json()
		else:
			raise AuthError

	def logout(self):
		global CAN_DOWNLOAD
		self.session.get(self.url, params={
			'cmd': 'logout',
		})
		CAN_DOWNLOAD = []

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
			"cmd": "frappe.client.delete",
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

	def get_doc(self, doctype, name="", filters=None, fields=None):
		params = {}
		if filters:
			params["filters"] = json.dumps(filters)
                if fields:
                        params["fields"] = json.dumps(fields)

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

	def get_pdf(self, doctype, name, print_format="Standard", letterhead=True):
		params = {
			'doctype': doctype,
			'name': name,
			'format': print_format,
			'no_letterhead': int(not bool(letterhead))
		}
		response = self.session.get(
			self.url + "/api/method/frappe.templates.pages.print.download_pdf",
			params=params, stream=True)

		return self.post_process_file_stream(response)

	def get_html(self, doctype, name, print_format="Standard", letterhead=True):
		params = {
			'doctype': doctype,
			'name': name,
			'format': print_format,
			'no_letterhead': int(not bool(letterhead))
		}
		response = self.session.get(
			self.url + '/print', params=params, stream=True
		)
		return self.post_process_file_stream(response)

	def __load_downloadable_templates(self):
		global CAN_DOWNLOAD
		CAN_DOWNLOAD = self.get_api('frappe.core.page.data_import_tool.data_import_tool.get_doctypes')

	def get_upload_template(self, doctype, with_data=False):
		global CAN_DOWNLOAD
		if not CAN_DOWNLOAD:
			self.__load_downloadable_templates()

		if doctype not in CAN_DOWNLOAD:
			raise NotUploadableException(doctype)

		params = {
			'doctype': doctype,
			'parent_doctype': doctype,
			'with_data': 'Yes' if with_data else 'No',
			'all_doctypes': 'Yes'
		}

		request = self.session.get(self.url +
			'/api/method/frappe.core.page.data_import_tool.exporter.get_template',
			params=params)
		return self.post_process_file_stream(request)

	def get_api(self, method, params={}):
		res = self.session.get(self.url + "/api/method/" + method + "/",
			params=params)
		return self.post_process(res)

	def post_api(self, method, params={}):
		res = self.session.post(self.url + "/api/method/" + method + "/",
			params=params)
		return self.post_process(res)

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

	def post_process_file_stream(self, response):
		if response.ok:
			output = StringIO()
			for block in response.iter_content(1024):
				output.write(block)
			return output

		else:
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
