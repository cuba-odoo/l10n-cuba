# -*- coding: utf-8 -*-

from odoo import models, fields 

class Partner(models.Model):
    _inherit = 'res.partner'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipio', domain="[('state_id', '=', state_id)]", help="Municipios de Cuba" )