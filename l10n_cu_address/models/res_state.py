# -*- coding: utf-8 -*-

from odoo import models, fields


class State(models.Model):
    _inherit = 'res.country.state'

    municipality_ids = fields.One2many(
        'res.municipality', 'state_id', 'Municipio', help="Municipios de Cuba"
    )
