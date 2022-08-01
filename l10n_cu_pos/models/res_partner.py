# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cnae_primary = fields.Char("CNAE Primary", compute="_compute_cnae_primary", inverse="_inverse_cnae_primary")

    @api.depends("l10n_cu_cnae_ids.cnae_id")
    def _compute_cnae_primary(self):
        for res in self:
            res.cnae_primary = res.l10n_cu_cnae_ids and res.l10n_cu_cnae_ids[0].cnae_id.code or False

    def _inverse_cnae_primary(self):
        for res in self:
            cnae_id = self.env["res.cnae"].search([('code', '=', res.cnae_primary)])
            if cnae_id:
                res.l10n_cu_cnae_ids.unlink()
                values = {'sequence': 0, 'cnae_id': cnae_id.id, 'partner_id': res.id}
                self.env["res.cnae.line"].create(values)
