# -*- coding: utf-8 -*-

from odoo import models, fields 

class State(models.Model):
    _inherit = 'res.country.state'

    municipality_id = fields.One2many('res.state.municipality', 'name', string='Municipality')
        