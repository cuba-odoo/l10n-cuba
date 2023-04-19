# -*- coding: utf-8 -*-
# © 2015 Salton Massally <smassally@idtlabs.sl>
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    cod_depositante = fields.Char(string='Codigo depositante',
                                  help='Codigo del SUA')

