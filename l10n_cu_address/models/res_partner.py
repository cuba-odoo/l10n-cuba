# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    municipality_id = fields.Many2one(
        'res.municipality',
        'Municipio',
        domain="[('state_id', '=', state_id)]",
        help="Municipios de Cuba"
    )

    municipality_name = fields.Char(string="Nombre del Municipio", related='municipality_id.name')

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.municipality_id not in self.state_id.municipality_ids:
            self.municipality_id = False

    @api.model
    def _address_fields(self):
        return super()._address_fields() + ['municipality_name']
