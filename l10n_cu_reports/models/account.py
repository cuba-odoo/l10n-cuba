# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class AccountFinancialReport(models.Model):
    _inherit = 'account.financial.report'

    plan_anual = fields.Float("Plan Anual", help="Lo que se definión en el presupuesto.")
    apertura = fields.Float("Apertura")

