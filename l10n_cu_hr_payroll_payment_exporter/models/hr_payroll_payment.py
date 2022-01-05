# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError

class HrPayslipPayment(models.Model):
    _inherit = 'hr.payslip.payment'

    archive = fields.Binary("Archive", copy=False)
    filename = fields.Char('Filename', default="massive.dbf")

    def action_validate(self):
        """ Validar los requisitos del banco. """
        self.ensure_one()
        if not self.total:
            raise UserError("No existen lineas de nóminas para este pago.")

        for line in self.payslip_line_ids:
            if line.total_on_payable:
                raise UserError("El total a pagar de la nómina %s debe ser superior a 0." % line.name)
            if line.state != 'done':
                raise UserError("La nómina %s tiene que estar en estado de Confirmada." % line.name)
            if not line.employee_id.identification_id:
                raise UserError("El usuario %s no tiene especificado un Carnet de Identidad." % line.employee_id.name)

        self.state = 'validate'

    def action_generate_txt(self):
        pass
