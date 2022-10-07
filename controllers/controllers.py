# -*- coding: utf-8 -*-
from odoo import http, _
from datetime import date, datetime, timedelta
import json
import requests
from requests.auth import HTTPBasicAuth

class RestApiCekData(http.Controller):
	@http.route('/restapi/cekdata', type="json", auth='public')
	def index(self, **kw):


		#api_key = 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e'

		#headers = {'Ocp-Apim-Subscription-Key': '{key}'.format(key=api_key)}

		url = "https://sandbox-api.stagingapps.net/merchants/session/login"


		data = {}
		#url = "https://sandbox-api.stagingapps.net/brand/210/detail?merchant_id=1"
		#url = "https://sandbox-api.stagingapps.net/brand/1?offset=0"
		#url = "https://sandbox-api.stagingapps.net/merchant/product?api_key=15cb7ebf9-3dcc-h28s-b056-2522c1eed03e&token=6eb5bc146d9b08d861a317f8b1885dedabf3ecdb"
		response = requests.get(url, data=json.dumps(data))		        
		res = response.json()

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + (res) + ');'
		console += '</script>'

		return console


# @http.route("/my/post/api/path", auth='none', type='http', method=['POST'], csrf=False, cors='*')
# 	def post_api_method(self, email, *kw):
# 		partners = request['res.partners'].sudo().search_read([('email','=',email)])

# 		headers = {'Content-Type': 'application/json'}
# 		body = { 'results': { 'code': 200, 'message': partners } }

# 		return Response(json.dumps(body), headers=headers)




