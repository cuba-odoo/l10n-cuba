# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResCnae(models.Model):
    _name = 'res.cnae'
    _description = "CNAE"

    def name_get(self):
        return [(record.id, "%s - %s" % (record.code, record.name)) for record in self]

    code = fields.Char()
    name = fields.Char()


class ResCnaeLine(models.Model):
    _name = 'res.cnae.line'
    _description = "CNAE Line"
    _sql_constraints = [
        ('check_cnae_id', 'unique(cnae_id)',
         'Las actividades economicas deben ser unicas.!')
    ]

    sequence = fields.Integer('Sequence', default=1,
                              help="Usado para organizar las actividades. La Actividad Principal sera la de primer orden.")
    cnae_id = fields.Many2one("res.cnae", "Clasificador Nacional de Activdades Economicas", required=True)
    company_id = fields.Many2one("res.company", "Company", required=True)


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_cu_cnae_ids = fields.One2many('res.cnae.line', 'company_id',
                                       string='Clase económica a la que pertenece (CNAE)')
