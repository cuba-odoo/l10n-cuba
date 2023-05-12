# -*- coding: utf-8 -*-

from odoo import models, fields 

class State(models.Model):
    _inherit = 'res.country.state'

    municipality_ids = fields.One2many('res.municipality', 'state_id', string='Municiipalities')
    
    def get_website_sale_municipalities(self, mode='billing'):
        return self.sudo().municipality_ids