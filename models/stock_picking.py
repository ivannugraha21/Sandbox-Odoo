# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo import api, fields, models, SUPERUSER_ID, _, http

# class StockPicking(models.Model):
# 	_inherit = 'stock.picking'

# 	def create(self, vals):
# 		res = super(StockPicking, self).create(vals)
# 		#create condition only receipt document
# 		print('Create Stock')
# 		print('===================================== Data Vals :')
# 		print(vals)
# 		print('===================================== Data Self :')
# 		print(res.products_availability_state)
# 		if res.products_availability_state != 'available':
# 			print('Send Message')
# 			#define purchase user by group
# 			# purchase_group = self.env.ref('purchase.group_purchase_user')
# 			# purchase_user = self.env['res.users'].search([('groups_id', '=', purchase_group)])
# 			#purchase_user = self.env['res.users'].search([('id', '=', 6)])
# 			notification_ids = []
# 			#for purchase in purchase_user:
# 			notification_ids.append((0,0,{
# 				'res_partner_id': 6,
# 				'notification_type':'inbox'
# 			}))

# 			http.request.env['stock.picking'].message_post(body='This receipt has been validated!', message_type='notification', subtype='mail.mt_comment', author_id='2', notification_ids=notification_ids)

# 		return res

# # Belum dicoba




