# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class restapi(models.Model):
#     _name = 'restapi.restapi'
#     _description = 'restapi.restapi'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


# from odoo import models, fields, api

# class AccountMove(models.Model):
# 	_inherit = 'account.move'

# 	# Field kustom res.partner
# 	company_id = fields.Many2one(comodel_name='res.company', string='Company',
#                                  store=True, readonly=True)