#-*- coding: utf-8 -*-

from frappeclient import FrappeClient as Client
import os

files = {
	'CRM': [
		'Customer',
		'Address',
		'Contact',
		'Customer Group',
		'Territory',
		'Sales Person',
		'Terms and Conditions',
		'Target Detail',
		'Sales Partner',
		'Opportunity',
		'Lead'
	],
	'Manufacturing': [
		'Production Order',
		'Workstation',
		'Operation',
		'BOM'
	],
	'Selling': [
		'Quotation',
		'Sales Order',
		'Sales Taxes and Charges',
		'Installation Note',
		'Product Bundle',
	],
	'Stock': [
		'Purchase Receipt',
		'Bin',
		'Item',
		'Delivery Note',
		'Material Request',
		'Item Variant',
		'Item Attribute Value',
		'Serial No',
		'Warehouse',
		'Stock Entry',
		'Price List',
		'Item Price',
		'Batch',
		'Landed Cost Voucher'
	],
	'Setup': [
		'UOM',
		'Print Heading',
		'Currency Exchange',
		'Authorization Rule',
		'Authorization Control'
	],
	'Support': [
		'Issue',
		'Warranty Claim',
		'Maintenance Visit'
	],
	'HR': [
		'Employee',
		'Job Applicant',
		'Offer Letter',
		'Salary Structure',
		'Leave Application',
		'Expense Claim',
		'Expense Claim Type',
		'Appraisal',
		'Salary Slip',
		'Holiday',
		'Attendance',
		'Leave Type',
		'Job Opening',
		'Designation',
		'Department',
		'Earning Type',
		'Deduction Type',
		'Branch'
	]
}

def get_path(*args):
	path = os.path.abspath(os.path.join(
		os.path.dirname(__file__), 'ERPNext',
		*args
	))
	if not os.path.exists(path):
		os.makedirs(path)

	return path

def download():
	c = Client('http://localhost:8000', 'Administrator', 'admin')

	for k,v in files.items():
		for dt in v:
			for s, ext, method in (('Schemes', 'pdf', 'get_pdf'), ('Upload Templates', 'csv', 'get_upload_template')):
				base_path = get_path(k, s)
				with open(os.path.join(base_path, '.'.join([dt, ext])), 'wb') as handler:
					fn = getattr(c, method)
					if ext == 'pdf':
						content = fn('DocType', dt, 'Standard')
					else:
						try:
							content = fn(dt)
						except Exception, e:
							print 'Failed to Download: ' + dt
							continue

					handler.write(content.getvalue())
				print 'Downloaded: `{0}` of {1}'.format(ext, dt)

if __name__ == '__main__':
	download()
