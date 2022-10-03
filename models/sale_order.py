# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json
import math


from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils

class SaleOrder(models.Model):
	_inherit = 'sale.order'


	order_type = fields.Char(string="Type Order from Sandbox")


	
	# @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
	# def _compute_tax_totals_json(self):
	# 	def compute_taxes(order_line):
	# 		#price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
	# 		price = order_line.price_unit
	# 		order = order_line.order_id
	# 		return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)

	# 	account_move = self.env['account.move']
	# 	for order in self:
	# 		tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
	# 		tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
	# 		print(tax_totals)
	# 		#
	# 		#tax_totals['amount_total'] = math.ceil(tax_totals['amount_total'])
	# 		#
	# 		order.tax_totals_json = json.dumps(tax_totals)







