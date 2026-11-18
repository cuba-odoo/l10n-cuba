# -*- coding: utf-8 -*-
from odoo import fields, models


class HrPayrollOtherInput(models.Model):
    _name = 'hr.payroll.other.input'
    _description = "Payroll Other Input"

    employee_id = fields.Many2one("hr.employee", "Employee")
    rule_input_id = fields.Many2one("hr.rule.input", "Code", required=True)
    amount = fields.Float("Amount", required=True)
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
