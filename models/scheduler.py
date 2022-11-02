# -*- coding: utf-8 -*-
from odoo import models, fields, api, http
from datetime import date, datetime, timedelta
import json
import requests
import math

class SchedulerSandbox(models.Model):
	_name = 'api.scheduler'

	def updateProduct(self, idk):
		# print("HAHAHAHA")
		# token = self.env.user.company_id.id
		print('=======Get Active Company=======')
		print('Company id => ',self.env.company.id)
		print('Company name => ', self.env.company.name)
		print('=======Get Active Company=======')

		return self.env.company


	def cron_schedule(self, uid=False):
		print(' Sandbox Cron Job')
		print('========================================================================')
		# If uid isn't False then its manual update from button
		domain = []
		if uid != False:
			domain = [('id', '=', uid)]
		# Get All User Data
		Users = http.request.env['res.users'].search(domain)
		#print(Users)

		for user in Users:
			print('User : ', user.name)
			# Define variable 
			apiUser = user.sandbox_id
			apiPass = user.sandbox_pw
			apiKey = str(user.sandbox_apikey)
			#print('Email : ', apiUser, ' Pass : ', apiPass, ' APIKEY : ', apiKey)
			# Get Token per user
			token = self.getTokenV1(apiKey, apiUser, apiPass)
			if token != False:
				# If get token success create / update company by user
				print('Token : ', token)
				# Get List Merchant from token
				merchants = self.getMerchantListFromToken(apiKey, token)
				if merchants != False:
					print('Merchant : ', merchants)
					# If get merchants list success, check if merchant exist in odoo company
					# Get data company first then loop, domain by email
					companies = http.request.env['res.company'].search([('email', '=', apiUser)])
					#
					merchant_ids = []
					#
					for merchant in merchants:
						addMerchant = True
						#
						company_id = False
						#
						# Check with data companies
						for company in companies:
							# Add company_id to array to update allowed_company user
							merchant_ids.append(company.id)
							#
							if int(company.sandbox_merchant_id) == int(merchant['id']):
								addMerchant = False
								company_id = company.id
								break
						#
						if addMerchant == True:
							# Add New Merchant to Odoo Company
							NewCompany = http.request.env['res.company'].sudo().create({
								'name': merchant['full_name'],
								'email': merchant['email'],
								'sandbox_merchant_id': merchant['id'],
							})
							# Add New company_id to merchant_ids
							merchant_ids.append(NewCompany.id)
							company_id = NewCompany.id
							# Set CoA Template for new Company, country_id 100 for Indonesia
							coaTemplate = http.request.env['account.chart.template'].search([('country_id', '=', 100)], limit=1)
							coaTemplate._load(11, 11, NewCompany)
							# Set default Outstanding for automatic paid invoice
							journals = http.request.env['account.journal'].search([('company_id', '=', NewCompany.id)])
							for journal in journals:
								if journal.type == 'bank' or journal.type == 'cash':
									journal.inbound_payment_method_line_ids[0].sudo().write({'payment_account_id': journal.default_account_id.id})
									journal.outbound_payment_method_line_ids[0].sudo().write({'payment_account_id': journal.default_account_id.id})
							# You can create new journal here and set the inbound/outbound like above code


						# Login V2 disini?
						tokenMerchant = self.getTokenV2(apiKey, merchant['email'], merchant['id'])
						#
						if tokenMerchant != False:
							#print(tokenMerchant)
							# Update Data Customers by company_id
							customers = self.cronCustomers(apiKey, tokenMerchant, company_id)
							if customers != False:
								products = self.cronProducts(apiKey, tokenMerchant, company_id)
								if products != False:
									taxes = self.cronTaxes(apiKey, tokenMerchant, company_id)
									if taxes != False:
										orders = self.cronOrders(apiKey, tokenMerchant, company_id, user.partner_id.id)
										print('Cron Job : ', merchant['full_name'], ' success!!!')
									else:
										print('Error when access orders data!')
								else:
									print('Error when access products data!')
							else:
								print('Error when access customers data!')

						else:
							print('Error when request token merchant!')



					# Update Allowed Company in User
					#print(merchant_ids)
					#print(merchant_ids[0])
					user.sudo().write({
						'company_id': merchant_ids[0],
						'company_ids': [(6,0, merchant_ids)],
					})

				else:
					print('Error at getting merchant list')
			else:
				print('Error')




		# Get API Info
		#apiKey = 'Basic 15cb7ebf9-3dcc-h28s-b056-2522c1eed03e'
		# token = self.getToken(apiKey)
		
		# Buat cron job di loop dari res.company, cek kalau data sandbox api nya tidak kosong
		# baru mulai cron job api, kalau kosong skip aja


		# # Cron Job Customers
		# customers = self.cronCustomers(apiKey, token)
		# if customers != False:
		# 	# Cron Job Products
		# 	products = self.cronProducts(apiKey, token)


		# 	print('Cron Job Success')

		

	# ===============================================================================
	# Generate token in v1, sent generate token to v2 to get all merchant list
	# Get Token API NEW
	def getTokenV1(self, apiKey, email, password):
		headers = {
			'api_key': apiKey,
			'content-type': 'application/json'
		}
		body = {
			'email': email,
			'password': password,
			'device_model': 'WEB',
			'device_type': 'WEB',
			'device_id': '1'
		}
		url = "https://sandbox-api.stagingapps.net/merchants/session/login_v2/step_1"
		response = requests.post(url, headers=headers, data=json.dumps(body))		        
		if response.status_code == 200:
			data = response.json()['data']['access_token']
		else:
			data = False
		#
		return data

	def getTokenV2(self, apiKey, email, id):
		headers = {
			'api_key': apiKey,
			'content-type': 'application/json'
		}
		body = {
			'email': email,
			'id': id,
			'device_model': 'WEB',
			'device_type': 'WEB',
			'device_id': '1'
		}
		url = "https://sandbox-api.stagingapps.net/merchants/session/login_v2/step_2"
		response = requests.post(url, headers=headers, data=json.dumps(body))		        
		if response.status_code == 200:
			data = response.json()['data']['access_token']
		else:
			data = False
		#
		return data

	def getMerchantListFromToken(self, apiKey, token):
		#https://sandbox-api.stagingapps.net/merchants/list
		headers = {
			'api_key': apiKey,
			'token': token,
			'content-type': 'application/json'
		}
		body = {}
		url = "https://sandbox-api.stagingapps.net/merchants/list"
		response = requests.get(url, headers=headers, data=json.dumps(body))		        
		if response.status_code == 200:
			data = response.json()['data']
		else:
			data = False
		#
		return data


	# ===============================================================================
	# Get Token API OLD
	def getToken(self, apiKey, email, password):
		headers = {
			'api_key': apiKey,
			'content-type': 'application/json'
		}
		body = {
			#'email': 'sandbox.wgs@gmail.com',
			'email': email,
			#'password': 'qwerty123',
			'password': password,
			'device_model': 'WEB',
			'device_type': 'WEB',
			'device_id': '1'
		}
		url = "https://sandbox-api.stagingapps.net/merchants/session/login"
		response = requests.post(url, headers=headers, data=json.dumps(body))		        
		if response.status_code == 200:
			data = response.json()['data']['access_token']
		else:
			data = False
		#
		return data

	# ===============================================================================
	# Cron Job Customers Function
	def cronCustomers(self, apiKey, token, company_id):
		headers = {'token': token, 'api_key': apiKey, 'content-type': 'application/json'}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/customer?limit=0&offset=0&sort=id'
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		getCustomers = http.request.env['res.partner'].search([('partner_status', '=', 'customer')])
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
				'status': True
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
						insertProduct = http.request.env['res.partner'].sudo().create({
							'name': data['name'],
							'email': data['email'],
							'phone': data['phone'],
							#'create_date': int(data['brand']['id']),
							'active': data['status'],
							'customer_id': data['id'],
							'partner_status': 'customer',
							'company_id': company_id,
						})

						print('#### Customer Baru : ', data['name'])
					else:
						# Update if data exist
						updateProduct = http.request.env['res.partner'].search([('customer_id', '=', data['id'])], limit=1)
						updateProduct.sudo().write({
							'name': data['name'],
							'email': data['email'],
							'phone': data['phone'],
							#'create_date': int(data['brand']['id']),
							'active': data['status'],
							'customer_id': data['id'],
							'partner_status': 'customer',
							'company_id': company_id,
						})
						print('#### Customer Edit : ', data['name'])	

		else:
			res = False
			print('Error : Terjadi error di fungsi customer')
		print('========================================================================')
		return res

	# ===============================================================================
	# Cron Job Products Function
	def cronProducts(self, apiKey, token, company_id):
		headers = {'token': token, 'api_key': apiKey, 'content-type': 'application/json'}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/product?limit=0'
		response = requests.get(url, headers=headers, data=json.dumps(data))
		# Check response
		if response.status_code == 200:
			res = response.json()
			# Payment Fee for customer using xendit payment method
			getPaymentFee = http.request.env['product.product'].search([('company_id', '=', company_id), ('product_payments', '=', 1)])
			if not getPaymentFee:
				insertPaymentFee = http.request.env['product.product'].sudo().create({
					'name': 'Payment Fee',
					'list_price': float(0),
					#'merchant_id': int(data['merchant_id']),
					#'brand_id': int(data['brand']['id']),
					#'product_id': 0,	
					'default_code': False,	
					'taxes_id': False,
					'company_id': company_id,
					'detailed_type': 'service',
					'product_discount': 0,
					'product_payments': 1,
				})
				print('#### Data Payment Fee Sudah ditambahkan')
				print('========================================================================')
			print(getPaymentFee)
			#
			# Delivery Fee for customer using shipper api
			getDeliveryFee = http.request.env['product.product'].search([('company_id', '=', company_id), ('product_payments', '=', 2)])
			if not getDeliveryFee:
				insertDeliveryFee = http.request.env['product.product'].sudo().create({
					'name': 'Delivery Fee',
					'list_price': float(0),
					#'merchant_id': int(data['merchant_id']),
					#'brand_id': int(data['brand']['id']),
					#'product_id': 0,	
					'default_code': False,	
					'taxes_id': False,
					'company_id': company_id,
					'detailed_type': 'service',
					'product_discount': 0,
					'product_payments': 2,
				})
				print('#### Data Payment Delivery Fee Sudah ditambahkan')
				print('========================================================================')
			print(getPaymentFee)

			#
			# Get data product in Odoo by company_id
			getProducts = http.request.env['product.product'].search([('company_id', '=', company_id)])
			#
			for data in res['data']:
				addNew = True
				for product in getProducts:
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
						'company_id': company_id,
						'detailed_type': 'product',
						'product_discount': data['product_detail']['discount']
					})
					print('#### Produk Baru : ', data['product_name'], ' Diskon : ', insertProduct['product_discount'])
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
						'company_id': company_id,
						'detailed_type': 'product',
						'product_discount': data['product_detail']['discount']
					})
					print('#### Produk Edit : ', data['product_name'], ' Diskon : ', updateProduct['product_discount'])		
		else:
			res = False
			print('Error : Terjadi error di fungsi product')

		print('========================================================================')
		return res


	# ===============================================================================
	# Cron Job Taxes Function
	def cronTaxes(self, apiKey, token, company_id):
		headers = {
			'token': token,
			'api_key': apiKey,
			'content-type': 'application/json'
		}
		data = {}
		url = 'https://sandbox-api.stagingapps.net/merchant/feesetting'
		response = requests.get(url, headers=headers, data=json.dumps(data))	
		#
		if response.status_code == 200:	
			res = response.json()
			res = res['data'][0]
			# Update Payemnt Fee Type
			company = http.request.env['res.company'].search([('id', '=', company_id)], limit=1)
			if len(company) != 0:
				company.sudo().write({'sandbox_payment_fee': res['payment_fee_type']})
				#print(updateCompany)
			# Insert / Update Tax
			tax = int(res['tax'])
			service = int(res['service'])
			getTax = http.request.env['account.tax'].search([('sandbox_tax', '=', True), ('company_id', '=', company_id)], limit=1)
			#print('===================================== CEK Tax : ', len(getTax))
			if len(getTax) != 0:
				#
				getTax.sudo().write({
					'name': str(tax) + '% Pajak',
					'amount': tax,
					'company_id': company_id,
				})
			else:
				insertTax = http.request.env['account.tax'].sudo().create({
					'name': str(tax) + '% Pajak',
					'amount': tax,
					'description': 'Pajak',
					'sandbox_tax': True,
					'company_id': company_id,
				})
			# Insert / Update Service
			getService = http.request.env['account.tax'].search([('sandbox_service', '=', True), ('company_id', '=', company_id)], limit=1)
			#print('===================================== CEK Services : ', len(getService))
			if len(getService) != 0:
				#
				getService.sudo().write({
					'name': str(service) + '% Biaya Layanan',
					'amount': service,
					'company_id': company_id,
				})
			else:
				insertServices = http.request.env['account.tax'].sudo().create({
					'name': str(service) + '% Biaya Layanan',
					'amount': service,
					'description': 'Biaya Layanan',
					'sandbox_service': True,
					'company_id': company_id,
				}) 
			# Create cash rounding rule for Taxes
			# Probably global data, so all company can use 1 data for rounding
			getRounding = http.request.env['account.cash.rounding'].search([])
			if len(getRounding) == 0:
				insertRounding = http.request.env['account.cash.rounding'].sudo().create({
					'name': 'Pembulatan Pajak',
					'rounding': 1,
					'strategy': 'biggest_tax',
					'rounding_method': 'HALF-UP',
					#'company_id': company_id,
				}) 

		else:
			res = False
			print('Error : Terjadi error di fungsi taxes')

		return res


	# ===============================================================================
	# Cron Job Orders Function
	def cronOrders(self, apiKey, token, company_id, user_id):
		headers = {
			'token': token,
			'api_key': apiKey,
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
			getPartners = http.request.env['res.partner'].search([('partner_status', '=', 'customer'), ('company_id', '=', company_id)])
			getProducts = http.request.env['product.product'].search([('company_id', '=', company_id)])
			getOrders = http.request.env['sale.order'].search([])
			#
			getCompany = company = http.request.env['res.company'].search([('id', '=', company_id)], limit=1)
			#
			getTax = http.request.env['account.tax'].search([('sandbox_tax', '=', True), ('company_id', '=', company_id)])
			getService = http.request.env['account.tax'].search([('sandbox_service', '=', True), ('company_id', '=', company_id)])
			#
			#res = res['data']
			res = reversed(res['data'])
			# Loop data from API

			#Ambil 10 data aja buat nyoba dulu
			# array = []
			# i = 0
			# for data in res:
			# 	if i < 40:
			# 		array.append(data)
			# 		i = i + 1
			# 	else:
			# 		break
			# array = reversed(array)


			for data in res:
			#for data in array:
				# Boolean to filter data, add new data if its true
				addNew = True
				# Default customer, added when getData customer from Sandbox API
				customer = http.request.env['res.partner'].search([('customer_id', '=', 0), ('company_id', '=', company_id)], limit=1).id
				# Check if data already exist in Odoo
				for order in getOrders:
					if data['order_number'] == order['name']:
						addNew = False

				# If it's new data, add data to Odoo
				if addNew == True:
					# Check data customer, default value is 0
					for partner in getPartners:
						# Using name instead of id because return data from sandbox doesn't have customer_id 
						if data['customer_name'] == partner['name']:
							customer = partner['id']
					# ====================================================================================
					# Start of Orderline =================================================================
					# ====================================================================================
					orderline = []
					# If addNew is Flase, add new array to clear orderline data first
					sectionLine = (0, 0, {'display_type': 'line_section', 'name': 'Produk',})
					orderline.append(sectionLine)
					# Total Price
					sub_total = 0
					# Loop data in order_detail
					for order in data['order_detail']:
						# Missing Product, if product didnt exist in Odoo then add new to Odoo
						mainProduct = True	
						# Check if data in order_detail is exist in Odoo
						for product in getProducts:
							# If data product exist in Odoo add to orderline
							if int(order['product_id']) == int(product['product_id']):
								# Product exist in Odoo
								mainProduct = False
								# 
								price = order['product_price']
								#
								sub_total = sub_total + (int(price) * int(order['product_qty']))
								#
								orderlineData = {
									'order_partner_id': customer,
									'product_id': product['id'],
									'product_uom_qty': order['product_qty'],
									#'price_unit': order['product_price'],
									'price_unit': price,
									'tax_id': [(6,0, [getTax.id, getService.id])],
									#'discount': product['product_discount'],
								}
								orderline.append((0,0,orderlineData))
						
						# ================================================================================
						# If Product didnt exist in Odoo add New
						if mainProduct == True:		
							# Create new product	
							createProduct = http.request.env['product.product'].sudo().create({
								'name': order['product_name'],
								'list_price': float(order['product_price']),
								'merchant_id': int(getCompany['sandbox_merchant_id']),								
								'product_id': int(order['product_id']),	
								'taxes_id': False,
								'company_id': company_id,
								'detailed_type': 'product',
							})
							# Add New Product to oder.orderline
							orderlineData = {
								'order_partner_id': customer,
								'product_id': createProduct['id'],
								'product_uom_qty': order['product_qty'],
								'price_unit': order['product_price'],
								'tax_id': [(6,0, [getTax.id, getService.id])],
							}
							orderline.append((0,0,orderlineData))
						# ================================================================================
						# If order have sub-order / productAddOn in Sandbox
						for subOrder in order['productAddOn']:
							# Missing Sub Product
							subProduct = True
							# Check sub-order data with Odoo product data
							productData = subOrder
							for product in getProducts:
								# If data product exist in Odoo add to orderline
								if int(subOrder['product_id']) == int(product['product_id']):
									# Product Exist in Odoo
									subProduct = False							
									# Calculate Price first
									price = subOrder['product_price']
									#
									sub_total = sub_total + (int(price) * int(subOrder['product_qty']))
									#
									orderlineData = {
										'order_partner_id': customer,
										'product_id': product['id'],
										'product_uom_qty': subOrder['product_qty'],
										'price_unit': price,
										'tax_id': [(6,0, [getTax.id, getService.id])],
									}
									orderline.append((0,0,orderlineData))
							# ================================================================================
							# If Product didnt exist in Odoo add New
							if subProduct == True:		
								# Create new product	
								createProduct = http.request.env['product.product'].sudo().create({
									'name': subOrder['product_name'],
									'list_price': float(subOrder['product_price']),
									'merchant_id': int(getCompany['sandbox_merchant_id']),								
									'product_id': int(subOrder['product_id']),	
									'taxes_id': False,
									'company_id': company_id,
									'detailed_type': 'product',
								})
								# Add New Product to oder.orderline
								orderlineData = {
									'order_partner_id': customer,
									'product_id': createProduct['id'],
									'product_uom_qty': subOrder['product_qty'],
									'price_unit': subOrder['product_price'],
									'tax_id': [(6,0, [getTax.id, getService.id])],
								}
								orderline.append((0,0,orderlineData))
					# ====================================================================================
					# End of Orderline ===================================================================
					# ====================================================================================
					# Add Payment Fee ====================================================================
					# ====================================================================================
					# Create new section in orderline
					sectionLine = (0, 0, {'display_type': 'line_section', 'name': 'Biaya Lainnya',})
					orderline.append(sectionLine)
					# Add payment fee to product and get it in product list Odoo
					payment_fee = http.request.env['product.product'].search([('company_id', '=', company_id), ('product_payments', '=', 1)], limit=1)
					# Get Payment Method from sandbox by order payment type
					PaymentMethod = self.getPaymentMethod(apiKey, getCompany.sandbox_merchant_id, data['payment_type'])
					if PaymentMethod != False:
						# There's 3 type payment (owner, customer, split) in getCompany.sandbox_payment_fee
						# owner = Owner pay all payment fee
						# customer = Customer pay all payment fee
						# split = Payment fee divided by half for customer and owner 
						payment_price = int(PaymentMethod['payment_fee_price'])
						payment_price_percentage = sub_total * (float(PaymentMethod['payment_fee_percentage']) / 100)
						totalPayment = payment_price + math.ceil(payment_price_percentage)
						# If Payment Fee Type is SPLIT or OWNER
						if getCompany.sandbox_payment_fee == 'SPLIT':
							# Fee is half for both owner and customer
							totalPayment = totalPayment / 2
						elif getCompany.sandbox_payment_fee == 'OWNER':
							# No fee for customer, all goes to owner
							totalPayment = 0
						# Add payment fee to order line
						PaymentFee = {
							'order_partner_id': customer,
							'product_id': payment_fee.id,
							'product_uom_qty': 1,
							'price_unit': math.ceil(totalPayment),
							'tax_id': [],
							'name': str(PaymentMethod['payment_name']) + ' - ' + str(getCompany.sandbox_payment_fee)
						}
						orderline.append((0,0,PaymentFee))
					# ====================================================================================
					# Check Order Type ===================================================================
					# ====================================================================================
					# If order type is "DELIVERY", add delivery cost from Shipper
					if data['order_type'] == 'DELIVERY':
						# Get Delivery Fee from product
						delivery_fee = http.request.env['product.product'].search([('company_id', '=', company_id), ('product_payments', '=', 2)], limit=1)
						
						# Get Shipping Data
						getShipping = self.getShipperData(apiKey, data['shipper_order_id'])
						#
						if getShipping != False:
							# Add payment fee to order line
							dataShipping = getShipping['data']['order']['detail']
							DeliveryFee = {
								'order_partner_id': customer,
								'product_id': delivery_fee.id,
								'product_uom_qty': 1,
								'price_unit': int(dataShipping['courier']['rate']['value']),
								'tax_id': [],
								'name': str(dataShipping['courier']['name']) + ' - ' + str(dataShipping['courier']['rate_name'])
							}
							orderline.append((0,0,DeliveryFee))
						else:
							DeliveryFee = {
								'order_partner_id': customer,
								'product_id': delivery_fee.id,
								'product_uom_qty': 1,
								'price_unit': 0,
								'tax_id': [],
								'name': 'Error saat menagmbil data Shipper!'
							}
							orderline.append((0,0,DeliveryFee))

					# ====================================================================================
					# Set other fields before create Order data
					# ====================================================================================
					# Set Order Date / Time delta decrease 7 hour to show id timezone in odoo
					dateOrder = datetime.strptime(data['payment_date'], '%Y-%m-%d %H:%M:%S')
					dateOrder = dateOrder - timedelta(hours=7,minutes=0)
					# Set status from sandbox status
					status = 'draft'
					if data['status'] == "CANCELLED":
						status = 'cancel'
					else:
						status = 'sale'
					#
					dataOrder = {
						'name': data['order_number'],
						'partner_id': customer,
						#'date_order': datetime.strptime(data['payment_date'], '%Y-%m-%d %H:%M:%S'),
						'date_order': dateOrder,
						'order_line': orderline,
						'state': status,
						'company_id': company_id,
						'order_type': data['order_type']
					}
					# Create order
					order = http.request.env['sale.order'].sudo().create(dataOrder)
					print('#### Data Order berhasil ditambahkan : ', order.name)
					# Create Invoice
					invoice = self.createInvoice(order, getCompany, data)
					# Check if order is not cancelled
					#if len(order.order_line) != 0 and status != 'cancel':
					if status != 'cancel':
						# Validate invoice
						invoice._post();
						# Sometime invoice name change, so check it
						# If the name changed, update to sandbox name again
						#print('========== Invoice Number : ', invoice.name)
						if invoice.name != data['invoice_number']:
							invoice.sudo().write({'name' : data['invoice_number']})
						# Automate payment for posted invoice
						payInvoice = self.payInvoice(invoice, getCompany, data['payment_channel'])
						# Check stock product
						stock = self.checkStockProduct(order, getCompany, user_id)
					else:
						# Cancel invoice
						invoice.button_cancel();
					# =================================================================================
		else:
			res = False
			print('Error : Terjadi error di fungsi orders')
		return res


	def getPaymentMethod(self, apiKey, merchant_id, paymentType):
		headers = {
			#'token': token,
			'api_key': apiKey,
			'content-type': 'application/json'
		}
		data = {}
		# Tanya entar apa bakalan beda tiap merchant untuk metode pembayarannya?
		url = 'https://sandbox-api.stagingapps.net/master/paymentmethod?device=MOBILEQR&merchant_id=' + str(merchant_id)
		response = requests.get(url, headers=headers, data=json.dumps(data))
		#
		if response.status_code == 200:		
			results = response.json()['data']
			res = False
			for payment in results:
				if payment['payment_code'] == paymentType:
					res = payment
		else:
			res = False
			print('Error : Terjadi error di fungsi orders')

		return res


	def sendNotification(self, company_id, user_id, message_text):
		# ================================================================================================
		# Send notification to discuss channel
		# ================================================================================================
		# Default message sender is OdooBot
		odoobot_id = http.request.env['res.users'].sudo().search([('id', '=', 1), ('active','=',False)], limit=1).partner_id.id
		# Get Chanel by users partner_id
		channel = http.request.env['mail.channel'].sudo().search([
			('name', '=', 'Stock Persediaan'),
			#('channel_partner_ids', 'in', [user.partner_id.id])
			('channel_partner_ids', 'in', [user_id])
		], limit=1)
		# If channel doesn't exist, create new
		if not channel:
			# Create new channel
			channel = http.request.env['mail.channel'].with_context(mail_create_nosubscribe=True).sudo().create({
				#'channel_partner_ids': [(4, user_id), (4, odoobot_id)],
				'channel_partner_ids': [(4, user_id), (4, odoobot_id), (4, 3)],
				'public': 'groups',
				'channel_type': 'channel',
				#'email_send': False,
				'name': f'Stock Persediaan',
				'display_name': f'Stok Persediaan',
			})
		# Send a message to the related user
		channel.sudo().message_post(
			body=message_text,
			author_id=odoobot_id,
			message_type="notification",
			subtype_id=None,
		) 


	def createInvoice(self, order, company, data):
		# ================================================================================================
		# Create invoice
		# ================================================================================================
		invoice_lines = []
		for line in order.order_line:
			if line.display_type == 'line_section':
				vals = {'name': line.name, 'display_type': 'line_section'}
			else:
				vals = {
					'name': line.name,
					'price_unit': line.price_unit,
					'quantity': line.product_uom_qty,
					'product_id': line.product_id.id,
					'product_uom_id': line.product_uom.id,
					'tax_ids': [(6, 0, line.tax_id.ids)],
					'sale_line_ids': [(6, 0, [line.id])],
				}
			invoice_lines.append((0, 0, vals))
		# Get Invoice Journal 
		journal = http.request.env['account.journal'].sudo().search([('company_id', '=', company.id), ('type', '=', 'sale')], limit=1)
		#print('=================== INI DATA JURNAL', journal)
		# Get Rounding Method
		rounding = http.request.env['account.cash.rounding'].search([], limit=1)
		#print('================== Ini data rounding : ', rounding.name)
		# Create Invoice
		invoice = http.request.env['account.move'].sudo().create({
			'ref': order.client_order_ref,
			'move_type': 'out_invoice',
			'date': order.date_order,
			'invoice_origin': order.name,
			'invoice_user_id': order.user_id.id,
			'partner_id': order.partner_invoice_id.id,
			'currency_id': order.pricelist_id.currency_id.id,
			'invoice_line_ids': invoice_lines,
			'company_id': company.id,
			'name': data['invoice_number'],
			'payment_reference': data['invoice_number'],
			'journal_id': journal.id,
			'invoice_cash_rounding_id': rounding.id,
		})

		return invoice

	def checkStockProduct(self, order, company, user_id):
		# ================================================================================================
		# Product stock check,
		# If the product is not available, send message to user
		# If the product available, validate stock product
		# ================================================================================================
		

		stock = http.request.env['stock.picking'].search([('origin', '=', order.name)], limit=1)
		


		if stock.products_availability_state != 'available':
			msg = f'<strong>' + str(company.name) + ' - Info Stok</strong> ' \
				f'<p>Order Pengiriman : ' + str(stock.origin) + '</p>' \
				f'<p>Referensi : ' + str(stock.name) + '</p>' \
				f'<p>Status : ' + str(stock.products_availability) + '</p>' \
				f'<p>Harap lakukan penyesuaian stok produk.'
			#sendNotification
			self.sendNotification(company.id, user_id, msg)
		else:
			immediate_transfer_line_ids = []
			for picking in order.picking_ids:
				immediate_transfer_line_ids.append([0, False, {
					'picking_id': picking.id,
					'to_immediate': True
				}])
			res = self.env['stock.immediate.transfer'].create({
				'pick_ids': [(4, p.id) for p in order.picking_ids],
				'show_transfers': False,
				'immediate_transfer_line_ids': immediate_transfer_line_ids
			})
			res = res.with_context(button_validate_picking_ids=res.pick_ids.ids).process()
			# Change state to done
			stock.sudo().write({'state': 'done'}) 

	def payInvoice(self, invoice, company, payment_channel):
		# ================================================================================================
		# Automate payment for posted invoice
		# Select journal based on payment_channel
		# If "cash" go to journal "Kas", the rest go to journal "Bank"
		# ================================================================================================
		if payment_channel == "cash":
			journal = http.request.env['account.journal'].sudo().search([('company_id', '=', company.id), ('type', '=', 'cash')], limit=1)
		else:
			journal = http.request.env['account.journal'].sudo().search([('company_id', '=', company.id), ('type', '=', 'bank')], limit=1)
		#
		payment = http.request.env['account.payment'].with_context(default_invoice_ids=[(4, invoice.id, False)])
		payment = payment.create({
			'date': invoice.date,
			'payment_method_id': 1,
			'payment_type': 'inbound',
			'partner_type': 'customer',
			'partner_id': invoice.partner_id.id,
			'amount': int(invoice.amount_total),
			'journal_id': journal.id,
			'company_id': company.id,
			'currency_id': company.currency_id.id,
		})
		# Post payment
		payment.action_post()
		# Get rececivable_line from payment
		receivable_line = payment.line_ids.filtered('credit')
		# Match payment with invoce to update status to "Paid"
		invoice.js_assign_outstanding_line(receivable_line.id)


	def getShipperData(self, apiKey, shipper_id):
		# Post ID to get data shipper
		headers = {
			'api_key': apiKey,
			#'token': token,
			'content-type': 'application/json'
		}
		body = {}
		url = "https://sandbox-api.stagingapps.net/shipper/tracking-shipment-status?id=" + str(shipper_id)
		response = requests.get(url, headers=headers, data=json.dumps(body))		        
		if response.status_code == 200:
			data = response.json()
			if data['status'] != 'fail':
				data = data
			else:
				data = False
		else:
			data = False
		#
		return data

