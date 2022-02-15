# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure', required=True,
                                help="Si lo que desea es relizar una nómina por días trabajados seleccione (operativa o "
                                     "administrativa).")

    def compute_sheet(self):
        """Override"""
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(['date_start', 'date_end', 'credit_note', 'journal_id'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):

            contract_ids = employee.contract_ids
            if self.struct_id.id not in [c.struct_id.id for c in contract_ids]:
                raise UserError("El empleado %s no tiene ningún contrato con la Estructura Salarial seleccionada." % employee.name)

            contract_struct = contract_ids.filtered(lambda contract: contract.struct_id.id == self.struct_id.id)
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)

            res = {
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                # 'struct_id': slip_data['value'].get('struct_id'),
                'struct_id': self.struct_id and self.struct_id.id or slip_data['value'].get('struct_id'),
                # 'contract_id': slip_data['value'].get('contract_id'),
                'contract_id': contract_struct[0].id,
                'payslip_run_id': active_id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': run_data.get('credit_note'),
                'company_id': employee.company_id.id,
            }
            slip_create = self.env['hr.payslip'].create(res)
            slip_create.journal_id = run_data.get('journal_id')
            slip_create.with_context(contract=True).onchange_employee()
            payslips += slip_create

        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
