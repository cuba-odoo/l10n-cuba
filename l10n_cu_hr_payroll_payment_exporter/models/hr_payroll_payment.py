# -*- coding: utf-8 -*-
from odoo import fields, models, api

class HrPayslipPayment(models.Model):
    _inherit = 'hr.payslip.payment'

    archive = fields.Binary("Archive", copy=False)
    filename = fields.Char('Filename', default="massive.dbf")

    def action_generate_txt(self):
        pass
