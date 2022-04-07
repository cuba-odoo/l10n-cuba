# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class AccountFinancialReport(models.Model):
    _inherit = 'account.financial.report'

    plan_anual = fields.Float("Plan Anual", help="Lo que se definió en el presupuesto.")
    apertura = fields.Float("Apertura")
    visible = fields.Boolean('Visible', default=True)
    type = fields.Selection(selection_add=[
        # ('account_group', 'Account Group'),
        ('account_reports', 'Reports Value'),
    ], ondelete={'account_reports': 'set default'})
    account_report_ids = fields.Many2many('account.financial.report', 'rel_account_report', 'account_report_id',
                                          'account_report_rel_id', string='Report Value', help="Hola")
