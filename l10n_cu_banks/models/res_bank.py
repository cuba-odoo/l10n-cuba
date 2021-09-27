# -*- coding: utf-8 -*-

from odoo import api, models, fields


class Bank(models.Model):
    _name = 'res.bank'
    _inherit = "res.bank"

    res_municipality_id = fields.Many2one('res.municipality', 'Municipio', domain="[('state_id', '=', state)]", help="Municipios de Cuba")

    @api.onchange('state')
    def _onchange_state(self):
        if self.state.country_id:
            self.country = self.state.country_id
        self.res_municipality_id = ""