class RestApiRequestToken(http.Controller):
	@http.route('/restapi/reqtoken', auth='public', method=['POST'])
	def index(self, **kw):
		headers = {
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		body = {
			'email': 'sandbox.wgs@gmail.com',
			'password': 'qwerty123',
			'device_model': 'WEB',
			'device_type': 'WEB',
			'device_id': '1'
		}

		#033963c2203be77f7b1918712d4318f03b1ce10a
		url = "https://sandbox-api.stagingapps.net/merchants/session/login"
		response = requests.post(url, headers=headers, data=json.dumps(body))		        
		
		if response.status_code == 200:
			res = response.json()
		else:
			res = 'Error ' + str(response.status_code)


		# Show data in console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		console += '</script>'

		return console
		#return res


class RestApiProducts(http.Controller):
	@http.route('/restapi/products', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		#url = 'https://sandbox-api.stagingapps.net/merchant/product?limit=0'
		url = 'https://sandbox-api.stagingapps.net/merchant/finance/transaction?limit=0&offset=0&store_id=0'
		response = requests.get(url, headers=headers, data=json.dumps(data))

		#total = ''


		# Check response
		if response.status_code == 200:
			# Response 200 / Success
			res = response.json()
			income = 0
			outcome = 0
			for data in res['data']:
				if data['status'] == "IN":
					income = income + int(data['amount'])
				elif data['status'] == "OUT":
					outcome = outcome + int(data['amount'])

			# Get data product in Odoo
			# getProducts = http.request.env['product.product'].search([])
			# #
			# for data in res['data']:
			# 	#print(data)
			# 	addNew = True
			# 	for product in getProducts:
			# 		#print(data['product_id'], ' / ', product['product_id'])
			# 		if data['product_id'] == product['product_id']:
			# 			addNew = False
			# 			break
			# 	#
			# 	if addNew == True:
			# 		# Create if data didnt exist
			# 		insertProduct = http.request.env['product.product'].sudo().create({
			# 			'name': data['product_name'],
			# 			'list_price': float(data['product_detail']['product_price']),
			# 			'merchant_id': int(data['merchant_id']),
			# 			'brand_id': int(data['brand']['id']),
			# 			'product_id': int(data['product_id']),	
			# 			'default_code': data['no_sku'],	
			# 		})
			# 		print('=================== Data berhasil ditambahkan : ', data['product_name'])
			# 	else:
			# 		# Update if data exist
			# 		updateProduct = http.request.env['product.product'].search([('product_id', '=', data['product_id'])], limit=1)
			# 		updateProduct.sudo().write({
			# 			'name': data['product_name'],
			# 			'list_price': float(data['product_detail']['product_price']),
			# 			'merchant_id': int(data['merchant_id']),
			# 			'brand_id': int(data['brand']['id']),
			# 			'product_id': int(data['product_id']),	
			# 			'default_code': data['no_sku'],
			# 		})
			# 		print('=================== Data Sudah di Update : ', data['product_name'])		
		else:
			# Response error
			res = 'Error ' + str(response.status_code)

		# Show data in console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		console += 'console.log("Income : ' + str(income) + '");'
		console += 'console.log("Outcome : ' + str(outcome) + '");'
		console += 'console.log("Total : ' + str(income - outcome) + '");'
		console += '</script>'

		return console


class RestApiBrands(http.Controller):
	@http.route('/restapi/shipper', auth='public')
	def index(self, **kw):
		headers = {
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			#'token': token,
			'content-type': 'application/json'
		}
		body = {}
		url = "https://sandbox-api.stagingapps.net/shipper/tracking-shipment-status?id=" + str(kw.get('id'))
		response = requests.get(url, headers=headers, data=json.dumps(body))		        
		if response.status_code == 200:
			data = response.json()
		else:
			data = False



		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(data) + ');'
		#console += 'console.log(' + json.dumps(filters) + ');'
		console += '</script>'

		return console



class RestApiBrands(http.Controller):
	@http.route('/restapi/brands', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		#url = 'https://sandbox-api.stagingapps.net/merchant/brand/list?offset=0&limit=0'
		#url = 'https://sandbox-api.stagingapps.net/merchant/orders/list?limit=0&offset=0&status_order=NEW_ORDER'
		url = 'https://sandbox-api.stagingapps.net/merchant/order/reports/data'
		#url = 'https://sandbox-api.stagingapps.net/merchant/product?limit=0'
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		if response.status_code == 200:
			res = response.json()

			filters = []
			closed = []
			for data in res['data']:
				#if data['payment_type'] == 'qr_code':
				if data['status_order'] == "CANCELLED":
					filters.append(data)
				#elif data['']

		else:
			res = 'Error ' + str(response.status_code)



		# # ==========================================================================================
		# # Set data Inbound dan Outbound di Jurnal untuk otomatisasi pembayaran PAID
		# # ==========================================================================================
		# journals = http.request.env['account.journal'].search([])

		# for journal in journals:
		# 	if journal.type == 'bank' or journal.type == 'cash':
		# 		journal.inbound_payment_method_line_ids[0].sudo().write({'payment_account_id': journal.default_account_id.id})
		# 		journal.outbound_payment_method_line_ids[0].sudo().write({'payment_account_id': journal.default_account_id.id})
		# # ==========================================================================================

		# # ==========================================================================================
		# # Set data CoA Template ke Company baru
		# # ==========================================================================================
		# getCompany = http.request.env['res.company'].search([('id', '=', 8)], limit=1)
		# print("Ini data Company : ", getCompany)
		# data = http.request.env['account.chart.template'].search([], limit=1)
		# print(data.name)
		# # 11 disini pajak dan pembelian defaul, kalau dari contoh otomatisnya 11 jadi disamain 11 juga
		# data._load(11,11,getCompany)
		# # ==========================================================================================
		

		# ==========================================================================================
		# Reset Data in Order
		# ==========================================================================================
		#getOrder = http.request.env['sale.order'].search([('name', '=', 'SBX220927200297')], limit=1)
		#getOrder = http.request.env['sale.order'].search([])
		# print(getOrder)
		# getOrder.sudo().write({
		# 	'state': 'draft',
		# })

		# ==========================================================================================
		# Reset Data in Invoice
		# ==========================================================================================	
		#getInvoice = http.request.env['account.move'].search([])
		# # # print(getOrder)
		# getInvoice.sudo().write({
		# 	'state': 'draft',
		# })


		

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		#console += 'console.log(' + json.dumps(filters) + ');'
		console += '</script>'

		return console


class RestApiStore(http.Controller):
	@http.route('/restapi/store', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/store?offset=0&limit=0'
		#url = 'https://sandbox-api.stagingapps.net/merchant/productstore/2'
		#merchant/productstore/1
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		if response.status_code == 200:
			res = response.json()
		else:
			res = 'Error ' + str(response.status_code)

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		#console += 'console.log(' + json.dumps(resData) + ');'
		console += '</script>'

		return console

class RestApiStore(http.Controller):
	@http.route('/restapi/order', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/orders/list?limit=0&offset=0&status_order=PENDING'
		#merchant/productstore/1
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		if response.status_code == 200:
			res = response.json()
		else:
			res = 'Error ' + str(response.status_code)

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		#console += 'console.log(' + json.dumps(resData) + ');'
		console += '</script>'


		newOrder = http.request.env['sale.order'].sudo().create({
			'name': 'TESTAJAADAENGGA',
			'partner_id': False,
			'date_order': datetime.strptime("2022-09-05 12:40:18", '%Y-%m-%d %H:%M:%S'),
			'order_line': [],
			'state': 'sale',
		})


		return console

# =====================================================================================================
# Get Tax and Service Data form Sandbox
# =====================================================================================================
class ApiSetTax(http.Controller):
	@http.route('/api/tax', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/feesetting'
		response = requests.get(url, headers=headers, data=json.dumps(data))	
		#
		if response.status_code == 200:	
			res = response.json()
			res = res['data'][0]
			# Insert / Update Tax
			tax = int(res['tax'])
			service = int(res['service'])
			getTax = http.request.env['account.tax'].search([('sandbox_tax', '=', True)], limit=1)
			print('===================================== CEK Tax : ', len(getTax))
			if len(getTax) != 0:
				#
				getTax.sudo().write({
					'name': str(tax) + '% Pajak',
					'amount': tax,
				})
			else:
				insertTax = http.request.env['account.tax'].sudo().create({
					'name': str(tax) + '% Pajak',
					'amount': tax,
					'description': 'Pajak',
					'sandbox_tax': True,
				})
			# Insert / Update Service
			getService = http.request.env['account.tax'].search([('sandbox_service', '=', True)], limit=1)
			print('===================================== CEK Services : ', len(getService))
			if len(getService) != 0:
				#
				getService.sudo().write({
					'name': str(service) + '% Biaya Layanan',
					'amount': service,
				})
			else:
				insertServices = http.request.env['account.tax'].sudo().create({
					'name': str(service) + '% Biaya Layanan',
					'amount': service,
					'description': 'Biaya Layanan',
					'sandbox_service': True,
				})

		else:
			res = 'Error ' + str(response.status_code)

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		#console += 'console.log(' + json.dumps(resData) + ');'
		console += '</script>'

		return console


# =====================================================================================================
# Get Orders Data form Sandbox
# =====================================================================================================
class ApiOrders(http.Controller):
	@http.route('/api/orders', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/order/reports/data'
		#url = 'https://sandbox-api.stagingapps.net/merchant/orders/list?limit=0&offset=0&status_order=NEW_ORDER'
		#merchant/productstore/1
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		if response.status_code == 200:
			res = response.json()
			# Request data from Odoo
			getPartners = http.request.env['res.partner'].search([('partner_status', '=', 'customer')])
			getProducts = http.request.env['product.product'].search([])
			getOrders = http.request.env['sale.order'].search([])
			#
			getTax = http.request.env['account.tax'].search([('sandbox_tax', '=', True)])
			getService = http.request.env['account.tax'].search([('sandbox_service', '=', True)])
			# Default customer, added when getData customer from Sandbox API
			customer = http.request.env['res.partner'].search([('customer_id', '=', 0)], limit=1).id
			# Loop data from API
			for data in res['data']:
				# Boolean to filter data, add new data if its true
				addNew = True
				# Check if data already exist in Odoo
				for order in getOrders:
					#print(data['order_number'], ' / ', order['name'])
					if data['order_number'] == order['name']:
						addNew = False
				# Check data customer, default value is 0
				for partner in getPartners:
					# Using name instead of id because return data from sandbox doesn't have customer_id 
					if data['customer_name'] == partner['name']:
						customer = partner['id']
				# Start of Orderline =================================================================
				orderline = []
				# If addNew is Flase, add new array to clear orderline data first
#				if addNew == False:
#					orderline.append((5,0,0))
				# Loop data in order_detail
				for order in data['order_detail']:
					# Check if data in order_detail is exist in Odoo
					for product in getProducts:
						# If data product exist in Odoo add to orderline
						if int(order['product_id']) == int(product['product_id']):
							# Order partner_id is set default to 0
							orderlineData = {
								'order_partner_id': customer,
								'product_id': product['id'],
								'product_uom_qty': order['product_qty'],
								'price_unit': order['product_price'],
								'tax_id': [(6,0, [getTax.id, getService.id])]
							}
							orderline.append((0,0,orderlineData))
					
					# ================================================================================
					# If order have sub-order / productAddOn in Sandbox
					for subOrder in order['productAddOn']:
						# Check sub-order data with Odoo product data
						for product in getProducts:
							# If data product exist in Odoo add to orderline
							if int(subOrder['product_id']) == int(product['product_id']):
								orderlineData = {
									'order_partner_id': customer,
									'product_id': product['id'],
									'product_uom_qty': subOrder['product_qty'],
									'price_unit': subOrder['product_price'],
									'tax_id': [(6,0, [getTax.id, getService.id])]
								}
								orderline.append((0,0,orderlineData))
								print('Ada Sub Order di data : ', data['order_number'])
				# End of Orderline ====================================================================
				# Default partner_id is 0, its created when updating data customer from sandbox 
				#
				dateOrder = datetime.strptime(data['payment_date'], '%Y-%m-%d %H:%M:%S')
				dateOrder = dateOrder - timedelta(hours=7,minutes=0)
				# Untuk sekarangs status close masuk ke draft karna belum tahu
				status = 'draft'
				if data['status'] == "NEW_ORDER":
					status = 'done'
				elif data['status'] == "CANCELLED":
					status = 'cancel'
				elif data['status'] == "CLOSED":
					status = 'draft'
				#
				dataOrder = {
					'name': data['order_number'],
					'partner_id': customer,
					#'date_order': datetime.strptime(data['payment_date'], '%Y-%m-%d %H:%M:%S'),
					'date_order': dateOrder,
					'order_line': orderline,
					'state': status,
				}
				# Check data Update/Create
				if addNew == True:
					newOrder = http.request.env['sale.order'].sudo().create(dataOrder)
					print('Data Order berhasil ditambahkan : ', data['order_number'])
#				else:
#					getOrder = http.request.env['sale.order'].search([('name', '=', data['order_number'])], limit=1)
#					getOrder.sudo().write(dataOrder)
#					print('Data Order berhasil diupdate : ', data['order_number'])
		else:
			res = 'Error ' + str(response.status_code)

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		#console += 'console.log(' + json.dumps(resData) + ');'
		console += '</script>'

		return console


# =====================================================================================================
# Get Products Data form Sandbox
# =====================================================================================================
class ApiProducts(http.Controller):
	@http.route('/api/products', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/product?limit=0'
		response = requests.get(url, headers=headers, data=json.dumps(data))

		# Check response
		if response.status_code == 200:
			# Response 200 / Success
			res = response.json()
			# Get data product in Odoo
			getProducts = http.request.env['product.product'].search([])
			#
			for data in res['data']:
				#print(data)
				addNew = True
				for product in getProducts:
					#print(data['product_id'], ' / ', product['product_id'])
					if int(data['product_id']) == int(product['product_id']):
						addNew = False
						break
				#
				if addNew == True:
					# Create if data didnt exist
					insertProduct = http.request.env['product.product'].sudo().create({
						'name': data['product_name'],
						'list_price': float(data['product_detail']['product_price']),
						'merchant_id': int(data['merchant_id']),
						'brand_id': int(data['brand']['id']),
						'product_id': int(data['product_id']),	
						'default_code': data['no_sku'],	
						'taxes_id': False,
						'company_id': 2,
					})
					print('=================== Data berhasil ditambahkan : ', data['product_name'])
				else:
					# Update if data exist
					updateProduct = http.request.env['product.product'].search([('product_id', '=', data['product_id'])], limit=1)
					updateProduct.sudo().write({
						'name': data['product_name'],
						'list_price': float(data['product_detail']['product_price']),
						'merchant_id': int(data['merchant_id']),
						'brand_id': int(data['brand']['id']),
						'product_id': int(data['product_id']),	
						'default_code': data['no_sku'],
						'taxes_id': False,
						'company_id': 2,
					})
					print('=================== Data Sudah di Update : ', data['product_name'])		
		else:
			# Response error
			res = 'Error ' + str(response.status_code)

		# Show data in console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		console += '</script>'

		return console


# =====================================================================================================
# Get Customers Data form Sandbox
# =====================================================================================================
class ApiCustomers(http.Controller):
	@http.route('/api/customers', auth='public')
	def index(self, **kw):
		headers = {
			'token': kw.get('token'),
			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/customer?limit=0&offset=0&sort=id'
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		getCustomers = http.request.env['res.partner'].search([('partner_status', '=', 'customer')])
		#print(getCustomers)
		#
		if response.status_code == 200:
			res = response.json()
			# Default Data for Unregistered Customer
			DefaultCus = {
				'id': 0,
				'email': False,
				'name': 'No Name',
				'last_purchase': False,
				'phone': False,
				'register_date': False,
				'status': True,
			}
			res['data'].append(DefaultCus)
			#
			for data in res['data']:
				#print(data['name'])
				#
				addNew = True
				# Check if data from res.partner exist
				for customer in getCustomers:
					# Convert variable to integer to prevent miss match type
					if int(data['id']) == int(customer['customer_id']):
						addNew = False
						break
				#
				if data['status'] == True:
					#
					if addNew == True:
						# Create if data didnt exist
						insertCustomer = http.request.env['res.partner'].sudo().create({
							'name': data['name'],
							'email': data['email'],
							'phone': data['phone'],
							#'create_date': int(data['brand']['id']),
							'active': data['status'],
							'customer_id': data['id'],
							'partner_status': 'customer',
							'company_id': 2,
						})
						print('=================== Data berhasil ditambahkan : ', data['name'])
					else:
						# Update if data exist
						updateCustomer = http.request.env['res.partner'].search([('customer_id', '=', data['id'])], limit=1)
						updateCustomer.sudo().write({
							'name': data['name'],
							'email': data['email'],
							'phone': data['phone'],
							#'create_date': int(data['brand']['id']),
							'active': data['status'],
							'customer_id': data['id'],
							'partner_status': 'customer',
							'company_id': 2,
						})
						print('=================== Data Sudah di Update : ', data['name'])	

		else:
			res = 'Error ' + str(response.status_code)

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(res) + ');'
		#console += 'console.log(' + getCustomers + ');'
		console += '</script>'

		return console



# Testing untuk update data Products
class RestApi(http.Controller):
	@http.route('/restapi/test', auth='public')
	def index(self, **kw):
		#https://sandbox-api.stagingapps.net/brand/210/detail?merchant_id=1&store_id=601
		data = {}
		url = "https://sandbox-api.stagingapps.net/brand/210/detail?merchant_id=1&store_id=601"
		response = requests.get(url, data=json.dumps(data))		        
		res = response.json()

		# Isi res ada 3 item [meta, message, data]
		#print(res['data'])

		resData = res['data']

		getProducts = http.request.env['product.product'].search([])


		# Filter data dari Sandbox
		arr = []

		for category in resData['category']:
			#
			#arr.append(category['products'])
			#print(category['products'])
			if category['products'] != None:
				#print(category['products'])
				for product in category['products']:
					#print(product['product_id'])
					arr.append(product)

					dataExist = False

					for getProduct in getProducts:
						print(product['product_id'], ' / ', getProduct['product_id'])
						if int(getProduct['product_id']) == int(product['product_id']):
							dataExist = True
							break

					# Cek data
					if dataExist == False:
						# Jika data belum ada, tambahkan data baru
						insertProduct = http.request.env['product.product'].sudo().create({
							'name': product['product_name'],
							'list_price': float(product['product_price']),
							'product_id': int(product['product_id']),
						})
						print('=================== Data berhasil ditambahkan')
					else:
						# Jika data sudah ada, Edit data yang lama
						updateProduct = http.request.env['product.product'].search([('product_id', '=', product['product_id'])], limit=1)
						updateProduct.sudo().write({
							'name': product['product_name'],
							'list_price': float(product['product_price']),
						})
						print('=================== Data Sudah di Update')

		# Munculkan data di console browser
		console = '<script>'
		console += 'console.log(' + json.dumps(resData) + ');'
		#console += 'console.log(' + json.dumps(resData) + ');'
		console += 'console.log(' + json.dumps(arr) + ');'
		console += '</script>'

		return console



# Testing untuk update data Order
class RestApiPOS(http.Controller):
	@http.route('/restapi/pos', auth='public')
	def index(self, **kw):
		# Skip dlu cari datanya, sekarang coba buat data order dlu aja random

		insertProduct = http.request.env['pos.config'].sudo().create({
			'name': 'Toko 2',
			'company_id': 5,
			'payment_method_ids': [(4, 4)],
			'journal_id': 29
		})

		# Masih Error Constraint: pos_config_journal_id_fkey
		return 'HAHAHAHHA'












# # =====================================================================================================
# # Get Orders Data form Sandbox
# # =====================================================================================================
# class ApiOrders(http.Controller):
# 	@http.route('/api/orders', auth='public')
# 	def index(self, **kw):
# 		headers = {
# 			'token': kw.get('token'),
# 			'api_key': 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e',
# 			'content-type': 'application/json'
# 		}
# 		data = {}
# 		#url = 'https://sandbox-api.stagingapps.net/merchant/store?offset=0&limit=0'
# 		url = 'https://sandbox-api.stagingapps.net/merchant/orders/list?limit=0&offset=0&status_order=NEW_ORDER'
# 		#merchant/productstore/1
# 		response = requests.get(url, headers=headers, data=json.dumps(data))
# 		#
# 		if response.status_code == 200:
# 			res = response.json()
# 			#
# 			getPartners = http.request.env['res.partner'].search([('partner_status', '=', 'customer')])
# 			getProducts = http.request.env['product.product'].search([])
# 			getOrders = http.request.env['sale.order'].search([])
# 			#
# 			for data in res['data']:
# 				#
# 				addNew = True
# 				# Check if data already exist in Odoo
# 				for order in getOrders:
# 					print(data['order_number'], ' / ', order['name'])
# 					if data['order_number'] == order['name']:
# 						addNew = False

# 				# Synch data Partner and Products and Create data Order
# 				dataOrder = False
# 				for partner in getPartners:
# 					# print(data['customer_name'], ' / ', partner['name'])
# 					# If data customer exist in Odoo
# 					if data['customer_name'] == partner['name']:
# 						#print(data)
# 						orderline = []
# 						# If addNew is False, add new array to clear orderline data first
# 						if addNew == False:
# 							orderline.append((5,0,0))
# 						#
# 						for order in data['order_detail']:
# 							#
# 							for product in getProducts:
# 								# If data product exist in Odoo
# 								if order['product_id'] == product['product_id']:
# 									order = {
# 										'order_partner_id': partner['id'],
# 										'product_id': product['id'],
# 										'product_uom_qty': order['product_qty'],
# 									}
# 									orderline.append((0,0,order))
# 									#orderline.append((order))
# 						#print(orderline)
# 						dataOrder = {
# 							'name': data['order_number'],
# 							'partner_id': partner['id'],
# 							'date_order': datetime.strptime(data['payment_date'], '%Y-%m-%d %H:%M:%S'),
# 							'order_line': orderline,
# 							#'state': 'sale',
# 						}
# 						#print(newOrder)

# 				# Check if dataOrder not empty
# 				if dataOrder != False:
# 					# Check data Update/Create
# 					if addNew == True:
# 						newOrder = http.request.env['sale.order'].sudo().create(dataOrder)
# 						print('Data Order berhasil ditambahkan : ', data['order_number'])
# 					else:
# 						getOrder = http.request.env['sale.order'].search([('name', '=', data['order_number'])], limit=1)
# 						getOrder.sudo().write(dataOrder)
# 						print('Data Order berhasil diupdate : ', data['order_number'])

# 		else:
# 			res = 'Error ' + str(response.status_code)

# 		# Munculkan data di console browser
# 		console = '<script>'
# 		console += 'console.log(' + json.dumps(res) + ');'
# 		#console += 'console.log(' + json.dumps(resData) + ');'
# 		console += '</script>'

# 		return console


