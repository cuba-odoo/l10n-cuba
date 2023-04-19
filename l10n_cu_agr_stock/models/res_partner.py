# -*- coding: utf-8 -*-
# © 2015 Salton Massally <smassally@idtlabs.sl>
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _


class ResPartnerNfm(models.Model):
    _name = 'res.partner.nfm'
    _description = 'Nacion mas favorecida'

    code = fields.Char('Code', size=64, required=True, index=True)
    name = fields.Char('Name', size=2048, required=True, translate=True, index=True)
    res_partner_ids = fields.One2many('res.partner', 'nfm_id', string='NFM', ondelete='cascade')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nfm_id = fields.Many2one('res.partner.nfm', string='Nfm', ondelete='cascade', help='Nfm')



