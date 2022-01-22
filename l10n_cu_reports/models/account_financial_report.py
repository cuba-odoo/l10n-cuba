# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class AccountFinancialReport(models.Model):
    _inherit = 'account.financial.report'

    plan_anual = fields.Float("Plan Anual", help="Lo que se definión en el presupuesto.")
    apertura = fields.Float("Apertura")
    visible = fields.Boolean('Visible', default=True)
    type = fields.Selection(selection=[
        ('sum', 'View'),
        ('accounts', 'Accounts'),
        ('account_group', 'Account Group'),
        ('account_type', 'Account Type'),
        ('account_report', 'Report Value'),
    ])

