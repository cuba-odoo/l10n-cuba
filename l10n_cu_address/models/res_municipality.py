# -*- coding: utf-8 -*-

from odoo import models, fields 

class Municipality(models.Model): 
    _name = 'res.state.municipality' 
    _description = 'Municipality'
    _order = 'name'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    country_id = fields.Many2one('res.country', string='Country', default='base.cu', required=True)
    state_id = fields.Many2one('res.country.state', 'State', domain="[('country_id', '=', country_id)]")
#    zipcode = fields.Many2one('res.city', string='Zip')
