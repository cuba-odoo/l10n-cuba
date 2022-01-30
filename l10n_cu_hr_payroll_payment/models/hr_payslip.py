# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    payslip_payment_id = fields.Many2one('hr.payslip.payment', 'Payslip Payment', copy=False)

    def action_payslip_done(self):
        if not self.employee_id.address_home_id:
            raise UserError("El empleado %s no tiene una dirección privada." % self.employee_id.name)
        res = super(HrPayslip, self).action_payslip_done()
        return res
