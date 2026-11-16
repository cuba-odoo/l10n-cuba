# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    struct_id = fields.Many2one(
        'hr.payroll.structure', string='Salary Structure', required=True,
        help="To compute a payslip by worked days, select the operational or administrative structure.")

    def compute_sheet(self):
        """Generate the batch payslips with the contract of each employee that uses the selected structure."""
        active_id = self.env.context.get('active_id')
        if not active_id:
            raise UserError(_("Generate the payslips from a payslip batch."))
        if not self.employee_ids:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        run = self.env['hr.payslip.run'].browse(active_id)
        payslips = self.env['hr.payslip']
        for employee in self.employee_ids:
            contract = employee.contract_ids.filtered(lambda c: c.struct_id == self.struct_id)[:1]
            if not contract:
                raise UserError(_(
                    "The employee %(employee)s has no contract with the selected salary structure.",
                    employee=employee.name))
            slip_data = payslips.onchange_employee_id(run.date_start, run.date_end, employee.id, contract_id=False)
            payslip = payslips.create({
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                'struct_id': self.struct_id.id,
                'contract_id': contract.id,
                'payslip_run_id': run.id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': run.date_start,
                'date_to': run.date_end,
                'credit_note': run.credit_note,
                'company_id': employee.company_id.id,
            })
            if run.journal_id:
                payslip.journal_id = run.journal_id
            payslip.with_context(contract=True).onchange_employee()
            payslips += payslip
        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('struct_id')
    def _onchange_struct(self):
        if self.struct_id:
            self.employee_ids = self.env['hr.employee'].search([('contract_id.struct_id', '=', self.struct_id.id)])
