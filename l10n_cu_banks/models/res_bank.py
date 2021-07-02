# -*- coding: utf-8 -*-
from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    municipality = fields.Many2one('res.state.municipality', string='Municipality')
