# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResProduct(models.Model):
	_inherit = 'product.product'

	# Field kustom untuk product
	merchant_id = fields.Integer(string="Merchant id from Sandbox")
	brand_id = fields.Integer(string="Brand id from Sandbox")
	product_id = fields.Integer(string="Product id from Sandbox")
	product_discount = fields.Integer(string="Product discount", default=0)
	product_payments = fields.Integer(string="Other payment. eg: xendit / delivery")
