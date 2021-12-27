# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
import base64

class HrPayslipPayment(models.Model):
    _inherit = 'hr.payslip.payment'
    _description = "Payslip Payment"

    def action_generate_txt(self):
        self.action_validate()
        self.ensure_one()
        date_obj = datetime.strptime(str(self.date), '%Y-%m-%d')
        date = date_obj.strftime('%d%m%Y')
        center_payment = "S"
        amount = "{0:.2f}".format(self.total)
        arch = "\"%s\",\"%s\",%s,\"%s\"\n" % (date, center_payment, amount, self.qty_paid)

        for line in self.payslip_line_ids:
            if line.employee_id.bank_account_id:
                account = line.employee_id.bank_account_id.acc_number
                sub_total = "{0:.2f}".format(line.total)
                subsidiary = "S"
                arch += "\"%s\",\"%s\",%s,\"%s\",\"%s\",\"%s\"\n" % (
                line.employee_id.identification_id, account, sub_total, subsidiary, 'S', 'S')

        message_bytes = arch.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        self.write({'archive': base64_bytes, 'filename': '%s.txt' % self.name})

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'target': 'current',
            'res_id': self.id
        }
