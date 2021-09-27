# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.osv import expression

class Municipality(models.Model):
    _name = 'res.municipality'
    _description = 'Municipio'
    _order = 'code'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='El código del municipio', required=True)
    country_id = fields.Many2one('res.country', string='Country', default='base.cu', required=True)
    state_id = fields.Many2one('res.country.state', 'State', domain="[('country_id', '=', country_id)]")
#    zipcode = fields.Many2one('res.city', string='Zip')

    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, code)', '¡El código del municipio debe ser único por provincia!')
    ]