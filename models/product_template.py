# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, http, models, _
import json
import requests


class ProductTemplate(models.Model):
	_inherit = 'product.template'


	# def action_update_product(self):
	# 	print("Dipencet")
	# 	#
	# 	CompanyData = http.request.env['res.company'].search([('id', '=', self.env.company.id)], limit=1)
	# 	#
	# 	apiKey = CompanyData.sandbox_key
	# 	us = CompanyData.sandbox_id
	# 	pw = CompanyData.sandbox_pw
	# 	company_id = CompanyData.id
	# 	#
	# 	msg_text = ''
	# 	msg_type = ''


	# 	token = self.env['api.scheduler'].getToken(apiKey, us, pw)

	# 	if token != False:
	# 		#print(token)
	# 		products = self.env['api.scheduler'].cronProducts(apiKey, token, company_id)
	# 		if products != False:
	# 			msg_text = 'Data produk berhasil diupdate!'
	# 			msg_type = 'success'
	# 		else:
	# 			msg_text = 'Terjadi kesalahan saat mengambil data produk!'
	# 			msg_type = 'danger'
	# 	else:
	# 		msg_text = 'Terjadi kesalahan, Api Key / Username / Password mungkin salah!'
	# 		msg_type = 'danger'

	# 	#print("Ini data apiKey : ", apiKey)

	# 	return {
	# 		'type': 'ir.actions.client',
	# 		'tag': 'display_notification',
	# 		'params': {
	# 			'message': msg_text,
	# 			'type': msg_type,
	# 			'sticky': True,
	# 		}
	# 	}





