# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.osv import expression

class Municipality(models.Model):
    _name = 'res.municipality'
    _description = 'Municipio'
    _order = 'code'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='El código del municipio', required=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', 'State', domain="[('country_id', '=', country_id)]")

    models.Constraint = [
        ('name_code_uniq', 'unique(state_id, code)', '¡El código del municipio debe ser único por provincia!')
    ]
