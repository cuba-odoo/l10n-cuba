# -*- coding: utf-8 -*-

from odoo import models, fields 

class State(models.Model):
    _inherit = 'res.country.state'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipio', help="Municipios de Cuba")
