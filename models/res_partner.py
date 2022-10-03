# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
	_inherit = 'res.partner'

	# Field kustom res.partner
	partner_merchant_id = fields.Integer(string="Merchant id dari Sandbox")
	partner_status = fields.Selection([
			('customer', 'Pelanggan')
		], string="Status partner")
	customer_id = fields.Char(string="Customer id dari Sandbox")
	last_purchase = fields.Char(string="Data pembelian terakhir dari Sandbox")