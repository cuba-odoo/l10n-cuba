# -*- coding: utf-8 -*-

from odoo import api, models, fields
# from odoo.osv import expression

from odoo import models, fields

from odoo import models, fields


class ResMunicipality(models.Model):
    _name = 'res.municipality'
    _description = 'Municipality'
    _order = 'code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', help='The municipality code.', required=True, index=True)

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        required=True,
        index=True
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
        domain="[('country_id', '=?', country_id)]",
        index=True
    )

    # --- Nueva sintaxis Odoo 19 para SQL Constraints ---
    # El nombre de la variable ('_name_code_uniq') será el nombre del constraint en PostgreSQL
    _name_code_uniq = models.Constraint(
        'UNIQUE(state_id, code)',
        'The municipality code must be unique per state!'
    )
