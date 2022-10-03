# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResAccountTax(models.Model):
	_inherit = 'account.tax'

	# Field kustom account.tax
	sandbox_tax = fields.Boolean(string="Data tax dari Sandbox", default=False)
	sandbox_service = fields.Boolean(string="Data service dari Sandbox", default=False)