# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
import base64
DEFAULT_DIGITS = (16, 2)

class HrPayslipPayment(models.Model):
    _inherit = 'hr.payslip.payment'
    _description = "Payslip Payment"

    archive = fields.Binary("Archive", copy=False)
    filename = fields.Char('Filename', default="massive.dbf")

    def action_generate_txt(self):
        pass

