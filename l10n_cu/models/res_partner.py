# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResCnae(models.Model):
    _name = 'res.cnae'
    _description = "CNAE"
    _rec_name = "complete_name"
    _order = "code"

    def name_get(self):
        return [(record.id, "%s - %s" % (record.code, record.name)) for record in self]

    code = fields.Char()
    name = fields.Char()
    industry_id = fields.Many2one("res.partner.industry", "Sector")

    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True)

    @api.depends('code', 'name')
    def _compute_complete_name(self):
        for cnae in self:
            cnae.complete_name = '%s - %s' % (cnae.code, cnae.name)


class ResCnaeLine(models.Model):
    _name = 'res.cnae.line'
    _description = "CNAE Line"
    _sql_constraints = [
        ('check_cnae_id', 'unique(partner_id, cnae_id)',
         'Las actividades economicas deben ser unicas.!')
    ]

    sequence = fields.Integer('Sequence', default=1,
                              help="Usado para organizar las actividades. La Actividad Principal será la de primer orden.")
    cnae_id = fields.Many2one("res.cnae", "Clasificador Nacional de Activdades Económicas", required=True)
    partner_id = fields.Many2one("res.partner", "Partner", required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_cu_cnae_ids = fields.One2many('res.cnae.line', 'partner_id',
                                       string='Clase económica a la que pertenece (CNAE)')

    @api.onchange('l10n_cu_cnae_ids')
    def onchange_cnae_ids(self):
        for res in self:
            if res.l10n_cu_cnae_ids:
                res.industry_id = res.l10n_cu_cnae_ids[0].cnae_id.industry_id
            else:
                res.industry_id = False
