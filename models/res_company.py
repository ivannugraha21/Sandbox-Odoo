# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResCompany(models.Model):
	_inherit = 'res.company'

	# Field kustom res.company
	sandbox_key = fields.Char(string="Api Key untuk akses Sandbox")
	sandbox_id = fields.Char(string="User id untuk api Sandbox")
	sandbox_pw = fields.Char(string="Pass id untuk api Sandbox")
	sandbox_merchant_id = fields.Integer(string="Merchant id from sandbox")
	sandbox_payment_fee = fields.Selection([
			('SPLIT', 'Split'),
			('OWNER', 'Owner'),
			('CUSTOMER', 'Customer') 
		], default="SPLIT", string="Tipe payment fee dari sandbox")


	def action_update_manual(self):
		if self.sandbox_id != False:
			#print("Next")
			msg_text = ''
			msg_type = '' 
			#
			if self.sandbox_pw != False:
				#print("After Next")
				# Get token using value from fields
				apiKey = self.sandbox_key
				us = self.sandbox_id
				pw = self.sandbox_pw
				company_id = self.id
				token = self.env['api.scheduler'].getToken(apiKey, us, pw)
				# Check response
				if token != False:
					# Update Customers
					customers = self.env['api.scheduler'].cronCustomers(apiKey, token, company_id)
					if customers != False:
						#print(customers)
						# Update Products
						products = self.env['api.scheduler'].cronProducts(apiKey, token, company_id)
						if products != False:
							#print(products)
							# Set/Update Taxes
							taxes = self.env['api.scheduler'].cronTaxes(apiKey, token, company_id)
							if taxes != False:
								#print(taxes)
								# Update Orders
								orders = self.env['api.scheduler'].cronOrders(apiKey, token, company_id)
								if orders != False:
									#print(orders)
									msg_text = 'Semua data berhasil diupdate!'
									msg_type = 'success'
								else:
									msg_text = 'Terjadi kesalahan saat mengambil data order!'
									msg_type = 'danger'
									#raise ValidationError(_("Terjadi kesalahan saat mengambil data order!"))
							else:
								msg_text = 'Terjadi kesalahan saat mengambil data pajak!'
								msg_type = 'danger'
								#raise ValidationError(_("Terjadi kesalahan saat mengambil data pajak!"))
						else:
							msg_text = 'Terjadi kesalahan saat mengambil data produk!'
							msg_type = 'danger'
							#raise ValidationError(_("Terjadi kesalahan saat mengambil data produk!"))
					else:
						msg_text = 'Terjadi kesalahan saat mengambil data pelanggan!'
						msg_type = 'danger'
						#raise ValidationError(_("Terjadi kesalahan saat mengambil data pelanggan!"))
				else:
					msg_text = 'Terjadi kesalahan, Api Key / Username / Password mungkin salah!'
					msg_type = 'danger'
					#raise ValidationError(_("Terjadi kesalahan, Api Key / Username / Password mungkin salah!"))
			else:
				msg_text = 'Harap isi password terlebih dahulu!'
				msg_type = 'danger'
				#raise ValidationError(_("Harap isi password terlebih dahulu!"))
		else:
			msg_text = 'Harap isi username terlebih dahulu!'
			msg_type = 'danger'
			#raise ValidationError(_("Harap isi username terlebih dahulu!"))

		
		return {
			'type': 'ir.actions.client',
			'tag': 'display_notification',
			'params': {
				'message': msg_text,
				'type': msg_type,
				'sticky': True,
			}
		}











