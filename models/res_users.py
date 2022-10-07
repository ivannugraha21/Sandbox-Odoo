# -*- coding: utf-8 -*-

from odoo import models, fields, api, http, _
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
	_inherit = 'res.users'

	# Field kustom res.company
	sandbox_apikey = fields.Char(string="Api Key untuk akses Sandbox")
	sandbox_id = fields.Char(string="User untuk akses Sandbox")
	sandbox_pw = fields.Char(string="Pass untuk kases Sandbox")

	def action_update_manual(self):
		# Get current user info
		active_user = self.env.user
		# Send current user id to scheduler cron function
		http.request.env['api.scheduler'].cron_schedule(active_user.id)
		#
		return