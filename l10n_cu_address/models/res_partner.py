# -*- coding: utf-8 -*-

from odoo import models, fields 

class Partner(models.Model):
    _inherit = 'res.partner'

    municipality_id = fields.Many2one('res.state.municipality', string='Municipality of Address', domain="[('state_id', '=', state_id)]")
    