# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
	_inherit = 'account.move'

	# Field kustom untuk product
	new_invoice_name = fields.Char(string="No invoice dari Sandbox")
	
